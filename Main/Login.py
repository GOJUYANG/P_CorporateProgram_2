from Controller import Controller

class LoginFunction:
    def __init__(self):
        self.clientconnect_Function()

    def controller_connect_Function(self):
        """컨트롤러와 이어주는 기능"""
        self.Controller = Controller()

    def input_Function(self):
        """데이터 입력 하는 기능"""
        data = input()
        return data

    def controller_to_send(self):
        self.input_Function()




