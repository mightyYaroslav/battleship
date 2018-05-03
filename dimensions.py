from typing import Dict


class Dimensions:

    @staticmethod
    def for_game(max_height: int, max_width: int) -> Dict[str, Dict[str, int]]:
        dims = {
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
        for v in dims.values():
            for (dim_key, dim_val) in v.items():
                if dim_key == "height":
                    sumheight += dim_val

        dims["history"]["height"] = max_height - sumheight
        return dims
