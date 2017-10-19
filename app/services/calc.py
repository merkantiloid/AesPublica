class Calc:
    def __init__(self, space):
        self.sel_space = space

    def to_json(self):
        return {
            "selSpace": self.sel_space,
        }