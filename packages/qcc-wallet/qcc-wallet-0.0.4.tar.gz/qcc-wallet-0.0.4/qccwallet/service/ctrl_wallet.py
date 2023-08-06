# coding:utf-8

from qccwallet.db import mongo as db
from tweb.error_exception import ErrException, ERROR
from tweb import time
from bson.objectid import ObjectId
import re
from qccwallet.service import ctrl_contract
from webmother.service import ctrl_catalog
from qccwallet.service.internal import ethereum as in_ethereum
from qccwallet.service.external import ethereum as ex_ethereum
from qccwallet.utils import secret


def query_mine(*auth_args):
    uid = auth_args[0]

    cursor = db.wallet.find({'uid': ObjectId(uid), 'status': {'$gte': 0}}, {'uid': 0, 'catalog': 0})

    array = list()
    for item in cursor:
        item['wallet_id'] = item.pop('_id').__str__()
        item['contract'] = ctrl_contract.read(item.pop('contract_id').__str__())
        array.append(item)

    return array


def create(contract_id, data, *auth_args):
    password = secret.verify_msg(data)
    uid = auth_args[0]

    now = time.millisecond()
    w = {
        "uid": ObjectId(uid),
        "contract_id": ObjectId(contract_id),
        "status": 10,
        "created": now,
        "updated": now
    }

    if 'alias' in data:
        w['alias'] = data['alias']
    if 'mark' in data:
        w['mark'] = data['mark']

    contract = ctrl_contract.read(contract_id)
    cid = contract['catalog']['cid']
    w['catalog'] = ObjectId(cid)

    t = contract['type']
    w['type'] = t

    if t == 'main':
        # 保证只有一个主币账户
        existed = db.wallet.find_one({'uid': ObjectId(uid), 'catalog': ObjectId(cid), 'status': {'$gte': 0}},
                                     {'uid': 0, 'catalog': 0})
        if existed is not None:
            existed['wallet_id'] = existed.pop('_id').__str__()
            existed['contract'] = ctrl_contract.read(existed.pop('contract_id').__str__())
            return existed

        if not re.match(r'^.{6,20}$', password):
            raise ErrException(ERROR.E40000, extra='password should be 6-20 characters')

        chain_name = contract['catalog']['name']
        if chain_name == 'eth':
            w['address'] = in_ethereum.new_account(password)
        else:
            raise ErrException(ERROR.E40000, extra='invalid block-chain: %s' % chain_name)
    else:
        existed = db.wallet.find_one(
            {'uid': ObjectId(uid), 'contract_id': ObjectId(contract_id), 'status': {'$gte': 0}},
            {'uid': 0, 'catalog': 0})
        if existed is not None:
            existed['wallet_id'] = existed.pop('_id').__str__()
            existed['contract'] = ctrl_contract.read(existed.pop('contract_id').__str__())
            return existed

        # 保证已经存在主币账户
        tmp = db.wallet.find_one({'uid': ObjectId(uid), 'catalog': ObjectId(cid), 'status': {'$gte': 0}},
                                 {'address': 1})
        if tmp is None:
            raise ErrException(ERROR.E40000, extra='please create main account first')

        w['address'] = tmp['address']

    result = db.wallet.insert_one(w)
    ret = db.wallet.find_one(result.inserted_id, {'uid': 0, 'catalog': 0})
    ret['wallet_id'] = ret.pop('_id').__str__()
    ret['contract'] = ctrl_contract.read(ret.pop('contract_id').__str__())

    return ret


def remove(contract_id, wallet_id, *auth_args):
    uid = auth_args[0]

    contract = ctrl_contract.read(contract_id)

    t = contract['type']
    if t == 'main':
        # 主币钱包涉及私钥等重要信息，故只做逻辑删除。同时将关联的合约账户全部删除

        existed = db.wallet.find_one({'_id': ObjectId(wallet_id),
                                      'uid': ObjectId(uid),
                                      'contract_id': ObjectId(contract_id),
                                      'status': {'$gte': 0}
                                      })
        if existed is None:
            raise ErrException(ERROR.E40400)

        address = existed['address']

        db.wallet.update_one({'_id': ObjectId(wallet_id),
                              'uid': ObjectId(uid),
                              'contract_id': ObjectId(contract_id)
                              },
                             {'$set': {'status': -10}})

        cursor = db.wallet.find({'address': address.lower(), 'uid': ObjectId(uid), 'status': {'$gte': 0}})
        for item in cursor:
            db.wallet.delete_one({'_id': item['_id']})
    else:
        # 合约账户实际是一种方便查看管理的绑定关系，故直接删除

        db.wallet.delete_one({'_id': ObjectId(wallet_id), 'uid': ObjectId(uid), 'contract_id': ObjectId(contract_id)})

    return {}


def balance(contract_id, address):
    contract = ctrl_contract.read(contract_id)

    ret = {'decimals': contract['decimals']}

    chain_name = contract['catalog']['name']
    t = contract['type']
    if chain_name == 'eth':
        if t == 'main':
            ret['balance'] = ex_ethereum.wallet_balance(address)
        elif t == 'ERC20':
            ret['balance'] = ex_ethereum.contract_call(contract, 'balanceOf', [address])
        else:
            raise ErrException(ERROR.E40000, extra='invalid contract type: %s' % t)
    else:
        raise ErrException(ERROR.E40000, extra='invalid block-chain: %s' % chain_name)

    return ret


