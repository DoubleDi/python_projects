# you can write to stdout for debugging purposes, e.g.

# {k=>{v, t}}
# put(k, v)
# get(k)
# dict = {k=>v}
# heap = {(t,k)}
# print("This is a debug message")


class LRUCache:
    def __init__(self, size=10):
        self.size = size
        self.d = {}
        self.h = heap()
        self.c = 0
        self.lock = lock()

    def put(self, k, v):
        self.lock.lock()
        if len(self.d) == self.size and not k in self.d:
            (t, kk) = self.h.first()
            self.d.pop(kk)
        if k in self.d:
            (v, t) = self.d[k]
            self.h.pop((t, k))
        self.c += 1
        t = self.c
        self.d[k] = (v, t)
        self.h.add((t, k))
        self.lock.unlock()

    def get(self, k):
        self.lock.rlock()
        r = self.d.get(k)
        if r is None:
            self.lock.runlock()
            return None
        v, t = r
        self.lock.wlock()
        self.h.pop((t, k))
        self.c += 1
        t = self.c
        self.h.add((t, k))
        self.d[k] = (v, t)
        self.lock.unlock()
        return v
