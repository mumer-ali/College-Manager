from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.properties import StringProperty
import mysql.connector as msc
import datetime as dt


global id
id = 123
global gender
gender = "Male"
global course
course = ""
global name
name = ""
global username
username = ''
global subs_med_1
subs_med_1 = ['Biology', 'Chemistry',
              'Physics', 'Urdu', 'English', 'Islamiyat']
global subs_med_2
subs_med_2 = ['Biology', 'Chemistry', 'Physics',
              'Urdu', 'English', 'Pakistan Studies']
global subs_eng_1
subs_eng_1 = ['Math', 'Chemistry',
              'Physics', 'Urdu', 'English', 'Islamiyat']
global subs_eng_2
subs_eng_2 = ['Math', 'Chemistry', 'Physics',
              'Urdu', 'English', 'Pakistan Studies']
global subs_it_1
subs_it_1 = ['Math', 'Computer Science',
             'Physics', 'Urdu', 'English', 'Islamiyat']
global subs_it_2
subs_it_2 = ['Math', 'Computer Science',
             'Physics', 'Urdu', 'English', 'Pakistan Studies']
global subs_bus_1
subs_bus_1 = ['Statistics', 'Accounting',
              'Finance', 'Urdu', 'English', 'Islamiyat']
global subs_bus_2
subs_bus_2 = ['Statistics', 'Accounting',
              'Finance', 'Urdu', 'English', 'Pakistan Studies']
global list_of_subs
list_of_subs = set(subs_med_1).union(
    set(subs_med_2), set(subs_eng_1), set(subs_eng_2), set(subs_it_1), set(subs_it_2), set(subs_bus_1), set(subs_bus_2))

list_of_subs = list(list_of_subs)

global sec_med_1
sec_med_1 = ['A', 'B', 'C']
global sec_med_2
sec_med_2 = ['A', 'B', 'C']
global sec_eng_1
sec_eng_1 = ['A', 'B', 'C']
global sec_eng_2
sec_eng_2 = ['A', 'B', 'C']
global sec_it_1
sec_it_1 = ['A', 'B', 'C']
global sec_it_2
sec_it_2 = ['A', 'B', 'C']
global sec_bus_1
sec_bus_1 = ['A', 'B', 'C']
global sec_bus_2
sec_bus_2 = ['A', 'B', 'C']
global cls_stu_cs
cls_stu_cs = ['1-IT-A', '1-IT-B', '1-IT-C', '2-IT-A', '2-IT-B', '2-IT-C']

global fac_id
fac_id = 123
global fac_name
fac_name = ""
global fac_gender
fac_gender = "Male"
global fac_subject
fac_subject = ""

con = msc.connect(host='localhost', user='root',
                  passwd='Root', database='Qalam')
cursor = con.cursor()


Window.clearcolor = (0.137254902, 0.121568627, 0.126984127, 1)
Window.minimum_width, Window.minimum_height = (500, 600)


class CollegeManagerApp(App):
    pass


class Screen_Manager(ScreenManager):
    pass


class Login_Page(Screen):
    invalid_user_pass = StringProperty("")

    def input_user_pass(self, user_, pass_):
        global username
        username = user_.text
        password = pass_.text
        user = "None"
        # Checking for Admin
        if user == "None":
            query = "select * from admin"
            cursor.execute(query)
            data = cursor.fetchall()
            for i in data:
                if (username in i) and (password in i):
                    user = "Admin"
        if user == "None":
            self.invalid_user_pass = "Incorrect Username or Password!"
        else:
            self.manager.current = 'admin_panel'


class Admin_Panel(Screen):
    def spinner_clicked(self, id):
        if id.text == 'Change Password':
            self.manager.current = 'admin_panel_cp'
        else:
            self.manager.current = 'login_page'


class Admin_Panel_CP(Screen):
    wrong_old_new_pass = StringProperty("")

    def change_password(self, old, new, con_new):
        global username
        password = old.text
        new_pass = new.text
        query = "select * from admin"
        cursor.execute(query)
        data = cursor.fetchall()
        count = 0
        for i in data:
            if username in i:
                if password in i:
                    count += 1
        if count != 0 and (new.text == con_new.text):
            query = "update admin set Password='{}' where Username='{}'".format(
                new_pass, username)
            cursor.execute(query)
            con.commit()
            self.wrong_old_new_pass = "Password Updated"
        else:
            self.wrong_old_new_pass = "Incorrect Username or Passwords"


