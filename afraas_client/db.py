import mysql.connector
import os
from dotenv import load_dotenv
from pathlib import Path


class db:
    def __init__(self) -> None:
        dotenv_path = Path(r'AFRAAS\resources\user.env')
        load_dotenv(dotenv_path = dotenv_path)
        self.conn = mysql.connector.connect(
            host="sql12.freemysqlhosting.net",
            user=os.getenv('AFRAAS_USER'),
            password=os.getenv('AFRAAS_PASSWORD'),
            database=os.getenv('AFRAAS_DATABASE'),
        )

    def check(self):
        cursor = self.conn.cursor()
        cursor.execute("select table_name, table_type, table_schema from information_schema.TABLES where table_schema like 'sql12606276';")
        check = ('attendance', 'departments', 'shifts', 'users')
        db_tables = []
        for table in cursor:
            db_tables.append(str(table[0]).lower())
        
        # print(db_tables)
        for table in check:
            if table not in db_tables:
                print(table," is not there")
                return False
        
        return True

    def addNewUser(self,name, dept_id, shift_id):
        cursor = self.conn.cursor()
        cursor.execute("show databases")
        pass
    def deleteUser(self, user_id, name=""):
        pass
    def updateUserDetails(self, user_id, args):
        pass
    def doesExist(self, user_id):

        pass
    # def getUserId(self, name):
    #     cursor = self.conn.cursor()
    #     cursor.execute(f'''
    #         SELECT user_id from Users where name like '{name}' ''')
        
    #     res = cursor.fetchall()
    #     if 

    #     if res == None:
    #         return -1
    #     else:
    #         return res[0]


    def addNewDept(self, dept_name):
        
        pass
    def updateDeptName(self, dept_id, new_name):
        pass
    def deleteDept(self, dept_id):
        pass
    def viewAllDepts(self):
        pass

    def addNewShift(self, time_in, time_out):
        pass
    def updateShift(self, shift_id, time_in=0, time_out=0):
        pass
    def deleteShift(self, shift_id):
        pass
    def viewAllShifts(self):
        pass

    def markAttendance(self, name, status):
        pass
    def viewAttendanceTable(self, From, To):
        pass

    def executeCustomQuery(self, query):
        pass
    
    def createTables(self):
        cursor = self.conn.cursor()
        cursor.execute("show databases")
        message = "DataBase is set up"
        
        # for x in cursor:
        #     print(x)

        try:
            cursor.execute('''
            CREATE TABLE Departments(
                dept_id int,
                dept_name VARCHAR(255),
                PRIMARY KEY(dept_id)
            ); ''')
        except:
            print("Departments table is already there")
        

        try:
            cursor.execute('''
            CREATE TABLE Shifts(
                shift_id int,
                time_in TIME, 
                PRIMARY KEY(shift_id)
            ); ''')
        except:
            print("Shifts table is already there")

        try:
            cursor.execute('''
            CREATE TABLE Users(
                name VARCHAR(255) NOT NULL,
                dept_id int, 
                shift_id int NOT NULL,
                user_id int,
                PRIMARY KEY (user_id),
                FOREIGN KEY (dept_id) REFERENCES Departments (dept_id),
                FOREIGN KEY (shift_id) REFERENCES Shifts (shift_id)
            ); ''')
        except:
            print("Users table is already there")

        try:
            cursor.execute('''
            CREATE TABLE Attendance(
                rec_id int,
                time_stamp TIME,
                status enum("enter", "exit", "absent"),
                user_id int,
                PRIMARY KEY (rec_id),
                FOREIGN KEY (user_id) REFERENCES Users(user_id)
            ); ''')
        except:
            print("Attendance table is already there")
        
        print(message)