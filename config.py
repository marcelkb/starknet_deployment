import json

with open('abi/erc20_abi.json') as file:
    ERC20_ABI = json.load(file)

with open("deploy/contract/counter.json", "r") as file:
    DEPLOYER_BYTECODE = file.read()

with open("deploy/contract/counter.casm", "r") as file:
    DEPLOYER_CASM = file.read()

BRAAVOS_PROXY_CLASS_HASH = 0x03131fa018d520a037686ce3efddeab8f28895662f019ca3ca18a626650f7d1e
BRAAVOS_IMPLEMENTATION_CLASS_HASH = 0x5aa23d5bb71ddaa783da7ea79d405315bafa7cf0387a74f4593578c3e9e6570
BRAAVOS_IMPLEMENTATION_CLASS_HASH_NEW = 0x5dec330eebf36c8672b60db4a718d44762d3ae6d1333e553197acb47ee5a062

ARGENTX_PROXY_CLASS_HASH = 0x025EC026985A3BF9D0CC1FE17326B245DFDC3FF89B8FDE106542A3EA56C5A918
ARGENTX_IMPLEMENTATION_CLASS_HASH = 0x33434AD846CDD5F23EB73FF09FE6FDDD568284A0FB7D1BE20EE482F044DABE2
ARGENTX_IMPLEMENTATION_CLASS_HASH_NEW = 0x01a736d6ed154502257f02b1ccdf4d9d1089f80811cd6acad48e6b6a9d1f2003
