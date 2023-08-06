# coding:utf-8

from qccwallet.service import ctrl_wallet
from asyncio import get_event_loop


async def query_mine(*auth_args):
    args = auth_args
    return await get_event_loop().run_in_executor(None, ctrl_wallet.query_mine, *args)


async def create(contract_id, data, *auth_args):
    args = (contract_id, data, *auth_args)
    return await get_event_loop().run_in_executor(None, ctrl_wallet.create, *args)


async def remove(contract_id, wallet_id, *auth_args):
    args = (contract_id, wallet_id, *auth_args)
    return await get_event_loop().run_in_executor(None, ctrl_wallet.remove, *args)


async def balance(contract_id, address):
    args = contract_id, address
    return await get_event_loop().run_in_executor(None, ctrl_wallet.balance, *args)


async def transfer(contract_id, from_address, data, *auth_args):
    args = contract_id, from_address, data, *auth_args
    return await get_event_loop().run_in_executor(None, ctrl_wallet.transfer, *args)


async def get_tx_info(cid, tx_hash, *auth_args):
    args = cid, tx_hash, *auth_args
    return await get_event_loop().run_in_executor(None, ctrl_wallet.get_tx_info, *args)
