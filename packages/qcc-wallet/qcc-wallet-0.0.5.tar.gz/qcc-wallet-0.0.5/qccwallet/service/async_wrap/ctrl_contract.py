# coding:utf-8

from qccwallet.service import ctrl_contract
from asyncio import get_event_loop


async def query_contracts(cid):
    args = (cid,)
    return await get_event_loop().run_in_executor(None, ctrl_contract.query_contracts, *args)


async def register(cid, data, *auth_args):
    args = (cid, data, *auth_args)
    return await get_event_loop().run_in_executor(None, ctrl_contract.register, *args)


async def unregister(cid, contract_id, *auth_args):
    args = (cid, contract_id, *auth_args)
    return await get_event_loop().run_in_executor(None, ctrl_contract.unregister, *args)


async def read(contract_id, *auth_args):
    args = (contract_id, *auth_args)
    return await get_event_loop().run_in_executor(None, ctrl_contract.read, *args)
