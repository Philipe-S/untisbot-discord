import os

import plotly.io.kaleido
import webuntis
import datetime
import json
import plotly.graph_objects as go
import hashlib

from utils.constants import ThemeData, Color
from utils.enums import HeaderData


class Untis():

    def to_string(self, step: int) -> str:
        return f'{step}'

    def __init__(self, server, username, password, school, useragent):
        # Creating the Session
        self.s = webuntis.Session(
            server=server,
            username=username,
            password=password,
            school=school,
            useragent=useragent
        )

        self.themeData = ThemeData(
            cancelled_color=Color(251, 72, 72),
            irregular_color=Color(189, 163, 199),
            none_color=Color(243, 184, 98)
        )


        # Background color for Outfile
        self.red = self.themeData.cancelled_color
        self.purple = self.themeData.irregular_color
        self.orange = self.themeData.none_color
        self.darkOrange = 'rgb(199, 131, 32)'


        self.layout = go.Layout(
            #width=900,
            #height=800,
        )

        # Data for the Output Timetable
        self.headerData = []

        for item in HeaderData:
            #print(item.value)
            self.headerData.append(item.value)

        self.cellsData = [['1','2','3','4','5','6','7','8','9','10','11'],  # 1st Column -> Lessons -- map(self.to_string ,range(1, 11, 1))
                          ['1','2','3','4','5','6','7','8','9','10','11'],  # Wednsday
                          ['1','2','3','4','5','6','7','8','9','10','11']]  # Thursday
        self.fill_firstCol = [self.darkOrange,
                              self.darkOrange,
                              self.darkOrange,
                              self.darkOrange,
                              self.darkOrange,
                              self.darkOrange,
                              self.darkOrange,
                              self.darkOrange,
                              self.darkOrange,
                              self.darkOrange]
        self.fill_secCol = [self.orange,
                            self.orange,
                            self.orange,
                            self.orange,
                            self.orange,
                            self.orange,
                            self.orange,
                            self.orange,
                            self.orange,
                            self.orange,
                            self.orange]
        self.fill_thirCol = [self.orange,
                             self.orange,
                             self.orange,
                             self.orange,
                             self.orange,
                             self.orange,
                             self.orange,
                             self.orange,
                             self.orange,
                             self.orange,
                             self.orange]

        self.code = ''
        self.teacher = ''
        self.room = ''
        self.subject = ''

        self.lastUpdate = 1

        # Styling for the Output Timetable
        self._refreshHeader()

        # Declaring dictionarys to be able to identify the timteable subjects
        today = datetime.date.today()
        self.monday = today - datetime.timedelta(days=today.weekday())
        self.friday = self.monday + datetime.timedelta(days=4)

        self.fetchedWednsday = {
            '735': {},
            '820': {},
            '930': {},
            '1015': {},
            '1120': {},
            '1205': {},
            '1300': {},
            '1350': {},
            '1435': {},
            '1530': {},
            '1615': {},
        }
        self.fetchedThursday = {
            '735': {},
            '820': {},
            '930': {},
            '1015': {},
            '1120': {},
            '1205': {},
            '1300': {},
            '1350': {},
            '1435': {},
            '1530': {},
            '1615': {},
        }

    # ---- Initial Setup end ----





    def login(self):
        try:
            print('Attemting login...')
            self.s.login()
            print('login successful')
        except:
            print('Login unsuccessful')

    def logout(self):
        try:
            print('logging out...')
            self.s.logout()
            print('done.')
        except:
            print('Logout not complete')


    def _calculateLessons(self):
        pass

    def _clearData(self):
        for key in self.fetchedWednsday.keys():
            self.fetchedWednsday[key] = {}
        for key in self.fetchedThursday.keys():
            self.fetchedThursday[key] = {}

    def _exportTimetable(self):
        try:
            os.remove('temp\\wedTimetable.json')
            os.remove('temp\\thurTimetable.json')
        except:
            pass
        klasse = self.s.klassen().filter(id=1144)[0]
        self.wednsday = self.monday + datetime.timedelta(days=2)
        self.thursday = self.monday + datetime.timedelta(days=3)

        # self.wednsday = datetime.date(2021, 11, 24)
        #self.thursday = datetime.date(2021, 12, 16)

        wedTT = str(self.s.timetable(klasse=klasse, start=self.wednsday, end=self.wednsday))
        wedTT = wedTT.replace("'", "\"")
        fi = open('temp\\wedTimetable.json', "a")
        fi.write(wedTT)
        fi.close()
        # print(wedTT)

        thurTT = str(self.s.timetable(klasse=klasse, start=self.thursday, end=self.thursday))
        thurTT = thurTT.replace("'", "\"")
        fi = open('temp\\thurTimetable.json', "a")
        fi.write(thurTT)
        fi.close()
        # print(thurTT)

    def _loadTemplate(self):
        fi = open('templates\\timetableWed.json')
        list1 = json.load(fi)
        fi.close()
        self._sortLessons('wednsday', list1, True)

    def _loadCurrent(self):
        fi = open('temp\\wedTimetable.json')
        list2 = json.load(fi)
        fi.close()
        self._sortLessons('wednsday', list2, False)
        # print(list2)

        fi2 = open('temp\\thurTimetable.json')
        list3 = json.load(fi2)
        fi2.close()
        self._sortLessons('thursday', list3, False)
        #print(list2)

    def _processTable(self, day, time, data, temp):
        if day == 'wednsday':
            self.fetchedWednsday[time] = data
            #print(self.fetchedWednsday)
        elif day == 'thursday':
            self.fetchedThursday[time] = data
            #print(self.fetchedThursday)
        else:
            print("ERROR at _processTable")

    def _sortLessons(self, day, liste, temp):
        for i in liste:
            time = str(i['startTime'])
            if time == '735':
                self._processTable(str(day), '735', i, temp)
            elif time == '820':
                self._processTable(str(day), '820', i, temp)
            elif time == '930':
                self._processTable(str(day), '930', i, temp)
            elif time == '1015':
                self._processTable(str(day), '1015', i, temp)
            elif time == '1120':
                self._processTable(str(day), '1120', i, temp)
            elif time == '1205':
                self._processTable(str(day), '1205', i, temp)
            elif time == '1300':
                self._processTable(str(day), '1300', i, temp)
            elif time == '1350':
                self._processTable(str(day), '1350', i, temp)
            elif time == '1435':
                self._processTable(str(day), '1435', i, temp)
            elif time == '1530':
                self._processTable(str(day), '1530', i, temp)
            elif time == '1615':
                self._processTable(str(day), '1615', i, temp)
            else:
                print("ERROR at _sortLessons")
                pass

    def _iterateTT(self, iList, ret):  # iList has to be this format: ['weekday', {*timetable data*}]
        # Will get properly soft-coded later --> Be able to use the bot with any schooldays

        if ret == True:
            with open("templates\last_import_data.json") as last:
                jsonData = json.load(last)
        else:
            with open("templates\exportData.json") as ed:
                jsonData = json.load(ed)

            for key in iList[1].keys():

                # print(iList[1][key])
                # print(key)
                # Get the Data to put in the export Table
                # print(self.fetchedWednsday[key])
                try:

                    self.teacher = iList[1][key]["te"][0]["id"]
                    self.subject = self._getSubject(iList[1][key]["su"][0]["id"])
                    self.room = self._getRoom(iList[1][key]["ro"][0]["id"])
                    self.code        = ''
                except:
                    # print(key + " empty")
                    pass

                try:
                    # Get the Code to put in the export Table
                    self.code = iList[1][key]['code']
                    # print(iList[1][key])

                    # Assigning the Data to the template used to create the exportable table
                    if iList[0] == 'wednsday':
                        jsonData[0]["date"] = int(str(self.wednsday).replace("-", ""))
                        jsonData[0][key]["teacher"] = int(self.teacher)
                        jsonData[0][key]["code"] = str(self.code)
                        jsonData[0][key]["subject"] = str(self.subject)
                        jsonData[0][key]["room"] = str(self.room)

                    elif iList[0] == 'thursday':
                        jsonData[1]["date"] = int(str(self.thursday).replace("-", ""))
                        jsonData[1][key]["teacher"] = int(self.teacher)
                        jsonData[1][key]["code"] = str(self.code)
                        jsonData[1][key]["subject"] = str(self.subject)
                        jsonData[1][key]["room"]    = str(self.room)
                        self.code = 'none'

                except:
                    # print(iList[1][key])
                    self.code = 'none'
                    if iList[0] == 'wednsday':
                        jsonData[0]["date"] = int(str(self.wednsday).replace("-", ""))
                        try:
                            jsonData[0][key]["teacher"] = int(self.teacher)
                        except:
                            pass
                        jsonData[0][key]["code"] = str(self.code)
                        jsonData[0][key]["subject"] = str(self.subject)
                        jsonData[0][key]["room"] = str(self.room)

                    elif iList[0] == 'thursday':
                        jsonData[1]["date"]    = int(str(self.thursday).replace("-", ""))
                        jsonData[1][key]["teacher"] = int(self.teacher)
                        jsonData[1][key]["code"] = str(self.code)
                        jsonData[1][key]["subject"] = str(self.subject)
                        jsonData[1][key]["room"] = str(self.room)

                self.teacher    = 1337
                self.subject    = ""
                self.room       = ""
                #print(jsonData)

        if ret == True:
            with open("templates\last_import_data.json", "w") as last:
                json.dump(jsonData, last)
        else:
            with open("templates\exportData.json", 'w') as ed:
                json.dump(jsonData, ed)

    def _refreshHeader(self):
        self.header = dict(values=self.headerData,
                           line_color='darkslategray',
                           fill_color=self.darkOrange,
                           align='center',
                           font=dict(color='black', size=16))
        self.cells = dict(values=self.cellsData,
                          line_color='darkslategray',
                          fill_color=[self.fill_firstCol, self.fill_secCol, self.fill_thirCol],
                          align=['center', 'center'],
                          font=dict(color='black', size=14),
                          height=55)

    def _createTable(self):
        self.table = go.Figure(data=[go.Table(
            columnorder=[1, 2, 3],
            #columnwidth=[2, 10, 10],

            header=self.header,
            cells=self.cells
        )], layout=self.layout)

    def _updateTable(self, day):
        # This part is going through the sorted Data from the WebUntis API and changing the table colors
        # 
        with open("templates\exportData.json", 'r') as ed:
            jsonData = json.load(ed)
            #print(jsonData)

            if day == 'wednsday':
                data = jsonData[0]
                # print(data)

                for key in data:
                    if key == "date":
                        pass
                    else:
                        lesson = self._translateTime(key) - 1
                        self.fill_secCol[lesson] = self.orange
                        if data[key]['teacher']  == 1337:
                            lessonInfo = str(data[key]['subject']) + "<br>" + str(data[key]['room']) + "<br>" + ""
                        else:
                            lessonInfo = str(data[key]['subject']) + "<br>" + str(data[key]['room']) + "<br>" + str(data[key]['teacher'])

                        if data[key]['code'] == 'cancelled':
                            self.fill_secCol[lesson] = self.red
                        elif data[key]['code'] == "irregular":
                            self.fill_secCol[lesson] = self.purple
                        elif data[key]['code'] == "none":
                            self.fill_secCol[lesson] = self.orange
                        else:
                            print("Error at _updateTable")
                    #print(key)

                        # This Part is getting the Lesson Data from the sorted Data fetched from the WebUntis API
                        # and writing the Lesson Information to the plotly table
                        self.cellsData[1][lesson] = lessonInfo

            elif day == 'thursday':
                data = jsonData[1]
                # print(data)

                for key in data:
                    #print(data[key])
                    if key == "date":
                        pass
                    else:
                        lesson = self._translateTime(key) - 1
                        self.fill_thirCol[lesson] = self.orange
                        if data[key]['teacher'] == 1337:
                            lessonInfo = str(data[key]['subject']) + "<br>" + str(data[key]['room']) + "<br>" + ""
                        else:
                            lessonInfo = str(data[key]['subject']) + "<br>" + str(data[key]['room']) + "<br>" + str(
                                data[key]['teacher'])

                        if data[key]['code'] == 'cancelled':
                                self.fill_thirCol[lesson] = self.red
                        elif data[key]['code'] == "irregular":
                            self.fill_thirCol[lesson] = self.purple
                        elif data[key]['code'] == "none":
                            self.fill_thirCol[lesson] = self.orange
                        else:
                            print("Error at _updateTable")
                        self.cellsData[2][lesson] = lessonInfo
                #print(key)
            else:
                pass

    # Used to index the lessons by numbers, not by time. WebUntis API is only giving the start / end times so this function is necessary
    def _translateTime(self, time):
        if time == '735':
            return 1
        elif time == '820':
            return 2
        elif time == '930':
            return 3
        elif time == '1015':
            return 4
        elif time == '1120':
            return 5
        elif time == '1205':
            return 6
        elif time == '1300':
            return 7
        elif time == '1350':
            return 8
        elif time == '1435':
            return 9
        elif time == '1530':
            return 10
        elif time == '1615':
            return 11
        else:
            print("Error")
            return "Error"

    def _hashTimetable(self, inputString):
        hash = hashlib.sha256(str.encode(inputString)).hexdigest()
        return hash

    # This function will return either "True" if changes have been detected or "False" if no changes were found.
    def findChanges(self):
        self._exportTimetable()
        self._loadCurrent()
        self._iterateTT(['wednsday', self.fetchedWednsday], True)
        self._iterateTT(['thursday', self.fetchedThursday], True)
        with open("templates\last_import_data.json", "r") as file:
            newHash = self._hashTimetable(str(json.load(file)))
        with open("templates\exportData.json", "r") as file2:
            oldHash = self._hashTimetable(str(json.load(file2)))

        if oldHash != newHash:
            return True
        else:
            return False

    def _exportImage(self):
        plotly.io.kaleido.scope.default_scale = "1"
        self.table.write_image("images\\timetable.png")

    def _getRoom(self, roomId):
        room = str(self.s.rooms().filter(id=roomId)).replace("[", "").replace("]", "")
        # print(room)
        return room

    def _getSubject(self, subId):
        subject = str(self.s.subjects().filter(id=subId)).replace("[", "").replace("]", "")
        # print(subject)
        return subject

    def _getTeacher(self, teacherId):
        pass

    def _getLastUpdate(self):
        hash = hashlib.sha256(str.encode(str(self.s.last_import_time().date))).hexdigest()
        #print(hash)
        with open("templates\\last_import_time.txt", "w") as file:
            file.write(str(hash))

    def _compareUpdateTimes(self):
        with open("templates\\last_import_time.txt", "r") as file:
            hash = file.read()
            newHash = hashlib.sha256(str.encode(str(self.s.last_import_time().date))).hexdigest()

            if hash == newHash:
                # Returns "false" if hash did not change
                return "false"
            else:
                # Returns "true" if hash changed, will set the new update time aswell
                self._getLastUpdate()
                return "true"


    def debugFunc(self):
        self._getLastUpdate()
        self._exportTimetable()
        self._loadCurrent()
        self._iterateTT(['wednsday', self.fetchedWednsday], False)
        self._updateTable('wednsday')
        self._iterateTT(['thursday', self.fetchedThursday], False)
        self._updateTable('thursday')
        self._refreshHeader()
        self._createTable()
        print(self.findChanges())
        self._exportImage()
        self.table.show()
