# coding=utf-8

import webmother
from webmother.service.passport import Passport

from qccwallet.db import mongo
from qccwallet import routes

# 在通证中增加对合约域的权限控制能力
lic_domain = 'contract'
max_lic_text = '{}:111111111;;'.format(lic_domain)
Passport.add_profile(lic_domain, {
    'switch': [
        "create",
        "read",
        "update",
        "remove",
        "submit",
        "audit",
        "reject",
        "activate",
        "deactivate"
    ]
})

Passport.add_display({
    'zh': {
        'contract': '合约管理',
        'contract.switch': '权限开关',
        'contract.switch.create': '创建',
        'contract.switch.read': '读取',
        'contract.switch.remove': '移除',
        'contract.switch.submit': '提交',
        'contract.switch.audit': '审核',
        'contract.switch.reject': '驳回',
        'contract.switch.activate': '上架',
        'contract.switch.deactivate': '下架',
    },
    'en': {
        'contract': 'Contract Manage',
        'contract.switch': 'Switches',
        'contract.switch.create': 'Create',
        'contract.switch.read': 'Read',
        'contract.switch.remove': 'Remove',
        'contract.switch.submit': 'Submit',
        'contract.switch.audit': 'Audit',
        'contract.switch.reject': 'Reject',
        'contract.switch.activate': 'Activate',
        'contract.switch.deactivate': 'Deactivate',
    }
})


def init(app):
    # 初始化webmother
    webmother.init(app)

    # 初始化本系统数据库
    mongo.init()

    # 加载路由模块
    app.load_routes(routes)
