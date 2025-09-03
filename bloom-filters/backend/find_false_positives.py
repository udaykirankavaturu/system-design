import hashlib
import mmh3
import xxhash
import fnvhash
import random
import string

class BloomFilter:
    def __init__(self, size):
        self.size = size
        self.bit_array = [0] * size
        self.hash_count = 4

    def _hashes(self, item):
        item_bytes = str(item).encode()
        hashes = [
            int(hashlib.md5(item_bytes).hexdigest(), 16) % self.size,
            mmh3.hash(item_bytes, 0) % self.size,
            xxhash.xxh32(item_bytes, seed=0).intdigest() % self.size,
            fnvhash.fnv1_32(item_bytes) % self.size
        ]
        return hashes

    def add(self, item):
        for hash_value in self._hashes(item):
            self.bit_array[hash_value] = 1

    def check(self, item):
        return all(self.bit_array[hash_value] == 1 for hash_value in self._hashes(item))

def find_false_positives():
    # Generate a list of random words
    words = [''.join(random.choices(string.ascii_lowercase, k=5)) for _ in range(500)]
    
    items_to_add = words[:10]  # Add the first 10 words
    items_to_check = words[10:] # Check against the rest

    bf = BloomFilter(size=100)

    for item in items_to_add:
        bf.add(item)

    false_positives = []
    for item in items_to_check:
        if bf.check(item):
            false_positives.append(item)

    print("--- Items to Add ---")
    for item in items_to_add:
        print(item)

    print("\n--- Potential False Positives ---")
    if false_positives:
        # Show the first couple of false positives found
        for fp in false_positives[:2]:
            print(fp)
    else:
        print("No false positives found with this random set. Try running the script again.")

if __name__ == "__main__":
    find_false_positives()
