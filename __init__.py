# -*- coding: utf-8 -*-
from trytond.pool import Pool
from webshop import WebShop, BannerCategory, Banner, Article, \
    Website, ArticleCategory, MenuItem
from product import Product
from invoice import Invoice
from sale import Sale, SaleLine
from party import Address
from shipment import ShipmentOut
from tree import Node
from static_file import NereidStaticFile


def register():
    Pool.register(
        WebShop,
        BannerCategory,
        Banner,
        Article,
        Product,
        Invoice,
        Address,
        ShipmentOut,
        Sale,
        SaleLine,
        Website,
        ArticleCategory,
        Node,
        MenuItem,
        NereidStaticFile,
        module='nereid_webshop', type_='model'
    )