def estimate_transfer_fei(contract_id, from_address, data):
    secret.verify_msg(data)

    to_address = data.get('to')
    if 'to_address' is None:
        raise ErrException(ERROR.E40000, extra='not to field')

    value = int(data.get('value'))
    if value is None:
        raise ErrException(ERROR.E40000, extra='not value field')

    contract = ctrl_contract.read(contract_id)

    t = contract['type']
    chain_name = contract['catalog']['name']

    if chain_name == 'eth':
        if t == 'main':
            tx = ex_ethereum.create_tx(from_address, to_address, value)
        elif t == 'ERC20':
            gas_price = ex_ethereum.get_gas_price()
            to_address = in_ethereum.to_crc_address(to_address)
            tx = ex_ethereum.contract_create_tx(contract, 'transfer', [to_address, value], {
                'from': in_ethereum.to_crc_address(from_address),
                'gasPrice': gas_price
            })
        else:
            raise ErrException(ERROR.E40000, extra='invalid contract type: %s' % t)

        return {
            'chain': 'eth',
            'miner_fei': tx['gas'] * tx['gasPrice']
        }
    else:
        raise ErrException(ERROR.E40000, extra='invalid block-chain: %s' % chain_name)


def transfer(contract_id, from_address, data, *auth_args):
    password = secret.verify_msg(data)
    if len(auth_args) > 0:
        uid = auth_args[0]

    to_address = data.get('to')
    if 'to_address' is None:
        raise ErrException(ERROR.E40000, extra='not to field')
    value = int(data.get('value'))
    if value is None:
        raise ErrException(ERROR.E40000, extra='not value field')

    contract = ctrl_contract.read(contract_id)

    t = contract['type']
    cid = contract['catalog']['cid']
    chain_name = contract['catalog']['name']

    if len(auth_args) > 0:
        # from_address必须是用户的主币地址，且为正常状态
        ret = db.wallet.find_one({'uid': ObjectId(uid), 'address': from_address.lower(), 'type': 'main', 'status': 10})
        if ret is None:
            raise ErrException(ERROR.E40400, extra='invalid from_address, maybe not belong to you')

    if chain_name == 'eth':
        if t == 'main':
            tx = ex_ethereum.create_tx(from_address, to_address, value)
            signed = in_ethereum.sign_tx(from_address, tx, password)
            tx_hash = ex_ethereum.send_raw_tx(signed['rawTransaction'])

            return get_tx_info(cid, tx_hash)
        elif t == 'ERC20':
            nonce = ex_ethereum.get_tx_count(from_address)
            gas_price = ex_ethereum.get_gas_price()
            to_address = in_ethereum.to_crc_address(to_address)
            tx = ex_ethereum.contract_create_tx(contract, 'transfer', [to_address, value], {
                'from': in_ethereum.to_crc_address(from_address),
                'gasPrice': gas_price,
                'nonce': nonce
            })

            signed = in_ethereum.sign_tx(from_address, tx, password)
            tx_hash = ex_ethereum.send_raw_tx(signed['rawTransaction'])
            return get_tx_info(cid, tx_hash)
        else:
            raise ErrException(ERROR.E40000, extra='invalid contract type: %s' % t)
    else:
        raise ErrException(ERROR.E40000, extra='invalid block-chain: %s' % chain_name)


def get_tx_info(cid, tx_hash, *auth_args):
    c = ctrl_catalog.simple_read(cid)
    chain_name = c['name']

    if chain_name == 'eth':
        tx = ex_ethereum.get_tx(tx_hash)

        ret = {
            'hash': tx.pop('hash'),
            'blockHash': tx.pop('blockHash'),
            'blockNumber': tx.pop('blockNumber'),
            'gas': tx.pop('gas'),
            'gasPrice': tx.pop('gasPrice'),
            'nonce': tx.pop('nonce'),
            'from': tx.pop('from')
        }

        if tx['input'] == '0x':
            cnt = db.contract.find_one({'catalog': ObjectId(cid), 'type': 'main'})
            ret['contract_id'] = cnt['_id'].__str__()
            ret['type'] = cnt['type']
            ret['symbol'] = cnt['symbol']
            ret['to'] = tx.pop('to')
            ret['value'] = tx.pop('value')
        else:
            # 此交易是合约交易
            contract_address = tx['to']
            cnt = db.contract.find_one({'spec.address': contract_address})
            if cnt is None:
                raise ErrException(ERROR.E50000, extra='unknown contract address: %s' % contract_address)
            contract = in_ethereum.get_contract(contract_address, cnt['spec']['data'])
            temp = contract.decode_function_input(tx['input'])
            tx['contract'] = {
                'method': temp[0].fn_name,
                'params': temp[1]
            }

            ret['contract_id'] = cnt['_id'].__str__()
            ret['type'] = cnt['type']
            if ret['type'] == 'ERC20':
                ret['symbol'] = cnt['symbol']
                if temp[0].fn_name == 'transfer':
                    ret['to'] = temp[1].get('to')
                    ret['value'] = temp[1].get('value')

        ret['extra'] = tx
        return ret
    else:
        raise ErrException(ERROR.E40000, extra='invalid block-chain: %s' % name)


def verify_password(address, password):
    in_ethereum.sign_msg(address, '', password)