# coding=utf-8

import config
from qccproduct.http_handler import product_handler, org_handler

base = '{}/{}/product'.format(config.VER, config.PLATFORM)
routes = [
    # 查询组织拥有哪些资源的许可证/通行证，许可范围有多大
    (rf"/{base}/org/([a-f0-9]*)/passports", org_handler.OurPassportsHandler),

    # 产品的增删改查
    (rf"/{base}/catalog/([a-f0-9]*)/product/([a-f0-9]*)", product_handler.ProductHandler),

    # 产品的状态操作
    (rf"/{base}/catalog/([a-f0-9]*)/product/([a-f0-9]*)/do/(\w*)", product_handler.StatusHandler),

    # 将产品从一个分类中已到另一分类中
    (rf"/{base}/catalog/([a-f0-9]*)/product/([a-f0-9]*)/move/(\w*)", product_handler.MovingHandler),

    # 查询分类节点下的产品列表
    (rf"/{base}/catalog/([a-f0-9]*)/list", product_handler.ListHandler),
]
