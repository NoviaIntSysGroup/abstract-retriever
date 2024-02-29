import os
import tempfile

LIBRARY_IDENTIFIER = "abstract-retriever"
CACHE_DIR = os.path.join(tempfile.gettempdir(), LIBRARY_IDENTIFIER)

# should be comaptiable with RedisCache...
class Cacheable:
    def set(self, key, value):
        raise NotImplementedError("Subclasses must implement set()")

    def get(self, key):
        raise NotImplementedError("Subclasses must implement get()")

    def exists(self, key):
        raise NotImplementedError("Subclasses must implement exists()")

    def path(self, key):
        modified_key = key.replace("/", "_").replace(":", "/", 1).replace(":", "-")
        return os.path.join(self.folder, modified_key + ".txt")

    def __init__(self, folder_name='cache') -> None:
        self.folder = os.path.join(CACHE_DIR, folder_name)
        os.makedirs(self.folder, exist_ok=True)

class FileCache(Cacheable):
    def __init__(self, folder_name='file-cache') -> None:
        super().__init__(folder_name=folder_name)

    def set(self, key, value):
        file_path = self.path(key)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as f:
            f.write(value)
        return True

    def get(self, key):
        file_path = self.path(key)
        
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                return f.read()
        else:
            return None
        
    def exists(self, key):
        file_path = self.path(key)
        
        if os.path.exists(file_path):
            return True

        return False
