from __future__ import annotations

# Python
from datetime import datetime

# Third party
from hashlib import blake2b


class Block:

    def __init__(
        self, data: str, timestamp: datetime = None,
        hash: str = None, nonce: int = 0, prev_block: Block = None
    ):
        self.data = data
        self.timestamp = timestamp
        self.hash = hash
        self.nonce = nonce
        self.prev_block = prev_block


class Blockchain:

    def __init__(self):
        self.blocks: list[Block] = []

        self.max_blocks_count = 10

        self.create_genesis_block()
        self.generate_remaining_blocks()
        self.print_hashs()

    def is_valid_hash(self, hash: str):
        if not hash:
            return False

        return hash.startswith('000')

    def create_genesis_block(self):
        block = Block('first block')
        self.generate_valid_block_hash(block)

    def generate_remaining_blocks(self):
        i = 1
        while len(self.blocks) < self.max_blocks_count:
            i += 1

            last_block = self.blocks[-1]
            block = Block(f'Block {i} - {last_block.hash}', prev_block=last_block)
            self.generate_valid_block_hash(block)

    def generate_valid_block_hash(self, block: Block):
        while not self.is_valid_hash(block.hash):
            block.hash = self.hash(block)
            block.nonce += 1

        block.timestamp = datetime.now()
        self.blocks.append(block)

    def hash(self, block: Block) -> str:
        h = blake2b(key=str(block.nonce).encode())
        h.update(block.data.encode())
        return h.hexdigest()

    def print_hashs(self):
        for block in self.blocks:
            print(f'[{block.nonce}] {block.hash}')


if __name__ == '__main__':
    chain = Blockchain()