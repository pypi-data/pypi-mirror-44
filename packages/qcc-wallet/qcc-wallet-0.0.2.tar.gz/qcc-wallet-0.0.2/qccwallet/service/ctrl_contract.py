# coding:utf-8

from qccwallet.db import mongo as db
from tweb.error_exception import ErrException, ERROR
from tweb import time
from webmother.service import ctrl_catalog
from webmother.service.passport import Passport
from bson.objectid import ObjectId
from qccwallet.service.internal import ethereum as in_ethereum


def query_contracts(cid, *auth_args):
    """
    查询某区块链下已注册的合约列表
    :param cid: 区块链标示，即分类ID
    """
    cursor = db.contract.find({'catalog': ObjectId(cid), 'status': {'$gte': 0}}, {'catalog': 0})
    array = list()
    for item in cursor:
        item['contract_id'] = item.pop('_id').__str__()
        array.append(item)
    return array


def register(cid, data, *auth_args):
    c = ctrl_catalog.simple_read(cid)

    # 授权检查
    Passport().verify(*auth_args).operable('{}/contracts'.format(c.get('node')), 'contract.create')
    # END

    name = data['name']
    symbol = data['symbol']
    t = data['type']
    decimals = data['decimals']

    supported = ['main', 'ERC20']
    if t not in supported:
        raise ErrException(ERROR.E40000, extra='only support type of %s' % supported)

    now = time.millisecond()
    w = {
        "catalog": ObjectId(cid),
        "name": name,
        "symbol": symbol,
        "decimals": decimals,
        "type": t,
        "status": 10,
        "created": now,
        "updated": now
    }
    if 'icon' in data:
        w['icon'] = data['icon']
    if t != 'main':
        # 是合约，则增加合约spec
        spec = data['spec']
        if spec is None:
            raise ErrException(ERROR.E40000, extra='no spec field')
        contract_address = spec.get('address')
        if not in_ethereum.is_address(contract_address):
            raise ErrException(ERROR.E40000, extra='invalid contract address')

        chain_name = c['name']
        if chain_name == 'eth':
            abi = spec.get('data')
            if abi is None:
                raise ErrException(ERROR.E40000, extra='need abi for eth')
            # 校验是否为合法合约参数
            if not in_ethereum.get_contract(contract_address, abi):
                raise ErrException(ERROR.E40000, extra='wrong contract params')

        w['spec'] = {
            'address': contract_address,
            'data': spec.get('data')
        }

        # 保证合约地址不重复
        existed = db.contract.find_one({'spec.address': contract_address, 'status': {'$gte': 0}})
        if existed is not None:
            raise ErrException(ERROR.E40020, extra='existed about the contract address: %s' % contract_address)
        # 保证name不重复
        existed = db.contract.find_one({'name': name, 'status': {'$gte': 0}})
        if existed is not None:
            raise ErrException(ERROR.E40020, extra='existed about the name: %s' % name)
        # 保证symbol不重复
        existed = db.contract.find_one({'symbol': symbol, 'status': {'$gte': 0}})
        if existed is not None:
            raise ErrException(ERROR.E40020, extra='existed about the symbol: %s' % symbol)

    else:
        existed = db.contract.find_one({'catalog': ObjectId(cid), 'type': t, 'status': {'$gte': 0}},
                                       {'catalog': 0})
        if existed is not None:
            existed['contract_id'] = existed.pop('_id').__str__()
            return existed

    result = db.contract.insert_one(w)
    ret = db.contract.find_one(result.inserted_id, {'catalog': 0})
    ret['contract_id'] = ret.pop('_id').__str__()

    return ret


def unregister(cid, contract_id, *auth_args):
    c = ctrl_catalog.simple_read(cid)

    # 授权检查
    Passport().verify(*auth_args).operable('{}/contracts'.format(c.get('node')), 'contract.remove')
    # END

    db.contract.update_one({'_id': ObjectId(contract_id)}, {'$set': {'status': -10}})

    return {}


def read(contract_id):
    ret = db.contract.find_one({'_id': ObjectId(contract_id)})
    if ret is None:
        raise ErrException(ERROR.E40400, extra='eth contract not registered: %s' % contract_id)

    ret['contract_id'] = ret.pop('_id').__str__()
    ret['catalog'] = ctrl_catalog.simple_read(ret['catalog'].__str__())

    return ret
