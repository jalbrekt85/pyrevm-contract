# pyrevm_contract
Minimal Brownie like contract wrapper for Pyrevm

```
pip install pyrevm_contract
```

#### init revm

```py
from pyrevm_contract import Revm, Contract

revm = Revm("https://eth.llamarpc.com", block_number=5282490) # revm singleton; sets backend for all contracts

caller = "0x00000000000000000000000000000000000021E8"
weth_addr = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
```

#### init contract via json file object

```py
weth_abi_path = ...
with open(weth_abi_path) as f:
    abi = json.load(f)

weth = Contract(weth_addr, abi)
```

#### init contract via json abi file path

```py
weth_abi_path = ...
weth = Contract(weth_addr, abi_file_path=weth_abi_path)
```

#### create contract abi manually

```py
from pyrevm_contract import ABIFunction, ContractABI
funcs = [
    ABIFunction(
        name="balanceOf",
        inputs=["address"],
        outputs=["uint256"],
        constant=True,
        payable=False,
    ),
    ABIFunction(
        selector="0xd0e30db0" # support for selector based funcs
        inputs=[],
        outputs=[],
        constant=False,
        payable=True
    )
]

weth = Contract(
    weth_addr,
    contract_abi=ContractABI(funcs),
)
```

#### call contract

```py
revm.set_balance(caller, 100) # revm cheatcode; sets ether balance of acct

weth.balanceOf(caller) # -> 0
weth["0xd0e30db0"](value=100, caller=caller) # call via selector
weth.balanceOf(caller) # -> 100
```
