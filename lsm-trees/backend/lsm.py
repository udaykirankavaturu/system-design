import os
import time
import json
from sortedcontainers import SortedDict
from bloom import BloomFilter

TOMBSTONE = "__TOMBSTONE__"

class MemTable:
    def __init__(self, threshold):
        self.threshold = threshold
        self.data = SortedDict()
        self.wal = open("wal.log", "a")

    def set(self, key, value):
        self.wal.write(json.dumps({"key": key, "value": value}) + "\n")
        self.wal.flush()
        self.data[key] = value
        return len(self.data) >= self.threshold

    def get(self, key):
        return self.data.get(key)

    def clear(self):
        self.data = SortedDict()
        self.wal.close()
        if os.path.exists("wal.log"):
            os.remove("wal.log")
        self.wal = open("wal.log", "a")

class LSMTree:
    def __init__(self, memtable_threshold, compaction_threshold=4):
        self.memtable = MemTable(memtable_threshold)
        self.sstables = []
        self.compaction_threshold = compaction_threshold

    def set(self, key, value):
        if self.memtable.set(key, value):
            self.flush()

    def delete(self, key):
        self.set(key, TOMBSTONE)

    def get(self, key):
        value = self.memtable.get(key)
        if value is not None:
            return value if value != TOMBSTONE else None
        for sstable_path, bf_path in reversed(self.sstables):
            with open(bf_path, 'r') as f:
                bit_array = json.load(f)
            bf = BloomFilter(len(bit_array))
            bf.bit_array = bit_array

            if bf.check(key)[0]:
                with open(sstable_path, "r") as f:
                    for line in f:
                        entry = json.loads(line)
                        if entry["key"] == key:
                            return entry["value"] if entry["value"] != TOMBSTONE else None
        return None

    def flush(self):
        timestamp = int(time.time())
        sstable_path = f"sstable_{timestamp}.log"
        bf_path = f"sstable_{timestamp}.bf"
        
        bf = BloomFilter(size=1000) # Adjust size as needed
        with open(sstable_path, "w") as f:
            for key, value in self.memtable.data.items():
                f.write(json.dumps({"key": key, "value": value}) + "\n")
                bf.add(key)

        with open(bf_path, 'w') as f:
            json.dump(bf.bit_array, f)

        self.sstables.append((sstable_path, bf_path))
        self.memtable.clear()
        if len(self.sstables) >= self.compaction_threshold:
            self.compact()

    def compact(self):
        sstables_to_compact = self.sstables[:self.compaction_threshold]
        remaining_sstables = self.sstables[self.compaction_threshold:]

        merged_data = {}
        for sstable_path, _ in sstables_to_compact:
            with open(sstable_path, "r") as f:
                for line in f:
                    entry = json.loads(line)
                    merged_data[entry["key"]] = entry["value"]
        
        timestamp = int(time.time())
        new_sstable_path = f"sstable_{timestamp}_compacted.log"
        new_bf_path = f"sstable_{timestamp}_compacted.bf"

        bf = BloomFilter(size=1000) # Adjust size as needed
        with open(new_sstable_path, "w") as f:
            for key, value in sorted(merged_data.items()):
                if value != TOMBSTONE:
                    f.write(json.dumps({"key": key, "value": value}) + "\n")
                    bf.add(key)

        with open(new_bf_path, 'w') as f:
            json.dump(bf.bit_array, f)

        for sstable_path, bf_path in sstables_to_compact:
            os.remove(sstable_path)
            os.remove(bf_path)
            
        self.sstables = remaining_sstables + [(new_sstable_path, new_bf_path)]
