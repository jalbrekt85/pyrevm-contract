from pyrevm import *


class Revm:
    _instance = None

    def __new__(cls, fork_url="", block_number="latest", *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Revm, cls).__new__(cls)
            cls._instance.fork_url = fork_url
            cls._instance.block_number = block_number
            cls._instance.revm = EVM(
                fork_url=fork_url,
                tracing=False,
                fork_block=str(block_number),
            )
        return cls._instance

    def __init__(self, fork_url="", block_number=0):
        pass

    def update_fork(self, new_block_number=None, fork_url=None):
        fork_url = fork_url if fork_url else self.fork_url
        self.block_number = new_block_number if new_block_number else self.block_number
        self.revm = EVM(
            fork_url=fork_url,
            tracing=False,
            fork_block=str(new_block_number),
        )

    def message_call(self, *args, **kwargs):
        return self.revm.message_call(*args, **kwargs)

    def get_balance(self, address):
        return self.revm.get_balance(address)

    def set_balance(self, address, value):
        return self.revm.set_balance(address, value)
    
    def transfer(self, sender, receiver, value):
        return self.revm.call_raw_committing(caller=sender, to=receiver, value=value)
