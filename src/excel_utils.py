import base64
import numpy
import pandas as pd
from openpyxl import load_workbook
from pandas import ExcelWriter
from xlrd import XLRDError


class ExcelFields:
    NAME = "Name"
    EMAIL = "Email"
    PHONE = "Mobile"
    PASSWORD = "Password"


class ExcelDB:
    FIELDS_LIST = [ExcelFields.NAME, ExcelFields.EMAIL, ExcelFields.PHONE, ExcelFields.PASSWORD]

    def __init__(self):
        self.writer = None
        self.file_path = ''

    def open_excel(self, file_path):
        self.file_path = file_path
        # Create a Pandas Excel writer using Openpyxl XlsxWriter as the engine
        self.writer = ExcelWriter(self.file_path, engine='openpyxl')

    def is_exist(self, email, phone=False):
        user_rows = self.read_user()
        for row in user_rows:
            if len(row) > 2:
                email_add = row[1]
                phone_no = row[2]
                if email_add == email:
                    return row
                if phone and phone == phone_no:
                    return row

        return False

    @staticmethod
    def __encode_password(payload):
        password = payload['password'].strip().encode("utf-8")
        return base64.b64encode(password)

    def write_user(self, payload):
        user = self.is_exist(payload['email'], phone=payload['phone'])
        if not isinstance(user, numpy.ndarray):

            # Encode Password In Base64
            password = self.__encode_password(payload)

            payload = {self.FIELDS_LIST[0]: [payload.get('name')], self.FIELDS_LIST[1]: [payload.get('email')],
                       self.FIELDS_LIST[2]: [payload.get('phone')], self.FIELDS_LIST[3]: [password]}
            # Dataframe User
            df = pd.DataFrame(payload)
            self.writer.book = load_workbook(self.file_path)
            # copy existing sheets
            self.writer.sheets = dict((ws.title, ws) for ws in self.writer.book.worksheets)
            # read existing file
            reader = pd.read_excel(r'users.xlsx')
            # write out the new sheet
            df.to_excel(self.writer, index=False, header=False, startrow=len(reader) + 1)

            self.writer.close()
            print("New User Added Successfully...")
            return True
        print("User Already Exist..., Please try with different email/phone")
        return False

    def read_user(self):
        try:
            data = pd.read_excel(self.file_path)
            return data.values
        except XLRDError as e:
            self.writer = ExcelWriter(self.file_path, engine='xlsxwriter')
            return []

    def close(self):
        pass


class Authenticate(ExcelDB):

    def __init__(self, excel_db_path):
        super().__init__()
        super().open_excel(excel_db_path)

    @staticmethod
    def verify_password(user, password):
        encoded_pass = user[3].replace('b\'', '')
        encoded_pass = encoded_pass.replace('\'', '')
        decoded_pass = base64.b64decode(encoded_pass.encode("utf-8"))
        return True if decoded_pass.decode("utf-8") == password else False

    def authenticate(self, email, password):
        user = self.is_exist(email)
        if isinstance(user, numpy.ndarray):
            if self.verify_password(user, password):
                print("User Authenticated Successfully")
            else:
                print("Invalid Credentials")
            return
        print("User Not Found")
        return False
