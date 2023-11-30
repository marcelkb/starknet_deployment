from loguru import logger
from config import DEPLOYER_BYTECODE, DEPLOYER_CASM
from starknet_py.contract import Contract
from starknet import Starknet


class Deployer(Starknet):
    def __init__(self, private_key: str, type_account: str) -> None:
        super().__init__(private_key=private_key, type_account=type_account)

    async def deploy_contract(self):
        logger.info(f"[{self.address}] Deploy contract")

        # To declare through Contract class you have to compile a contract and pass it to the Contract.declare
        declare_result = await Contract.declare(
            account=self.account, compiled_contract=DEPLOYER_BYTECODE,
            compiled_contract_casm=DEPLOYER_CASM, max_fee=int(1e14) #0.0001 ETH evt. 1e15

        )

        # Wait for the transaction
        await declare_result.wait_for_acceptance()

        # After contract is declared it can be deployed
        deploy_result = await declare_result.deploy(max_fee=int(1e14)) #0.0001 ETH evt. 1e15
        await deploy_result.wait_for_acceptance()

        # You can pass more arguments to the `deploy` method. Check `API` section to learn more

        # To interact with just deployed contract get its instance from the deploy_result
        contract = deploy_result.deployed_contract

        logger.success(f"[{self.address}] successfully deployed contract at {contract.address}")