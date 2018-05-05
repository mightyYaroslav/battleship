class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Dimensions(metaclass=Singleton):

    def __init__(self, max_width: int, max_height: int):
        self.width = max_width
        self.max_height = max_height
        self.instance = {
            "title": {
                "width": max_width,
                "height": 1
            },
            "subtitle": {
                "width": round(max_width / 2),
                "height": 1
            },
            "player": {
                "width": round(max_width / 2),
                "height": round(max_height / 2)
            },
            "history": {
                "width": max_width
            },
            "command": {
                "width": max_width,
                "height": 4
            }
        }

        sumheight = 0
        for v in self.instance.values():
            for (dim_key, dim_val) in v.items():
                if dim_key == "height":
                    sumheight += dim_val

        self.instance["history"]["height"] = max_height - sumheight
