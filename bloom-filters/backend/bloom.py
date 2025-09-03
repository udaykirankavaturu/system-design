import hashlib
import mmh3
import xxhash
import fnvhash

class BloomFilter:
    def __init__(self, size):
        self.size = size
        self.bit_array = [0] * size
        # The number of hash functions is determined by the number of functions in _hashes
        self.hash_count = 4

    def _hashes(self, item):
        """Generate hashes for the item using a set of different hash functions."""
        item_bytes = str(item).encode()

        hashes = [
            int(hashlib.md5(item_bytes).hexdigest(), 16) % self.size,
            mmh3.hash(item_bytes, 0) % self.size,  # Seed 0 for murmur3
            xxhash.xxh32(item_bytes, seed=0).intdigest() % self.size, # Seed 0 for xxhash
            fnvhash.fnv1_32(item_bytes) % self.size
        ]
        return hashes

    def add(self, item):
        """Add an item to the Bloom filter and return the hashes."""
        hashes = self._hashes(item)
        for hash_value in hashes:
            self.bit_array[hash_value] = 1
        return hashes

    def check(self, item):
        """Check if an item is possibly in the Bloom filter and return the hashes."""
        hashes = self._hashes(item)
        possibly_exists = all(self.bit_array[hash_value] == 1 for hash_value in hashes)
        return possibly_exists, hashes
