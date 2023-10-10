# pyrevm_contract
Minimal Brownie like contract wrapper for Pyrevm

```
pip install pyrevm_contract
```

```py
from pyrevm_contract import Revm, Contract

caller = "0x0000000000000000000000000000002100000000"
weth_addr = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
weth_abi_path = ... # abi .json file path

Revm("https://eth.llamarpc.com", 5000000) # revm singleton; sets backend for all contracts
weth = Contract(weth_addr, abi_file_path=weth_abi_path)

weth.balanceOf(caller) # -> 0
weth.deposit(value=100, caller=caller)
weth.balanceOf(caller) # -> 100
```
