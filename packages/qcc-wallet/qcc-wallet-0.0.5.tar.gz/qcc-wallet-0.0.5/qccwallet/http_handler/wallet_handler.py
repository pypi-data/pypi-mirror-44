# coding=utf-8

from tweb import base_handler, myweb
from tornado import gen
import json
from qccwallet.service.async_wrap import ctrl_wallet


class MyWalletsHandler(base_handler.BaseHandler):

    @myweb.authenticated
    @gen.coroutine
    def get(self):
        user_id = self.request.headers.get('x-user-id')
        access_token = self.request.headers.get('x-access-token')

        ret = yield ctrl_wallet.query_mine(user_id, access_token)
        return self.write({'list': ret})


class WalletHandler(base_handler.BaseHandler):
    """
    钱包账户操作
    """

    @myweb.authenticated
    @gen.coroutine
    def post(self, contract_id, wallet_id):
        user_id = self.request.headers.get('x-user-id')
        access_token = self.request.headers.get('x-access-token')

        data = json.loads(self.request.body.decode('utf-8'))
        ret = yield ctrl_wallet.create(contract_id, data, user_id, access_token)
        return self.write(ret)

    @myweb.authenticated
    @gen.coroutine
    def delete(self, contract_id, wallet_id):
        user_id = self.request.headers.get('x-user-id')
        access_token = self.request.headers.get('x-access-token')

        ret = yield ctrl_wallet.remove(contract_id, wallet_id, user_id, access_token)
        return self.write(ret)


class BalanceHandler(base_handler.BaseHandler):
    """
    钱包余额
    """

    @myweb.authenticated
    @gen.coroutine
    def get(self, contract_id, address):
        ret = yield ctrl_wallet.balance(contract_id, address)
        return self.write(ret)


class TransferHandler(base_handler.BaseHandler):
    """
    交易转账（含合约交易）
    """

    @myweb.authenticated
    @gen.coroutine
    def post(self, contract_id, from_address):
        user_id = self.request.headers.get('x-user-id')
        access_token = self.request.headers.get('x-access-token')

        data = json.loads(self.request.body.decode('utf-8'))
        ret = yield ctrl_wallet.transfer(contract_id, from_address, data, user_id, access_token)
        return self.write(ret)


class TxInfoHandler(base_handler.BaseHandler):
    """
    获取交易详情（含合约交易）
    """

    @myweb.authenticated
    @gen.coroutine
    def get(self, cid, tx_hash):
        user_id = self.request.headers.get('x-user-id')
        access_token = self.request.headers.get('x-access-token')

        ret = yield ctrl_wallet.get_tx_info(cid, tx_hash, user_id, access_token)
        return self.write(ret)
