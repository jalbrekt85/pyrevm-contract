import json

from .revm import Revm
from .abi import ABIFunction, ContractABI, parse_json_abi


ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"


class Contract:
    def __init__(
        self,
        address: str,
        abi: dict = None,
        abi_file_path: str = None,
        caller: str = ZERO_ADDRESS,
        fork_url="",
        block_number=0,
    ):
        self.address = address
        self.caller = caller

        self.abi = self._load_abi(abi, abi_file_path)
        self.revm = Revm(fork_url=fork_url, block_number=block_number)

    def __getattr__(self, attribute):
        for func in self.abi.functions:
            if func.name == attribute or func.selector == attribute:
                return lambda *args, **kwargs: self.call_function(func, args, kwargs)
        raise AttributeError(f"No function named {attribute} in contract ABI")

    def _load_abi(self, abi: dict = None, file_path: dict = None) -> ContractABI:
        if not abi and not file_path:
            raise ValueError("Either abi or abi_file_path must be provided")

        if file_path:
            with open(file_path, "r") as file:
                abi = json.load(file)

        return parse_json_abi(abi)

    def _decode_output(self, func: ABIFunction, raw_output: bytes) -> any:
        if func.outputs:
            if isinstance(raw_output, str):
                raw_output = bytes.fromhex(
                    raw_output[2:] if raw_output.startswith("0x") else raw_output
                )
            return func.decode_outputs(raw_output)
        return None

    def call_function(self, func: ABIFunction, args: tuple, kwargs: dict = {}):
        value = kwargs.get("value", 0)
        caller = kwargs.get("caller", self.caller)

        calldata = func.encode_inputs(args)

        if func.constant:
            raw_output = self.revm.call_raw(
                caller=caller, to=self.address, data=calldata
            )
            return self._decode_output(func, raw_output)
        else:
            if not func.payable and value > 0:
                raise ValueError("Cannot send value to a non-payable function")

            if caller == ZERO_ADDRESS:
                raise ValueError("Cannot call a non-constant function without a caller")
            raw_output = self.revm.call_raw_committing(
                caller=caller,
                to=self.address,
                data=calldata,
                value=value,
            )
            return self._decode_output(func, raw_output)

    def balance(self):
        return self.revm.get_balance(self.address)
