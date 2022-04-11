import json

from api.untis_api import UnitsApi
from api.ploty_api import PlotyApi
from api.models.color import Color
import datetime
import re
import itertools
from functools import reduce

TIME_REGEX = "([0-9][0-9]|[0-9])([0-9][0-9])"


class TimetableGenerator:

    def __init__(self, units: UnitsApi, plotly: PlotyApi):
        self.units = units
        self.plotly = plotly

    def generate(self, classId: int):
        n = 2
        clazz = self.units.find_class(class_id=classId)
        # Monday - Friday
        today = datetime.date.today()
        monday = today - datetime.timedelta(days=today.weekday())
        friday = monday + datetime.timedelta(days=4)
        tables = []
        headers = []
        headers.append('')
        for i in range(5):
            day: datetime.datetime = monday + datetime.timedelta(days=i)
            if i == 0 or day.month != monday.month:
                headers.append(day.strftime("%b\n%a\n%d"))
            else:
                headers.append(day.strftime("%a\n%d"))
            table = self.units.get_timetable(klasse=clazz, start_time=day, end_time=day)
            tables.append(json.loads(self._toJson(table)))
        times = [1350]
        for table in tables:
            if table is not None:
                for time in table:
                    times.append(time['startTime'])
                    times.append(time['endTime'])
        print(tables)
        times.sort()
        groupedTimes = [list(v) for k, v in itertools.groupby(times)]
        groupedTimes = reduce(self._onlyTwoEntries, groupedTimes)
        newTimes = (groupedTimes[2::2] + groupedTimes[1::2])
        newTimes.sort()
        newTimes = list(map(self._intToTimeString, newTimes))
        times = list(dict.fromkeys(times))
        blocks = (len(times) - 1)
        fillColor = [[self.plotly.getTheme().none_color] * blocks] * (len(tables) + 1)
        fillColor[0] = ([self.plotly.getTheme().first_column_color] * blocks)
        cellsData = [['1'] * blocks] * (len(tables) + 1)
        groupedBlock = list(map(self._listToString, list(newTimes[i:i + n] for i in range(0, len(newTimes), n))))
        leftBlocks = [groupedBlock[x:x + 1] for x in range(0, len(groupedBlock))]
        for i in range(5):
            x = tables[i]
            x.sort(key=lambda t: t['startTime'])
            if len(x) == 0:
                cellsData[i + 1] = list([' '] * blocks)

            else:
                cellsData[i + 1] = self._table_to_entry(x, groupedBlock)
            print(cellsData[i + 1])

        cellsData[0] = leftBlocks
        self.plotly.build(headers=headers, cellData=cellsData, colColors=fillColor)
        self.plotly.export()

    def _onlyTwoEntries(self, a, b):
        return a + b[0:2]

    def _intToTimeString(self, n):
        return re.sub(TIME_REGEX, r"\1:\2", str(n))

    def _listToString(self, n):
        return str.join(f"-", n)

    def _table_to_entry(self, table, left_blocks):
        result = []

        for x, block in enumerate(left_blocks):
            print(table)
            re = self.find_block(table, block)
            if re is not None:
                room = str(self.units.find_room(room_id=re['ro'][0]['id']))
                subject = self.units.find_subject(subject_id=re['su'][0]['id'])
                result.append(str(f'{subject}<br>{room}<br>    '))
            else:
                result.append(' ')
        return result

    def find_block(self, table, block):
        for x in table:
            time = [self._intToTimeString(x['startTime']), self._intToTimeString(x['endTime'])]
            mapped_time = self._listToString(time)
            if mapped_time == block:
                return x
        return None

    # print(re.sub(TIME_REGEX,r"\1:\2", str(time['startTime'])))
    def _toJson(self, obj) -> str:
        return str(obj).replace("'", '"')
