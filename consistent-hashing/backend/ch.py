import hashlib
import bisect

class ConsistentHashing:
    def __init__(self, num_replicas=3):
        self.num_replicas = num_replicas
        self.hash_ring = {}
        self._sorted_hashes = []

    def _hash(self, key):
        return int(hashlib.md5(key.encode('utf-8')).hexdigest(), 16)

    def add_node(self, node):
        for i in range(self.num_replicas):
            hash_key = self._hash(f"{node}-{i}")
            self.hash_ring[hash_key] = node
        self._sorted_hashes = sorted(self.hash_ring.keys())

    def remove_node(self, node):
        for i in range(self.num_replicas):
            hash_key = self._hash(f"{node}-{i}")
            if hash_key in self.hash_ring:
                del self.hash_ring[hash_key]
        self._sorted_hashes = sorted(self.hash_ring.keys())

    def get_node(self, key):
        if not self.hash_ring:
            return None
        hash_key = self._hash(key)
        
        # Find the index of the first hash that is >= hash_key
        idx = bisect.bisect_left(self._sorted_hashes, hash_key)
        
        # If the index is out of bounds, it means we need to wrap around to the first node
        if idx == len(self._sorted_hashes):
            idx = 0
            
        return self.hash_ring[self._sorted_hashes[idx]]