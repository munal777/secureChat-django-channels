from channels.consumer import SyncConsumer

class EchoConsumer(SyncConsumer):

    def websocket_connect(self, event):
        self.send({
            "type": "websocket.accept",
        })

    def websocket_receive(self, event):
        text = event.get("text","")

        if text.lower() == "hi":
            response = "Hello! how may I help you!"
        elif text.lower() == "bye":
            response = "Goodbye!"
        else:
            response = f"Client message: {text}"

        self.send({
            "type": "websocket.send",
            "text": response,
        })