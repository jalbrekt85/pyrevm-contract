import json
import unittest

from pyrevm_contract import Contract, Revm, ABIFunction, ContractABI


class TestContract(unittest.TestCase):
    def setUp(self):
        with open("tests/abi/vault.json", "r") as file:
            vault_abi = json.load(file)

        self.caller = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
        self.vault_addr = "0xBA12222222228d8Ba445958a75a0704d566BF2C8"
        self.weth_addr = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
        self.bal_addr = "0xba100000625a3754423978a60c9317c58a424e3D"
        self.pool_id = (
            "0x5c6ee304399dbdb9c8ef030ab642b10820db8f56000200000000000000000014"
        )

        Revm("https://eth.llamarpc.com", 18000000)
        self.vault = Contract(self.vault_addr, vault_abi)

    def test_init(self):
        self.assertEqual(
            self.vault.address, "0xBA12222222228d8Ba445958a75a0704d566BF2C8"
        )
        self.assertEqual(len(self.vault.abi.functions), 1)
        batch_swap = self.vault.abi.functions[0]
        self.assertEqual(batch_swap.name, "queryBatchSwap")
        self.assertEqual(
            batch_swap.inputs,
            [
                "uint8",
                "(bytes32,uint256,uint256,uint256,bytes)[]",
                "address[]",
                "(address,bool,address,bool)",
            ],
        )
        self.assertEqual(batch_swap.outputs, ["int256[]"])

    def test_query_batch_swap(self):
        swap_kind = 0
        asset_in_index = 0
        asset_out_index = 1
        amt = int(1e18)
        underlyings = [self.weth_addr, self.bal_addr]
        swap = [
            (
                bytes.fromhex(self.pool_id[2:]),
                asset_in_index,
                asset_out_index,
                amt,
                b"",
            )
        ]
        funds = (
            self.caller,
            False,
            self.caller,
            False,
        )
        (weth_amt, bal_amt) = self.vault.queryBatchSwap(
            swap_kind, swap, underlyings, funds, caller=self.caller
        )

        self.assertIsInstance(weth_amt, int)
        self.assertIsInstance(bal_amt, int)
        
    def test_manual_abi(self):
        funcs = [
            ABIFunction(
                "balanceOf",
                ["address"],
                ["uint256"],
                True,
                False,
            ),
            ABIFunction(
                "deposit",
                [],
                [],
                False,
                True
            )
        ]
        
        weth = Contract(
            self.weth_addr,
            contract_abi=ContractABI(funcs),
            caller=self.caller
        )

        weth_before = weth.balanceOf(self.caller)
        weth.deposit(value=1)
        self.assertEqual(weth.balanceOf(self.caller), weth_before + 1)
    
    def test_call_by_identifier(self):
        funcs = [
            ABIFunction(
                "balanceOf",
                ["address"],
                ["uint256"],
                True,
                False,
            ),
            ABIFunction(
                "deposit",
                [],
                [],
                False,
                True
            )
        ]
        
        weth = Contract(
            self.weth_addr,
            contract_abi=ContractABI(funcs),
            caller=self.caller
        )

        weth_before = weth["0x70a08231"](self.caller)
        weth["deposit"](value=1)
        self.assertEqual(weth.balanceOf(self.caller), weth_before + 1)


if __name__ == "__main__":
    unittest.main()
