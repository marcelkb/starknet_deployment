
import random
import sys
from typing import Union, List

from loguru import logger
from starknet_py.cairo.felt import decode_shortstring
from starknet_py.contract import Contract
from starknet_py.hash.address import compute_address
from starknet_py.hash.selector import get_selector_from_name
from starknet_py.net.account.account import Account
from starknet_py.net.client_models import Call
from starknet_py.net.full_node_client import FullNodeClient
from starknet_py.net.models import StarknetChainId, Invoke
from starknet_py.net.signer.stark_curve_signer import KeyPair

from config import (
    BRAAVOS_PROXY_CLASS_HASH,
    BRAAVOS_IMPLEMENTATION_CLASS_HASH,
    ARGENTX_PROXY_CLASS_HASH,
    ARGENTX_IMPLEMENTATION_CLASS_HASH,
    ARGENTX_IMPLEMENTATION_CLASS_HASH_NEW, ERC20_ABI,
)

CAIRO_VERSION = 1

class Starknet:

    def __init__(self, private_key: str, type_account: str) -> None:
        self.key_pair = KeyPair.from_private_key(private_key)
        self.client = FullNodeClient(random.choice("https://1rpc.io/starknet"))
        self.address = self._create_account(type_account)
        self.account = Account(
            address=self.address,
            client=self.client,
            key_pair=self.key_pair,
            chain=StarknetChainId.MAINNET,
        )
        self.account.ESTIMATED_FEE_MULTIPLIER = 1.5
        self.explorer = "https://starkscan.co/tx/"

    def _create_account(self, type_account) -> Union[int, None]:
        if type_account == "argent":
            return self._get_argent_address()
        elif type_account == "braavos":
            return self._get_braavos_account()
        else:
            logger.error("Type wallet error! Available values: argent or braavos")
            sys.exit()

    def _get_argent_address(self) -> int:
        if CAIRO_VERSION == 0:
            selector = get_selector_from_name("initialize")

            calldata = [self.key_pair.public_key, 0]

            address = compute_address(
                class_hash=ARGENTX_PROXY_CLASS_HASH,
                constructor_calldata=[ARGENTX_IMPLEMENTATION_CLASS_HASH, selector, len(calldata), *calldata],
                salt=self.key_pair.public_key,
            )

            return address
        else:
            address = compute_address(
                class_hash=ARGENTX_IMPLEMENTATION_CLASS_HASH_NEW,
                constructor_calldata=[self.key_pair.public_key, 0],
                salt=self.key_pair.public_key,
            )

            return address

    def _get_braavos_account(self) -> int:
        selector = get_selector_from_name("initializer")

        calldata = [self.key_pair.public_key]

        address = compute_address(
            class_hash=BRAAVOS_PROXY_CLASS_HASH,
            constructor_calldata=[BRAAVOS_IMPLEMENTATION_CLASS_HASH, selector, len(calldata), *calldata],
            salt=self.key_pair.public_key,
        )

        return address

    def get_contract(self, contract_address: int, abi: Union[dict, None] = None, cairo_version: int = 0):
        if abi is None:
            abi = ERC20_ABI

        contract = Contract(address=contract_address, abi=abi, provider=self.account, cairo_version=cairo_version)

        return contract

    async def get_balance(self, contract_address: int) -> dict:
        contract = self.get_contract(contract_address)

        symbol_data = await contract.functions["symbol"].call()
        symbol = decode_shortstring(symbol_data.symbol)

        decimal = await contract.functions["decimals"].call()

        balance_wei = await contract.functions["balanceOf"].call(self.address)

        balance = balance_wei.balance / 10 ** decimal.decimals

        return {"balance_wei": balance_wei.balance, "balance": balance, "symbol": symbol, "decimal": decimal.decimals}


    async def sign_transaction(self, calls: List[Call]):
        transaction = await self.account.sign_invoke_transaction(
            calls=calls,
            auto_estimate=True,
            nonce=await self.account.get_nonce(),
        )

        return transaction

    async def send_transaction(self, transaction: Invoke):
        transaction_response = await self.account.client.send_transaction(transaction)

        return transaction_response

    async def wait_until_tx_finished(self, tx_hash: int):
        await self.account.client.wait_for_tx(tx_hash, check_interval=10)

        logger.success(f"[{hex(self.address)}] {self.explorer}{hex(tx_hash)} successfully!")