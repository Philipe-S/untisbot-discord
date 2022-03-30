class Color(object):

    @property
    def color(self):
        return f'rgb({self._red},{self._green},{self._blue})'

    def __init__(self, red: int, green: int, blue: int):
        self._red = red
        self._green = green
        self._blue = blue
