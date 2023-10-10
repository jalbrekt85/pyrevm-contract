# pyrevm_contract
Minimal Brownie like contract wrapper for Pyrevm

```
pip install pyrevm_contract
```

```py
from pyrevm_contract import Revm, Contract

vitalik = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
weth_addr = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
weth_abi_path = ... # abi .json file path

Revm("https://eth.llamarpc.com", 5000000) # revm singleton; sets backend for all contracts
weth = Contract(weth_addr, abi_file_path=weth_abi_path)

weth.balanceOf(vitalik) # -> 0
weth.deposit(value=100, caller=vitalik)
weth.balanceOf(vitalik) # -> 100
```
