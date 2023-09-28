from typing import List, Optional, Any
from dataclasses import dataclass

from eth_abi import encode, decode
import sha3


@dataclass
class ABIFunction:
    name: Optional[str] = None
    inputs: Optional[List[str]] = None
    possible_inputs: Optional[List[str]] = None
    num_args: Optional[int] = None
    outputs: List[str] = None
    constant: bool = False
    payable: bool = False
    selector: Optional[str] = None
    
    @staticmethod
    def func_selector(sig: str) -> bytes:
        k = sha3.keccak_256()
        k.update(sig.encode('utf-8'))
        return k.digest()[:4]

    def get_selector(self) -> bytes:
        if self.selector:
            return bytes.fromhex(
                self.selector[2:]
                if self.selector.startswith("0x")
                else self.selector
            )
        elif self.name:
            return self.func_selector(self.get_signature())
        else:
            raise ValueError(
                "Cannot compute selector without a name or selector"
            )

    def get_signature(self) -> str:
        if self.name is None:
            raise ValueError("Cannot compute signature without a name")

        input_types = ""
        if self.inputs:
            input_types = ",".join(self.inputs)

        return f"{self.name}({input_types})"

    def encode_inputs(self, values: List[Any]) -> bytes:
        selector = self.get_selector()
        if self.inputs == []:
            return selector
        encoded_inputs = encode(self.inputs, values)
        return selector + encoded_inputs

    def decode_outputs(self, output_data: bytes) -> Any:
        if not output_data:
            return None

        if not self.outputs:
            return []

        try:
            decoded = decode(self.outputs, output_data)
            if len(decoded) == 1:
                return decoded[0]
            return decoded
        except Exception as e:
            raise ValueError(
                "Failed to decode outputs for function"
                f" {self.name or self.selector}: {str(e)}"
            )


@dataclass
class ContractABI:
    functions: List[ABIFunction]
    name: Optional[str] = None
