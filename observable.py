class Observable:
    def __init__(self, wrapped, *callbacks):
        self.wrapped = wrapped
        self.callbacks = list(callbacks)

    def subscribe(self, cb):
        self.callbacks.append(cb)

    def unsubscribe(self, cb):
        self.callbacks.append(cb)

    def __getattr__(self, name):
        res = self.wrapped.__getattribute__(name)
        if not callable(res):
            return res

        def wrap(*args, **kwargs):
            for c in self.callbacks:
                c(self.wrapped, *args, **kwargs)
            return res(*args, **kwargs)

        return wrap

    def __str__(self):
        return self.wrapped.__str__()
