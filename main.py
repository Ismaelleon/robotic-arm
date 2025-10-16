from servo import Servo
from microdot import Microdot
from websocket import with_websocket
import network

# Initialize servo motors
#rotation = Servo(pin=22)
#shoulder = Servo(pin=21)
#elbow = Servo(pin=20)

def connect_wifi():
    sta_if = network.WLAN(network.WLAN.IF_STA)
    if not sta_if.isconnected():
        print("connecting to network...")
        sta_if.active(True)
        sta_if.connect("Ismael", "06072012")
        while not sta_if.isconnected():
            pass
    print(f"server running on http://{sta_if.ipconfig("addr4")[0]}:5000")
    connected = True

    start_server()

def start_server():
    app = Microdot()

    # Serve page
    @app.route("/")
    async def index(request):
        html_file = open("static/index.html")
        return html_file, 200, {"Content-Type": "text/html"}

    # Websockets route
    @app.route("/ws")
    @with_websocket
    async def ws(request, ws):
        while True:
            data = await ws.receive()
            print(data)

    app.run()

connect_wifi()
