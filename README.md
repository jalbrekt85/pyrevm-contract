# pyrevm_contract
Minimal Brownie like contract wrapper for Pyrevm

```
pip install pyrevm_contract
```

```py
from pyrevm_contract import Revm, Contract

revm = Revm(rpc_url, block_num)
c = Contract("0x", "abi_file_path", caller="0x")
res = c.contractFunc()
```
