import os
import webuntis
import datetime
import json
import plotly.graph_objects as go
from plotly.colors import n_colors


class untis():
    def __init__(self, server, username, password, school, useragent):
        # Creating the Session
        self.s = webuntis.Session(
            server      = server,
            username    = username,
            password    = password,
            school      = school,
            useragent   = useragent
        )


        # Background color for Outfile
        self.red = 'rgb(251, 72, 72)'
        self.purple = 'rgb(189, 163, 199)'
        self.orange = 'rgb(243, 184, 98)'
        self.darkOrange = 'rgb(199, 131, 32)'
        
        # For better understanding in usage
        self.teacher = "te"
        self.klasse = "kl"
        self.subject = "su"
        self.room = "ro"

        # Data for the Output Timetable
        self.headerData = ['Stunde', 'Mittwoch', 'Donnerstag']
        self.cellsData  = [['1','2','3','4','5','6','7','8','9','10','11'], # 1st Column -> Lessons
                            [], # Wednsday
                            []] # Thursday
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
        self.fill_secCol    = []
        self.fill_thirCol   = []

        self.code       = ''
        self.teacher    = ''
        self.room       = ''
        self.subject    = ''

        self.lastUpdate = 1

        # Styling for the Output Timetable
        self._refreshHeader()

        # Declaring dictionarys to be able to identify the timteable subjects
        today = datetime.date.today()
        self.monday  = today - datetime.timedelta(days=today.weekday())
        self.friday = self.monday + datetime.timedelta(days=4)
        self.tempWednsday = {
        '735':  {},
        '820':  {},
        '930':  {},
        '1015': {},
        '1120': {},
        '1205': {},
        '1300': {},
        '1350': {},
        '1435': {},
        '1530': {},
        '1615': {},
        }
        self.tempThursday = {
        '735':  {},
        '820':  {},
        '930':  {},
        '1015': {},
        '1120': {},
        '1205': {},
        '1300': {},
        '1350': {},
        '1435': {},
        '1530': {},
        '1615': {},
        }
        self.fetchedWednsday = {
        '735':  {},
        '820':  {},
        '930':  {},
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
        '735':  {},
        '820':  {},
        '930':  {},
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

    def _exportTT(self):
        try:
            os.remove('temp\\wedTimetable.json')
            os.remove('temp\\thurTimetable.json')
        except:
            pass
        klasse = self.s.klassen().filter(id=1144)[0]
        #self.wednsday = self.monday + datetime.timedelta(days=2)
        #self.thursday = self.monday + datetime.timedelta(days=3)

        self.wednsday = datetime.date(2021, 12, 15)
        self.thursday = datetime.date(2021, 12, 16)

        wedTT = str(self.s.timetable(klasse=klasse, start=self.wednsday, end=self.wednsday))
        wedTT = wedTT.replace("'", "\"")
        fi = open('temp\\wedTimetable.json', "a")
        fi.write(wedTT)
        fi.close
        #print(wedTT)

        thurTT = str(self.s.timetable(klasse=klasse, start=self.thursday, end=self.thursday))
        thurTT = thurTT.replace("'", "\"")
        fi = open('temp\\thurTimetable.json', "a")
        fi.write(thurTT)
        fi.close
        #print(thurTT)

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
        #print(list2)

        fi2 = open('temp\\thurTimetable.json')
        list2 = json.load(fi2)
        fi2.close()
        self._sortLessons('thursday', list2, False)
        #print(list2)
    
    def _processTable(self, day, time, data, temp):
        if temp == True:
            if day == 'wednsday':
                self.tempWednsday[time] = data
                #print(self.tempWednsday)
            elif day == 'thursday':
                self.tempThursday[time] = data
                #print(self.tempThursday)
            else:
                print("ERROR at _processTable")
        else:
            if day == 'wednsday':
                self.fetchedWednsday[time] = data
                #print(self.fetchedWednsday)
            elif day == 'thursday':
                self.fetchedThursday[time] = data
                #print(self.fetchedThursday)
            else:
                print("ERROR at _processTable")
                #pass

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
                self._processTable(str(day), '1250', i, temp)
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
        #print(self.tempWednsday)

    def _iterateTT(self, iList): # iList has to bis format: ['weekday', {*timetable data*}]
        # Will get properly soft-coded later --> Be able to use the bot with any schooldays
        with open("templates\exportData.json") as ed:
            jsonData = json.load(ed)
            
            for key in iList[1].keys():
                # Get the Data to put in the export Table
                #print(self.fetchedWednsday[key])
                try:
                    self.teacher     = iList[1][key][self.teacher][0]["id"]
                    self.subject     = self._getSubject(iList[1][key][self.subject][0]["id"])
                    self.room        = self._getRoom(iList[1][key][self.rooms][0]["id"])
                except:
                    #print(key + " empty")
                    pass

                try:
                    # Get the Code to put in the export Table
                    self.code        = iList[1][key]['code']
                    #print(self.code)

                    # Assigning the Data to the template used to create the exportable table
                    if iList[0] == 'wednsday':
                        jsonData[0]["date"]    = int(str(self.wednsday).replace("-", ""))
                        jsonData[0][key]["code"]    = self.code
                        jsonData[0][key]["teacher"] = self.teacher
                        jsonData[0][key]["subject"] = self.subject
                        jsonData[0][key]["room"]    = self.room

                    elif iList[0] == 'thursday':
                        jsonData[1]["date"]    = int(str(self.thursday).replace("-", ""))
                        jsonData[1][key]["code"]    = self.code
                        jsonData[1][key]["teacher"] = self.teacher
                        jsonData[1][key]["subject"] = self.subject
                        jsonData[1][key]["room"]    = self.room

                except:
                    self.code = 'none'
                    if iList[0] == 'wednsday':
                        jsonData[0]["date"]    = int(str(self.wednsday).replace("-", ""))
                        jsonData[0][key]["code"]    = self.code
                        jsonData[0][key]["teacher"] = self.teacher
                        jsonData[0][key]["subject"] = self.subject
                        jsonData[0][key]["room"]    = self.room

                    elif iList[0] == 'thursday':
                        jsonData[1]["date"]    = int(str(self.thursday).replace("-", ""))
                        jsonData[1][key]["code"]    = self.code
                        jsonData[1][key]["teacher"] = self.teacher
                        jsonData[1][key]["subject"] = self.subject
                        jsonData[1][key]["room"]    = self.room

                    jsonData[0]
                    pass
        with open("templates\exportData.json", 'w') as ed:
            json.dump(jsonData, ed)
            print(jsonData)

    def _refreshHeader(self):
        self.header=dict(values=self.headerData,
                                line_color='darkslategray',
                                fill_color=self.darkOrange,
                                align='center')
        self.cells=dict(values=self.cellsData,
                                line_color='darkslategray',
                                fill_color=[self.fill_firstCol, self.fill_secCol, self.fill_thirCol],
                                align='center',
                                height=45)

    def _createTable(self):
        self.table = go.Figure(data=[go.Table(
            columnorder=[1,2,3],
            columnwidth=[10,45,45],
            
            header=self.header,
            cells=self.cells
        )])

    def _updateTable(self):
        pass

    def _getRoom(self, roomId):
        room = self.s.rooms().filter(id=roomId)
        #print(room)
        return room

    def _getSubject(self, subId):
        subject = self.s.subjects().filter(id=subId)
        return subject

    def _getTeacher(self, teacherId):
        pass

    def _getLastUpdate(self):
        stamp = self.s.last_import_time()
        date = datetime.datetime.fromtimestamp(stamp / 1000)
        print(date)


    def getSubject(self):
        pass
    def debugFunc(self):
        self._exportTT()
        self._loadTemplate()
        self._loadCurrent()
        self._iterateTT(['wednsday', self.fetchedWednsday])
        #self._refreshHeader()
        #self._createTable()
        #self.table.show()

