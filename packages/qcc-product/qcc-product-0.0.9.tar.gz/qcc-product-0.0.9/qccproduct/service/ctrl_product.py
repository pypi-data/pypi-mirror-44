# coding:utf-8

from qccproduct.db import mongo as db
from tweb.json_util import filter_keys
from tweb.error_exception import ErrException, ERROR
from tweb import time
from bson.objectid import ObjectId
from webmother.service import ctrl_catalog
from webmother import Passport
import re


# 分类节点状态以及状态迁移定义
class Status:
    removed = -10  # 已删除
    editing = 0  # 编辑中
    auditing = 10  # 待审(审核中)
    sleeping = 20  # 休眠中
    activated = 30  # 已激活

    status_map = {
        editing: {'submit': auditing, 'remove': removed},
        auditing: {'reject': editing, 'audit': sleeping, 'remove': removed},
        sleeping: {'activate': activated, 'remove': removed},
        activated: {'deactivate': sleeping}
    }

    @staticmethod
    def trans(cur_status, action):
        """
        在当前状态，进行操作将会得到新的状态
        :param cur_status: 当前状态
        :param action: 操作名称
        :return: 新的状态
        """

        valid_actions = Status.status_map.get(cur_status)
        if valid_actions is None:
            raise ErrException(ERROR.E40022, extra=f'current status is {cur_status}, forbid change status')

        new_status = valid_actions.get(action)
        if new_status is None:
            raise ErrException(ERROR.E40022, extra=f'current status is {cur_status}, wrong action [{action}]')

        return new_status


def create(cid, prod_meta, *auth_args):
    name = prod_meta['name'].lower()
    if not re.match(r'^[\w-]{0,19}$', name):
        raise ErrException(ERROR.E40000, extra='name should be 20 letter, number, _, -, and beginning with letter')

    c = ctrl_catalog.simple_read(cid)

    # 授权检查
    Passport().verify(*auth_args).operable(c.get('node'), 'product.create')
    # END

    if c['status'] not in [ctrl_catalog.Status.sleeping, ctrl_catalog.Status.activated]:
        raise ErrException(ERROR.E40300, extra='can not add something into catalog because it not audited')

    if db.product.find_one({'name': name, 'status': {'$gte': 0}}) is not None:
        raise ErrException(ERROR.E40020)

    prod_meta['catalog'] = ObjectId(cid)
    prod_meta['status'] = Status.editing

    now = time.millisecond()
    prod_meta['created'] = now
    prod_meta['updated'] = now

    result = db.product.insert_one(prod_meta)
    return simple_read(result.inserted_id)


def read(cid, pid, *auth_args):
    c = ctrl_catalog.simple_read(cid)

    # 授权检查
    # 因为授权限制操作授权本级节点，故在这里加一个'/product'，表示是读取子节点
    Passport().verify(*auth_args).operable('{}/product'.format(c.get('node')), 'product.read')
    # END

    return simple_read(pid)


def simple_read(pid):
    p = db.product.find_one({'_id': ObjectId(pid), 'status': {'$gte': 0}}, {'catalog': 0})
    if p is None:
        raise ErrException(ERROR.E40400, extra=f'the product({pid}) not existed')

    p['pid'] = p.pop('_id').__str__()

    return p


def update(cid, pid, prod_meta, *auth_args):
    """
    修改产品信息
    :param cid: 产品所属分类节点ID
    :param pid: 产品id
    :param prod_meta: 产品信息
    :param auth_args: 鉴权参数：(signed, nonce), 即("签名的授权字符串", "临时一致性标示，需与生成签名时使用的nonce相同")
    :return:
    """
    c = ctrl_catalog.simple_read(cid)

    # 授权检查
    Passport().verify(*auth_args).operable('{}/product'.format(c.get('node')), 'product.update')
    # END

    p = simple_read(pid)
    if p is None:
        raise ErrException(ERROR.E40400, extra='wrong product id')

    if p['status'] not in (Status.editing, Status.auditing, Status.sleeping, Status.activated):
        raise ErrException(ERROR.E40021)

    new_data = filter_keys(prod_meta, {
        'display': 1,
        'desc': 1,
        'icon': 1
    })

    new_data['status'] = Status.editing
    new_data['updated'] = time.millisecond()

    db.product.update_one({'_id': ObjectId(pid)}, {'$set': new_data})
    return simple_read(pid)


def change_status(cid, pid, action, *auth_args):
    """
    :param cid: 产品所属分类节点ID
    :param pid: 产品id
    :param action: 操作（提交，过审，驳回，上架，下架，删除等）
    :param auth_args: 鉴权参数：(signed, nonce), 即("签名的授权字符串", "临时一致性标示，需与生成签名时使用的nonce相同")
    :return:
    """
    c = ctrl_catalog.simple_read(cid)

    # 授权检查
    Passport().verify(*auth_args).operable('{}/product'.format(c.get('node')), f'product.{action}')
    # END

    p = simple_read(pid)
    if p is None:
        raise ErrException(ERROR.E40400, extra='wrong product id')

    cur_status = p.get('status')
    new_status = Status.trans(cur_status, action)

    new_data = {
        'status': new_status,
        'updated': time.millisecond()
    }

    db.product.update_one({'_id': ObjectId(pid)}, {'$set': new_data})

    return {'id': pid, 'status': new_status, 'old_status': cur_status}


def move(cid, pid, cid_to, *auth_args):
    """
    把cid节点下的pid产品移到cid_to标示的节点之下
    :param cid: 原节点ID
    :param pid: 产品ID
    :param cid_to: 新节点ID
    :param auth_args: 鉴权参数：(signed, nonce), 即("签名的授权字符串", "临时一致性标示，需与生成签名时使用的nonce相同")
    :return:
    """
    c = ctrl_catalog.simple_read(cid)
    c_to = ctrl_catalog.simple_read(cid_to)

    if cid == cid_to:
        raise ErrException(ERROR.E40000, extra='the same node, not need move')

    # 授权检查
    Passport().verify(*auth_args).operable('{}/product'.format(c['node']), 'product.remove')
    Passport().verify(*auth_args).operable('{}/product'.format(c_to['node']), 'product.create')
    # END

    p = simple_read(pid)
    if p['status'] not in (Status.editing, Status.auditing, Status.sleeping, Status.activated):
        raise ErrException(ERROR.E40021)

    now = time.millisecond()

    tmp_p = {
        'catalog': ObjectId(cid_to),
        'updated': now
    }

    db.product.update_one({'_id': ObjectId(pid)}, {'$set': tmp_p})

    return simple_read(pid)


def query_products(cid, *auth_args):
    # c = ctrl_catalog.simple_read(cid)

    # 读取产品列表为公开接口
    # 授权检查
    # 因为授权限制操作授权本级节点，故在这里加一个'/products'，表示是读取子节点
    # Passport().verify(*auth_args).operable('{}/products'.format(c.get('node')), 'product.read')
    # END

    cursor = db.product.find({'catalog': ObjectId(cid), 'status': {'$gte': 0}}, {'catalog': 0})

    array = list()
    for item in cursor:
        item['pid'] = item.pop('_id').__str__()
        array.append(item)

    return array
