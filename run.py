from deploy import Deployer
TYPE = "braavos" # or "argent"
KEY = "PRIVATE_KEY" # the private key of the wallet

deployer = Deployer(TYPE, KEY)
deployer.deploy_contract()
