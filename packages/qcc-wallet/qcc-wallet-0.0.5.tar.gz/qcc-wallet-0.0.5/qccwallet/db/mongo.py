# coding:utf-8

import pymongo
from webmother.db import mongo as mother_db
from tornado.options import options

MongoDB = {
    'active': True,  # 是否启用
    'dev': {
        'host': 'udl.link',
        'port': 27017,
        'db': 'wtdb',
        'user': 'app',
        'pwd': 'Wllt2app'
    },
    'prod': {
        'host': 'udl.link',
        'port': 27017,
        'db': 'wtdb',
        'user': 'app',
        'pwd': 'Wllt2app'
    }
}

# web-mother相关集合
catalog = None

# wallet DB
mongo_client = None
mongo_db = None

wallet = None
contract = None


def init():
    if not MongoDB['active']:
        return

    global catalog

    global mongo_client
    global mongo_db

    global wallet
    global contract

    mongo_cfg = MongoDB[options.env]

    if mongo_client is not None:
        return

    mother_db.init()

    # 引用webmother中的数据集合
    catalog = mother_db.catalog
    # END

    mongo_client = pymongo.MongoClient(host=mongo_cfg['host'],
                                       port=mongo_cfg['port'],
                                       username=mongo_cfg['user'],
                                       password=mongo_cfg['pwd'],
                                       authSource=mongo_cfg['db'])
    mongo_db = mongo_client[mongo_cfg['db']]

    # my collections
    wallet = mongo_db.wallet
    contract = mongo_db.contract
    # END

    # 创建索引
    _wallet_index()
    _contract_index()

    # 初始化系统数据
    _init_data()


def start_session():
    return mongo_client.start_session()


def _wallet_index():
    """
    {
        "_id": ObjectId('5c729df2e155ac16da86a1d0'),
        "uid": ObjectId('5c9c25cae155acde223d5472'),                # 用户ID
        "catalog": ObjectId('5c710622e155ac0c39c8b66d'),            # 所属分类节点ID, 即所属区块链
        "address": '0x58a81beab5f9948114d267ee834d82928accb030',    # 钱包地址
        "contract_id": ObjectId('5c729df2e155ac16da86a1d0'),        # 合约ID，也是币种定义
        "type": "ERC20",     # 币种类型，如：main：主币（本系统将主币也作为一种特殊的合约），ERC20：ERC20币，ERC721：ERC721币
        "alias": '理财钱包',
        "mark": '我不想当韭菜',
        "status": 10,          # -10:已删除，0: 休眠中，10: 活动中
        "created": 1551015331186,
        "updated": 1551015331186
    }
    """
    wallet.create_index('uid')
    wallet.create_index('address')


def _contract_index():
    """
    {
        "_id": ObjectId('5c729df2e155ac16da86a1d0'),
        "catalog": ObjectId('5c710622e155ac0c39c8b66d'), # 所属分类节点ID, 即所属区块链
        "name": 'Simple Token',
        "symbol": 'TST',
        "decimals": 18,       # 有效位长度，即小数位数
        "icon": "https://cdn2.iconfinder.com/data/icons/5/100/cryptocurrency_blockchain_crypto-02-512.png",
        "type": "ERC20",     # 币种类型，如：main：主币（本系统将主币也作为一种特殊的合约），ERC20：ERC20币，ERC721：ERC721币
        "spec": {            # 主币spec为空
            "address": '0x7af963cF6D228E564e2A0aA0DdBF06210B38615D',  # 合约地址
            "data": [...],                                            # 合约相关数据，不同链存在不同的数据
        }
        "status": 10,          # -10:已删除，0: 休眠中，10: 活动中
        "created": 1551015331186,
        "updated": 1551015331186
    }

    本系统将主币也作为一种特殊的合约！！！
    """
    contract.create_index('catalog')
    contract.create_index('spec.address')


def _init_data():
    pass
