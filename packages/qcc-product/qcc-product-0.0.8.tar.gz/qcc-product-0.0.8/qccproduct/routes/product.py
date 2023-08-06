# coding=utf-8

import config
from qccproduct.http_handler import product_handler as h

base = '{}/{}/product'.format(config.VER, config.PLATFORM)
routes = [
    # 产品的增删改查
    (rf"/{base}/catalog/([a-f0-9]*)/product/([a-f0-9]*)", h.ProductHandler),

    # 产品的状态操作
    (rf"/{base}/catalog/([a-f0-9]*)/product/([a-f0-9]*)/do/(\w*)", h.StatusHandler),

    # 将产品从一个分类中已到另一分类中
    (rf"/{base}/catalog/([a-f0-9]*)/product/([a-f0-9]*)/move/(\w*)", h.MovingHandler),

    # 查询分类节点下的产品列表
    (rf"/{base}/catalog/([a-f0-9]*)/list", h.ListHandler),
]
