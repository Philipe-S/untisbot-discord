import datetime
from webuntis.objects import *
import webuntis
class UnitsApi:
    def __init__(self, server: str, username: str, password: str, school: str, useragent: str):
        self.server = server
        self.username = username
        self.password = password
        self.school = school
        self.useragent = useragent
        self.session = webuntis.Session(
            server=str(self.server),
            username=str(self.username),
            password=str(self.password),
            school=str(self.school),
            useragent=str(self.useragent)
        )

    def login(self):
        try:
            self.session.login()
        except webuntis.errors.RemoteError as e:
            print(str(e))

    def logout(self) -> None:
        self.session.logout()

    def find_class(self, class_id: int) -> KlassenObject:
        return self.session.klassen().filter(id=class_id)[0]

    def find_teacher(self, teacher_id: int) -> TeacherObject:
        return self.session.teachers().filter(id=teacher_id)[0]

    def find_subject(self, subject_id: int) -> SubjectObject:
        return self.session.subjects().filter(id=subject_id)[0]

    def find_room(self, room_id: int) -> RoomObject:
        return self.session.rooms().filter(id=room_id)[0]

    def get_timetable(self, klasse: KlassenObject, start_time: datetime.datetime, end_time: datetime.datetime) -> PeriodList:
        return self.session.timetable_extended(klasse=klasse, start=start_time, end=end_time)

