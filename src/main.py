# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from excel_utils import ExcelDB, Authenticate

FILE_PATH = '../users.xlsx'


def validate_payload(payload):
    is_valid = True
    name = payload.get("name")
    email = payload.get('email')
    phone = payload.get('phone')
    password = payload.get('password')
    if not name:
        print("Name is required")
        is_valid = False
    if not email:
        print("Email is required")
        is_valid = False
    if not phone:
        print("Phone is required")
        is_valid = False
    if not password:
        print("Password is required")
        is_valid = False
    return is_valid


def signup_user(payload):
    if validate_payload(payload):
        edb = ExcelDB()
        edb.open_excel(FILE_PATH)
        edb.write_user(payload)


def login_user():
    auth = Authenticate(excel_db_path=FILE_PATH)
    auth.authenticate('sada4@gmail.com', 'mahesh')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    user_payload = {'name': 'Sadashive Bhosale', 'email': 'sada4@gmail.com', 'phone': '89287638768', 'password': 'mahesh'}
    signup_user(user_payload)
    # login_user()
