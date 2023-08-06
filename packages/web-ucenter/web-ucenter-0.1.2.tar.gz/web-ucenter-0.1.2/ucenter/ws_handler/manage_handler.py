from tornado import websocket, gen
import json


class ManageHandler(websocket.WebSocketHandler):
    def data_received(self, chunk):
        print('data_received')

    def check_origin(self, origin):
        print('check_origin')
        return True

    def open(self):
        print("WebSocket opened")

    @gen.coroutine
    def on_message(self, message):
        try:
            req = json.loads(message)

            if 'method' in req:
                method = req['method']

                self.write_message('success')
            else:
                self.write_message(u'Missing method in request')

        except json.JSONDecodeError:
            self.write_message(u'Not valid JSON message')

    def on_close(self):
        print("WebSocket closed")