class Student_Section(Screen):
    pass


class Student_Insert_I(Screen):
    global id
    global name
    global gender
    global course
    errors_student_insert_1 = StringProperty("")

    def student_insert_1_1(self, state, gen):
        global gender
        if state:
            gender = gen
        else:
            gender = ''

    def student_insert_1_3(self, id_insert_student, name_insert_student, course_insert_student):
        global id
        global name
        global gender
        global course
        i = id_insert_student.text
        n = name_insert_student.text
        course = course_insert_student.text
        if i == '' or n == '' or course == '' or gender == '':
            self.errors_student_insert_1 = 'Insufficient Information'
        else:
            self.errors_student_insert_1 = ''
            if not (i.isnumeric()) or len(i) != 6:
                self.errors_student_insert_1 = 'ID can only be a six-digit number'
            elif course == '':
                self.errors_student_insert_1 = 'Select Course'
            elif n == '':
                self.errors_student_insert_1 = 'Enter Name'
            elif n != '':
                id = int(i)
                x = n.split()
                temp = ''
                count = 0
                leng = 0
                for i in x:
                    leng += len(i)
                    if not i.isalpha():
                        count += 1
                if count == 0 and leng < 40:
                    for i in x:
                        temp += str(' ') + str(i.capitalize())
                    temp = temp.strip()
                    name = str(temp)
                    self.manager.current = 'student_insert_2'
                else:
                    self.errors_student_insert_1 = 'Name can only be alphabets less than 40'


class Student_Insert_II(Screen):
    global id
    global name
    global gender
    global course
    global status
    status = "False"
    errors_student_insert_2 = StringProperty('')
    payable_fee = StringProperty('')
    batch = dt.date.today().year
    batch = int(batch)
    monthly_fee = 10000

    def student_insert_2_1(self, state, yes_no):
        global status
        if state:
            status = yes_no
        else:
            status = " "

    def student_insert_2_2(self, year_insert_student, section_insert_student, scholarship_insert_student):
        global status
        year = year_insert_student.text
        section = section_insert_student.text
        sship = scholarship_insert_student.text
        if year == '' or section == '' or status == '':
            self.errors_student_insert_2 = 'Insufficient Information'
        else:
            self.errors_student_insert_2 = ''
            if status == 'True' and sship == '':
                self.errors_student_insert_2 = 'Select the percentage'
            elif status == 'True' and sship != '':
                self.errors_student_insert_2 = ''
                per = sship[0]+sship[1]
                per = int(per)
                per = (per/100)*self.monthly_fee
                per = int(per)
                self.monthly_fee -= per
                try:
                    query = '''insert into Students (Id, Name, Gender, Course,Batch,Section,ScholarshipStatus,ScholarshipPercentage,MonthlyFee,Year)
                                values
                                ({},'{}','{}','{}',{},'{}','{}','{}',{},'{}')'''.format(id, name, gender, course, self.batch, section, status, sship, self.monthly_fee, year)
                    cursor.execute(query)
                    con.commit()
                    if cursor.rowcount > 0:
                        self.errors_student_insert_2 = "Data inserted successfully"
                except:
                    self.errors_student_insert_2 = 'ID not available'
            elif status == 'False':
                self.errors_student_insert_2 = ''
                sship = ''
                try:
                    query = '''insert into Students (Id, Name, Gender, Course,Batch,Section,ScholarshipStatus,ScholarshipPercentage,MonthlyFee,Year)
                                values
                                ({},'{}','{}','{}',{},'{}','{}','{}',{},'{}')'''.format(id, name, gender, course, self.batch, section, status, sship, self.monthly_fee, year)
                    cursor.execute(query)
                    con.commit()
                    if cursor.rowcount > 0:
                        self.errors_student_insert_2 = "Data inserted successfully"
                except:
                    self.errors_student_insert_2 = 'ID not available'


