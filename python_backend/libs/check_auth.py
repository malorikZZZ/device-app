from sanic import response
import requests, json


class Auth_checker():

    token = ''
    url_is = 'http://yabt-test/identity/connect/userinfo'
    check_user = ''
    device_id = ''
    DB = ''
    users = ''
    data = ''

    def __init__(self, token, check_user=False, device_id='', db_conn=''):
        if token:
            self.token = token
            self.__check_token()

        if check_user and device_id and db_conn:
            self.check_user = True
            self.device_id = device_id
            self.DB = db_conn


    def __get_device_login(self):

        #get device.login from DB via db_connector
        self.DB.get_device(self.device_id)
        self.login = 'test'


    def __check_users(self):
        self.__get_device_login()
        if self.login == self.data['sub']:
            return True
        else:
            return False

    def __check_token(self):

        headers = {'Authorization': self.token, 'accept': 'application/json'}

        try:
            resp = requests.get(self.url_is, headers=headers)
        except:
            return False
        if resp.status_code != int(200):
            return False
        else:
            self.data = json.loads(resp.text)
            if self.check_user:
                self.__check_users()
            else:
                return True
