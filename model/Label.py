class Label:
    def __init__(self, key: str, short: str, long: str):
        self.key = key
        self.short = short
        self.long = long

    @property
    def text(self):
        return self.long

    @property
    def where(self):
        return 'labels like %s'

    @property
    def param(self):
        return '%{0}%'.format(self.key)

    @property
    def is_link(self):
        return True


class CountryLabel(Label):
    @property
    def where(self):
        return 'country = %s'

    @property
    def param(self):
        return self.key


class MenuLabel(Label):
    @property
    def where(self):
        return None

    @property
    def param(self):
        return None

    @property
    def is_link(self):
        return False

