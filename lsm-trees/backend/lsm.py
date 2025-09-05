import os
import time
import json

TOMBSTONE = "__TOMBSTONE__"

class MemTable:
    def __init__(self, threshold):
        self.threshold = threshold
        self.data = {}
        self.wal = open("wal.log", "a")

    def set(self, key, value):
        self.wal.write(json.dumps({"key": key, "value": value}) + "\n")
        self.wal.flush()
        self.data[key] = value
        return len(self.data) >= self.threshold

    def get(self, key):
        return self.data.get(key)

    def clear(self):
        self.data = {}
        self.wal.close()
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
        for sstable in reversed(self.sstables):
            with open(sstable, "r") as f:
                for line in f:
                    entry = json.loads(line)
                    if entry["key"] == key:
                        return entry["value"] if entry["value"] != TOMBSTONE else None
        return None

    def flush(self):
        sstable_path = f"sstable_{int(time.time())}.log"
        with open(sstable_path, "w") as f:
            for key, value in sorted(self.memtable.data.items()):
                f.write(json.dumps({"key": key, "value": value}) + "\n")
        self.sstables.append(sstable_path)
        self.memtable.clear()
        if len(self.sstables) >= self.compaction_threshold:
            self.compact()

    def compact(self):
        merged_data = {}
        for sstable in self.sstables:
            with open(sstable, "r") as f:
                for line in f:
                    entry = json.loads(line)
                    merged_data[entry["key"]] = entry["value"]
        
        new_sstable_path = f"sstable_{int(time.time())}_compacted.log"
        with open(new_sstable_path, "w") as f:
            for key, value in sorted(merged_data.items()):
                if value != TOMBSTONE:
                    f.write(json.dumps({"key": key, "value": value}) + "\n")

        for sstable in self.sstables:
            os.remove(sstable)
            
        self.sstables = [new_sstable_path]
