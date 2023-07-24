from ClientSocket import ClientSocket


class Controller:
    def __init__(self):
        self._connect_client_Function('127.0.0.1', 7001)

    def _connect_client_Function(self, ip_, port_):
        self.clientconnect = ClientSocket()
        self.clientconnect.clientsocket_Setting(ip_, port_)

    def client_to_server(self, header, msg):
        send_data = f'{header}:{msg}'
        self.clientconnect.client_Send_Function(send_data)
