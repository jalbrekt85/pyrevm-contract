from pyrevm import *


from pyrevm import EVM

class Revm:
    _instance = None
    
    @staticmethod
    def _initialize(instance, fork_url, block_number):
        instance.fork_url = fork_url
        instance.block_number = block_number
        instance.revm = EVM(
            fork_url=fork_url,
            tracing=False,
            fork_block=str(block_number),
        )

    def __new__(cls, fork_url="", block_number="latest"):
        if cls._instance is None:
            cls._instance = super(Revm, cls).__new__(cls)
            cls._initialize(cls._instance, fork_url, block_number)
        return cls._instance

    def update_fork(self, new_block_number=None, fork_url=None):
        self.block_number = new_block_number if new_block_number else self.block_number
        self.fork_url = fork_url if fork_url else self.fork_url

        self._initialize(self, self.fork_url, self.block_number)

    def message_call(self, *args, **kwargs):
        return self.revm.message_call(*args, **kwargs)

    def get_balance(self, address):
        return self.revm.get_balance(address)

    def set_balance(self, address, value):
        return self.revm.set_balance(address, value)
    
    def transfer(self, sender, receiver, value):
        return self.revm.message_call(caller=sender, to=receiver, value=value)