class Student_Update(Screen):
    errors_student_update = StringProperty('')
    global status
    status = "False"
    monthly_fee = 10000

    def student_update_1(self, state, yes_no):
        global status
        if state:
            status = yes_no
        else:
            status = " "

    def student_update_3(self, username_update_student, course_update_student, section_update_student, year_update_student, scholarship_update_student):
        global status
        id_to_update = username_update_student.text
        c_to_update = course_update_student.text
        s_to_update = section_update_student.text
        y_to_update = year_update_student.text
        sship_to_update = scholarship_update_student.text
        if not (id_to_update.isnumeric()) or len(id_to_update) != 6 or id_to_update == '':
            if not (id_to_update.isnumeric()) or len(id_to_update) != 6:
                self.errors_student_update = 'ID can only be a six-digit number'
            if id_to_update == '':
                self.errors_student_update = 'ID required'
        else:
            self.errors_student_update = ''
            if status == 'True' and sship_to_update == '':
                self.errors_student_update = 'Select the percentage'
            elif status == 'True' and sship_to_update != '':
                self.errors_student_update = ''
                id_to_update = int(id_to_update)
                query = "select * from students"
                cursor.execute(query)
                data = cursor.fetchall()
                count = 0
                for i in data:
                    if id_to_update in i:
                        fetched_list = i
                        fetched_list = list(fetched_list)
                        count += 1
                if count == 0:
                    self.errors_student_update = "Record not found"
                else:
                    per = sship_to_update[0]+sship_to_update[1]
                    per = int(per)
                    per = (per/100)*self.monthly_fee
                    per = int(per)
                    self.monthly_fee -= per
                    fetched_list[8] = self.monthly_fee
                    fetched_list[6] = status
                    fetched_list[7] = sship_to_update
                    if c_to_update != '':
                        fetched_list[3] = c_to_update
                    if s_to_update != '':
                        fetched_list[5] = s_to_update
                    if y_to_update != '':
                        fetched_list[9] = y_to_update
                    query = "update students set Course='{}' where ID={}".format(
                        fetched_list[3], id_to_update)
                    cursor.execute(query)
                    con.commit()
                    query = "update students set Section='{}' where ID={}".format(
                        fetched_list[5], id_to_update)
                    cursor.execute(query)
                    con.commit()
                    query = "update students set ScholarshipStatus='{}' where ID={}".format(
                        fetched_list[6], id_to_update)
                    cursor.execute(query)
                    con.commit()
                    query = "update students set ScholarshipPercentage='{}' where ID={}".format(
                        fetched_list[7], id_to_update)
                    cursor.execute(query)
                    con.commit()
                    query = "update students set MonthlyFee={} where ID={}".format(
                        fetched_list[8], id_to_update)
                    cursor.execute(query)
                    con.commit()
                    query = "update students set Year='{}' where ID={}".format(
                        fetched_list[9], id_to_update)
                    cursor.execute(query)
                    con.commit()
                    self.errors_student_update = "Data updated successfully"
            elif status == 'False':
                self.errors_student_update = ''
                id_to_update = int(id_to_update)
                query = "select * from students"
                cursor.execute(query)
                data = cursor.fetchall()
                count = 0
                for i in data:
                    if id_to_update in i:
                        fetched_list = i
                        fetched_list = list(fetched_list)
                        count += 1
                if count == 0:
                    self.errors_student_update = "Record not found"
                else:
                    fetched_list[8] = self.monthly_fee
                    fetched_list[6] = status
                    fetched_list[7] = sship_to_update
                    if c_to_update != '':
                        fetched_list[3] = c_to_update
                    if s_to_update != '':
                        fetched_list[5] = s_to_update
                    if y_to_update != '':
                        fetched_list[9] = y_to_update
                    query = "update students set Course='{}' where ID={}".format(
                        fetched_list[3], id_to_update)
                    cursor.execute(query)
                    con.commit()
                    query = "update students set Section='{}' where ID={}".format(
                        fetched_list[5], id_to_update)
                    cursor.execute(query)
                    con.commit()
                    query = "update students set ScholarshipStatus='{}' where ID={}".format(
                        fetched_list[6], id_to_update)
                    cursor.execute(query)
                    con.commit()
                    query = "update students set ScholarshipPercentage='{}' where ID={}".format(
                        fetched_list[7], id_to_update)
                    cursor.execute(query)
                    con.commit()
                    query = "update students set MonthlyFee={} where ID={}".format(
                        fetched_list[8], id_to_update)
                    cursor.execute(query)
                    con.commit()
                    query = "update students set Year='{}' where ID={}".format(
                        fetched_list[9], id_to_update)
                    cursor.execute(query)
                    con.commit()
                    self.errors_student_update = "Data updated successfully"


