class Color(object):

    @property
    def color(self):
        return f'rgb({self._red},{self._green},{self._blue})'

    def __init__(self, red: int, green: int, blue: int):
        self._red = red
        self._green = green
        self._blue = blue


class ThemeData(object):

    @property
    def none_color(self) -> str:
        return str(self._none_color.color)

    @none_color.setter
    def none_color(self, value: Color):
        self._none_color = value

    @none_color.deleter
    def none_color(self):
        del self._none_color

    @property
    def irregular_color(self) -> str:
        return str(self._irregular_color.color)

    @irregular_color.setter
    def irregular_color(self, value: Color):
        self._irregular_color = value

    @irregular_color.deleter
    def irregular_color(self):
        del self._irregular_color

    @property
    def cancelled_color(self) -> str:
        return str(self._cancelled_color.color)

    @cancelled_color.setter
    def cancelled_color(self, value: Color):
        self._cancelled_color = value

    @cancelled_color.deleter
    def cancelled_color(self):
        del self._cancelled_color

    def __init__(self, cancelled_color: Color, irregular_color: Color, none_color: Color):
        self._cancelled_color = cancelled_color
        self._irregular_color = irregular_color
        self._none_color = none_color



