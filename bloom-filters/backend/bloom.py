import hashlib

class BloomFilter:
    def __init__(self, size, hash_count):
        self.size = size  # Size of the bit array
        self.hash_count = hash_count  # Number of hash functions
        self.bit_array = [0] * size
    
    def _hashes(self, item):
        """Generate 'hash_count' hashes for the item using different hash functions."""
        hashes = []
        for i in range(self.hash_count):
            # Create a unique hash for each iteration
            hash_result = int(hashlib.md5((str(item) + str(i)).encode()).hexdigest(), 16) % self.size
            hashes.append(hash_result)
        return hashes

    def add(self, item):
        """Add an item to the Bloom filter."""
        for hash_value in self._hashes(item):
            self.bit_array[hash_value] = 1

    def check(self, item):
        """Check if an item is possibly in the Bloom filter."""
        return all(self.bit_array[hash_value] == 1 for hash_value in self._hashes(item))