class Student_Fetch(Screen):
    text_for_confirmation = StringProperty("")
    list_of_student_fetch = StringProperty("")

    def fetch_student(self, id):
        id_to_fetch = id.text
        try:
            id_to_fetch = int(id_to_fetch)
            query = "select * from students"
            cursor.execute(query)
            data = cursor.fetchall()
            count = 0
            for i in data:
                if id_to_fetch in i:
                    k = str(list(i))
                    self.list_of_student_fetch = k
                    count += 1
            if count == 0:
                self.text_for_confirmation = "Record not found"
        except:
            self.text_for_confirmation = "ID can only be Number"


class Student_Delete(Screen):
    text_for_confirmation = StringProperty("")

    def delete_student(self, id):
        id_to_delete = id.text
        try:
            id_to_delete = int(id_to_delete)
            query = "delete from students where ID={}".format(id_to_delete)
            cursor.execute(query)
            con.commit()
            if cursor.rowcount > 0:
                self.text_for_confirmation = "Data Deleted Successfully"
            else:
                self.text_for_confirmation = "Record not found"
        except:
            self.text_for_confirmation = "ID can only be Number"


class Faculty_Section(Screen):
    pass


class Faculty_Insert_I(Screen):
    global list_of_subs
    subs = list_of_subs
    global fac_id
    global fac_name
    global fac_subject
    global fac_gender
    errors_faculty_insert_1 = StringProperty('')

    def faculty_insert_1_1(self, state, gen):
        global fac_gender
        if state:
            fac_gender = gen
        else:
            fac_gender = ''

    def faculty_insert_1_2(self, id_insert_faculty, name_insert_faculty, subject_insert_faculty):
        global fac_id
        global fac_name
        global fac_subject
        global fac_gender
        i = id_insert_faculty.text
        n = name_insert_faculty.text
        fac_subject = subject_insert_faculty.text
        if i == '' or n == '' or fac_subject == '' or fac_gender == '':
            self.errors_faculty_insert_1 = 'Insufficient Information'
        else:
            self.errors_faculty_insert_1 = ''
            if not (i.isnumeric()) or len(i) != 6:
                self.errors_faculty_insert_1 = 'ID can only be a six-digit number'
            elif fac_subject == '':
                self.errors_faculty_insert_1 = 'Select Subject'
            elif n == '':
                self.errors_faculty_insert_1 = 'Enter Name'
            elif n != '':
                self.errors_faculty_insert_1 = ''
                fac_id = int(i)
                x = n.split()
                temp = ''
                count = 0
                leng = 0
                for i in x:
                    leng += len(i)
                    if not i.isalpha():
                        count += 1
                if count == 0 and leng < 40:
                    for i in x:
                        temp += str(' ') + str(i.capitalize())
                    temp = temp.strip()
                    fac_name = str(temp)
                    self.manager.current = 'faculty_insert_2'
                else:
                    self.errors_faculty_insert_1 = 'Name can only be alphabets less than 40'


class Faculty_Insert_II(Screen):
    global fac_id
    global fac_name
    global fac_subject
    global fac_gender


class Faculty_Update(Screen):
    pass


class Faculty_Fetch(Screen):
    text_for_confirmation = StringProperty("")
    list_of_faculty_fetch = StringProperty("")

    def fetch_faculty(self, id):
        id_to_fetch = id.text
        try:
            id_to_fetch = int(id_to_fetch)
            query = "select * from faculty"
            cursor.execute(query)
            data = cursor.fetchall()
            count = 0
            for i in data:
                if id_to_fetch in i:
                    k = str(list(i))
                    self.list_of_faculty_fetch = k
                    count += 1
            if count == 0:
                self.text_for_confirmation = "Record not found"
        except:
            self.text_for_confirmation = "ID can only be Number"


class Faculty_Delete(Screen):
    text_for_confirmation = StringProperty("")

    def delete_faculty(self, id):
        id_to_delete = id.text
        try:
            id_to_delete = int(id_to_delete)
            query = "delete from faculty where ID={}".format(id_to_delete)
            cursor.execute(query)
            con.commit()
            if cursor.rowcount > 0:
                self.text_for_confirmation = "Data Deleted Successfully"
            else:
                self.text_for_confirmation = "Record not found"
        except:
            self.text_for_confirmation = "ID can only be Number"


CollegeManagerApp().run()