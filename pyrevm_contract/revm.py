from pyrevm import *


class Revm:
    _instance = None

    def __new__(cls, fork_url="", block_number=0, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Revm, cls).__new__(cls)
            cls._instance.revm = EVM(
                fork_url=fork_url,
                tracing=False,
                fork_block_number=block_number,
            )
        return cls._instance

    def __init__(self, fork_url="", block_number=0):
        pass

    def call_raw(self, *args, **kwargs):
        return self.revm.call_raw(*args, **kwargs)

    def call_raw_committing(self, *args, **kwargs):
        return self.revm.call_raw_committing(*args, **kwargs)

    def get_balance(self, address):
        return self.revm.get_balance(address)
