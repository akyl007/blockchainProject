import hashlib
import time
import json


def hash(text):
    encoded_text = text.encode('utf-8')
    hashed_value = hashlib.sha256(encoded_text).hexdigest()
    return hashed_value


class MerkleTree:
    def __init__(self, transactions):
        self.transactions = transactions
        self.root = self.build_merkle_root(transactions)

    def build_merkle_root(self, transactions):
        current_level = [hash(tx) for tx in transactions]
        while len(current_level) > 1:
            next_level = []
            for i in range(0, len(current_level), 2):
                left = current_level[i]
                right = current_level[i + 1] if i + 1 < len(current_level) else left
                combined = left + right
                next_level.append(hash(combined))
            current_level = next_level
        return current_level[0] if current_level else None

class Block:
    def __init__(self, previous_hash, transactions):
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.merkle_root = MerkleTree(transactions).root
        self.hash = self.mine_block()
    def mine_block(self):
        block_content = json.dumps({
            'previous_hash': self.previous_hash,
            'timestamp': self.timestamp,
            'merkle_root': self.merkle_root,
        }, sort_keys=True)
        return hash(block_content)

class Blockchain:
    def __init__(self):
        genesis_block = Block("0", ["Genesis Transaction"])
        self.chain = [genesis_block]

    def add_block(self, transactions):
        previous_hash = self.chain[-1].hash
        new_block = Block(previous_hash, transactions)
        self.chain.append(new_block)

    def validate_blockchain(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            if current.previous_hash != previous.hash:
                return False
        return True


def main():
        blockchain = Blockchain()

        while True:
            print("\nBlockchain Console:")
            print("1. Add Transaction")
            print("2. Mine Block")
            print("3. Validate Blockchain")
            print("4. Display Blockchain")
            print("5. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                transaction = input("Enter transaction in the format 'Sender,Receiver,Amount': ")
                blockchain.add_block([transaction])
                print("Transaction added and block mined!")

            elif choice == '2':
                print("Mining block...")
                blockchain.add_block([])
                print("Block mined successfully!")

            elif choice == '3':
                if blockchain.validate_blockchain():
                    print("Blockchain is valid.")
                else:
                    print("Blockchain is invalid!")

            elif choice == '4':
                for i, block in enumerate(blockchain.chain):
                    print(f"\nBlock {i}:")
                    print(f"Timestamp: {block.timestamp}")
                    print(f"Previous Hash: {block.previous_hash}")
                    print(f"Merkle Root: {block.merkle_root}")
                    print(f"Hash: {block.hash}")
                    print(f"Transactions: {block.transactions}")

            elif choice == '5':
                print("Exiting...")
                break

            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
