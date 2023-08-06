# coding=utf-8

import config
from web3 import Web3
import json
from hexbytes import HexBytes
from tweb.error_exception import ErrException, ERROR

provider = Web3.HTTPProvider(config.Ethereum['external']['http'], request_kwargs={'timeout': 60})

web3 = Web3(provider)


def wallet_balance(address):
    address = web3.toChecksumAddress(address)
    ret = web3.eth.getBalance(address)
    return str(ret)


def get_tx_count(address):
    address = web3.toChecksumAddress(address)
    return web3.eth.getTransactionCount(address)


def get_gas_price():
    return web3.eth.gasPrice


def send_raw_tx(raw_transaction):
    result = web3.eth.sendRawTransaction(raw_transaction)
    tx_hash = web3.toHex(result)
    return tx_hash


def create_tx(from_address, to_address, value):
    from_address = web3.toChecksumAddress(from_address)
    to_address = web3.toChecksumAddress(to_address)

    nonce = get_tx_count(from_address)
    gas_price = get_gas_price()

    transaction = {
        'from': from_address,
        'to': to_address,
        'value': value,
        'gasPrice': gas_price,
        # 'data': "",
        'nonce': nonce,
        # 'chainId': 5
    }

    gas = web3.eth.estimateGas(transaction)
    transaction['gas'] = gas

    return transaction


def get_tx(tx_hash):
    tx = web3.eth.getTransaction(tx_hash)
    json_str = json.dumps(dict(tx), cls=HexJsonEncoder)
    ret = json.loads(json_str)
    return ret


# 合约调用相关


def contract_call(contract_json, method, args=None):
    contract_address = web3.toChecksumAddress(contract_json['spec']['address'])
    abi = contract_json['spec']['data']
    contract = web3.eth.contract(contract_address, abi=abi)

    if args is None:
        args = []

    temp = list()
    for i, val in enumerate(args):
        if web3.isAddress(val):
            temp.append(web3.toChecksumAddress(val))
        else:
            temp.append(val)

    ret = contract.functions[method](*tuple(temp)).call()
    if isinstance(ret, int):
        ret = str(ret)

    return ret


def contract_create_tx(contract_json, method, args, tx_param):

    contract_address = web3.toChecksumAddress(contract_json['spec']['address'])
    abi = contract_json['spec']['data']

    contract = web3.eth.contract(contract_address, abi=abi)

    temp = list()
    for i, val in enumerate(args):
        if web3.isAddress(val):
            temp.append(web3.toChecksumAddress(val))
        else:
            temp.append(val)

    try:
        transaction = contract.functions[method](*tuple(temp)).buildTransaction(tx_param)
    except Exception as e:
        raise ErrException(ERROR.E50000, extra='%s' % e)

    gas = web3.eth.estimateGas(transaction)
    transaction['gas'] = gas

    return transaction


# 其他辅助工具
class HexJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, HexBytes):
            return obj.hex()
        return super().default(obj)
