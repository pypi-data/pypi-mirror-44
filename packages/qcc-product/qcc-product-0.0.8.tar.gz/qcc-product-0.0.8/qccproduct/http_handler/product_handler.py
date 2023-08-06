# coding=utf-8

from tweb import base_handler, myweb
from tweb.error_exception import ErrException, ERROR
from tornado import gen
import json
from qccproduct.service.async_wrap import ctrl_product


class ProductHandler(base_handler.BaseHandler):
    """
    产品基本操作：增删改查（CRUD）
    """

    @myweb.authenticated
    @gen.coroutine
    def post(self, cid, pid):
        passport = self.request.headers.get('x-signed-passport')
        access_token = self.request.headers.get('x-access-token')

        data = json.loads(self.request.body.decode('utf-8'))
        if 'name' not in data:
            raise ErrException(ERROR.E40000, extra='not name field')

        ret = yield ctrl_product.create(cid, data, passport, access_token)
        return self.write(ret)

    @myweb.authenticated
    @gen.coroutine
    def get(self, cid, pid):
        passport = self.request.headers.get('x-signed-passport')
        access_token = self.request.headers.get('x-access-token')

        ret = yield ctrl_product.read(cid, pid, passport, access_token)
        return self.write(ret)

    @myweb.authenticated
    @gen.coroutine
    def put(self, cid, pid):
        passport = self.request.headers.get('x-signed-passport')
        access_token = self.request.headers.get('x-access-token')

        data = json.loads(self.request.body.decode('utf-8'))
        ret = yield ctrl_product.update(cid, pid, data, passport, access_token)
        return self.write(ret)

    @myweb.authenticated
    @gen.coroutine
    def delete(self, cid, pid):
        passport = self.request.headers.get('x-signed-passport')
        access_token = self.request.headers.get('x-access-token')

        ret = yield ctrl_product.change_status(cid, pid, 'remove', passport, access_token)
        return self.write(ret)


class StatusHandler(base_handler.BaseHandler):
    """
    产品状态操作，只存在更新操作
    """

    @myweb.authenticated
    @gen.coroutine
    def put(self, cid, pid, action):
        passport = self.request.headers.get('x-signed-passport')
        access_token = self.request.headers.get('x-access-token')

        ret = yield ctrl_product.change_status(cid, pid, action, passport, access_token)
        return self.write(ret)


class MovingHandler(base_handler.BaseHandler):
    """
    将产品从一个分类中已到另一分类中
    """

    @myweb.authenticated
    @gen.coroutine
    def put(self, cid, pid, cid_to):
        passport = self.request.headers.get('x-signed-passport')
        access_token = self.request.headers.get('x-access-token')

        ret = yield ctrl_product.move(cid, pid, cid_to, passport, access_token)
        return self.write(ret)


class ListHandler(base_handler.BaseHandler):
    """
    查询目录下的产品列表
    """

    # 读取产品列表为公开接口
    # @myweb.authenticated
    @gen.coroutine
    def get(self, cid):
        passport = self.request.headers.get('x-signed-passport')
        access_token = self.request.headers.get('x-access-token')

        ret = yield ctrl_product.query_products(cid, passport, access_token)
        return self.write({'list': ret})
