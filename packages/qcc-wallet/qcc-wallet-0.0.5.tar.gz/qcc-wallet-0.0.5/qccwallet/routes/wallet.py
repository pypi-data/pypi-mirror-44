# coding=utf-8

import config
from qccwallet.http_handler import wallet_handler as w, contract_handler as c, org_handler

base = '{}/{}/wallet'.format(config.VER, config.PLATFORM)
routes = [
    # 查询组织拥有哪些资源的许可证/通行证，许可范围有多大
    (rf"/{base}/org/([a-f0-9]*)/passports", org_handler.OurPassportsHandler),

    # 查询我的钱包账户列表
    (rf"/{base}/mine", w.MyWalletsHandler),

    # ******************************************************
    # 以下catalog/([a-f0-9]*)的含义是指在哪个区块链下，如eth，btc，eos等等，参数为注册时生成的类型ID
    # ******************************************************

    # *************************
    # 合约相关(注意：主币也是一种合约！)

    # 查询已注册合约列表
    (rf"/{base}/catalog/([a-f0-9]*)/contracts", c.QueryContractsHandler),

    # 向平台注册/注销合约（仅管理员可以使用）
    (rf"/{base}/catalog/([a-f0-9]*)/contract/([a-f0-9]*)", c.ContractHandler),

    # *************************
    # 基础账户/钱包相关

    # 创建/删除新钱包账户，含合约钱包，只是对应的contract_id不同
    (rf"/{base}/contract/([a-f0-9]*)/wallet/([a-f0-9]*)", w.WalletHandler),

    # 查询余额(根据钱包地址)
    (rf"/{base}/contract/([a-f0-9]*)/address/([a-fA-F0-9x]*)/balance", w.BalanceHandler),

    # 执行转账交易
    (rf"/{base}/contract/([a-f0-9]*)/address/([a-fA-F0-9x]*)/transfer", w.TransferHandler),

    # 查询交易详情
    (rf"/{base}/catalog/([a-f0-9]*)/txid/([a-fA-F0-9x]*)", w.TxInfoHandler),
]
