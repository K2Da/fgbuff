class Label:
    def __init__(self, key: str, short: str, long: str, color: str):
        self.key = key
        self.short = short
        self.long = long
        self.color = color

    @property
    def html(self):
        return "<span class='tag' style='background-color: {0}'>{1}</span>".format(self.color, self.short)

    @property
    def text(self):
        return self.long




