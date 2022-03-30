from api.models.color import Color
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
    def first_column_color(self) -> str:
        return str(self._first_column_color.color)

    @first_column_color.setter
    def first_column_color(self, value: Color):
        self._first_column_color = value

    @first_column_color.deleter
    def first_column_color(self):
        del self._first_column_color

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

    def __init__(self, cancelled_color: Color, irregular_color: Color, none_color: Color, first_column_color: Color):
        self._cancelled_color = cancelled_color
        self._irregular_color = irregular_color
        self._none_color = none_color
        self._first_column_color = first_column_color