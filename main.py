from servo import Servo
from microdot import Microdot
from websocket import with_websocket
import network, asyncio

# Initialize servo motors
rotation_servo = Servo(pin=26)
shoulder_servo = Servo(pin=27)
elbow_servo = Servo(pin=25)
hand_servo = Servo(pin=33)

# Set buttons data
buttons = {
    "right": False,
    "left": False,
    "up": False,
    "down": False,
    "elbow-up": False,
    "elbow-down": False,
    "hand-open": False,
    "hand-close": False,
}

vel = 5
url = ""

# Set initial position
rotation_servo.move(45)
shoulder_servo.move(45)
elbow_servo.move(45)
hand_servo.move(0)


def connect_wifi():
    sta_if = network.WLAN(network.WLAN.IF_STA)
    if not sta_if.isconnected():
        print("connecting to network...")
        sta_if.active(True)
        sta_if.connect("Ismael", "06072012")
        while not sta_if.isconnected():
            pass
    global url
    url = f"http://{sta_if.ipconfig("addr4")[0]}:5000"
    print(f"server running on {url}")
    connected = True

    start_server()


def buttons_control(data):
    # Rotation
    if data == "btn-right pressed":
        buttons["right"] = True
    elif data == "btn-right":
        buttons["right"] = False

    if data == "btn-left pressed":
        buttons["left"] = True
    elif data == "btn-left":
        buttons["left"] = False

    # Shoulder
    if data == "btn-up pressed":
        buttons["up"] = True
    elif data == "btn-up":
        buttons["up"] = False

    if data == "btn-down pressed":
        buttons["down"] = True
    elif data == "btn-down":
        buttons["down"] = False

    # Elbow 
    if data == "btn-elbow-up pressed":
        buttons["elbow-up"] = True
    elif data == "btn-elbow-up":
        buttons["elbow-up"] = False 

    if data == "btn-elbow-down pressed":
        buttons["elbow-down"] = True
    elif data == "btn-elbow-down":
        buttons["elbow-down"] = False 

    # Hand
    if data == "btn-hand-open pressed":
        buttons["hand-open"] = True
    elif data == "btn-hand-open":
        buttons["hand-open"] = False

    if data == "btn-hand-close pressed":
        buttons["hand-close"] = True
    elif data == "btn-hand-close":
        buttons["hand-close"] = False




async def movement_loop():
    while True:
        movement()
        await asyncio.sleep(0.05)

def movement():
    print("\x1b[2J\x1b[H")
    print(f"server running on {url}")
    print(f"Rotation Servo: {rotation_servo.current_angle}°")
    print(f"Shoulder Servo: {shoulder_servo.current_angle}°")
    print(f"Elbow Servo: {elbow_servo.current_angle}°")
    print(f"Hand Servo: {hand_servo.current_angle}°")

    # Rotation
    if buttons["right"] == True and rotation_servo.current_angle < 170:
        rotation_servo.move(rotation_servo.current_angle + vel)
    elif buttons["left"] == True and rotation_servo.current_angle > 10:
        rotation_servo.move(rotation_servo.current_angle - vel)

    # Shoulder
    if buttons["up"] == True and shoulder_servo.current_angle < 170:
        shoulder_servo.move(shoulder_servo.current_angle + vel)
    elif buttons["down"] == True and shoulder_servo.current_angle > 10:
        shoulder_servo.move(shoulder_servo.current_angle - vel)

    # Elbow
    if buttons["elbow-up"] == True and elbow_servo.current_angle < 170:
        elbow_servo.move(elbow_servo.current_angle + vel)
    elif buttons["elbow-down"] == True and elbow_servo.current_angle > 10:
        elbow_servo.move(elbow_servo.current_angle - vel)

    # Hand
    if buttons["hand-open"] == True and hand_servo.current_angle < 90:
        hand_servo.move(hand_servo.current_angle + vel)
    elif buttons["hand-close"] == True and hand_servo.current_angle > 10:
        hand_servo.move(hand_servo.current_angle - vel)


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
            buttons_control(data.strip())

    loop = asyncio.get_event_loop()
    loop.create_task(movement_loop())
    app.run()

connect_wifi()
