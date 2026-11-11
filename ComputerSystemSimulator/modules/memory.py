class Memory:
    """A simple addressable memory model; each address stores one Python value."""

    def __init__(self, capacity=1024):
        if not isinstance(capacity, int) or capacity <= 0:
            raise ValueError("capacity must be a positive integer")
        self.capacity = capacity
        self.storage = {}

    def _valid_address(self, address):
        return isinstance(address, int) and 0 <= address < self.capacity

    def write(self, address, value):
        if not self._valid_address(address):
            return False
        self.storage[address] = value
        return True

    def read(self, address):
        if not self._valid_address(address):
            return None
        return self.storage.get(address)

    def delete(self, address):
        if not self._valid_address(address):
            return False
        return self.storage.pop(address, None) is not None

    def clear(self):
        self.storage.clear()

    def get_usage(self):
        used = len(self.storage)
        return {"used": used, "total": self.capacity, "free": self.capacity - used}

    def get_contents(self):
        return dict(sorted(self.storage.items()))
