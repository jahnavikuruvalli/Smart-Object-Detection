import cv2, serial, time, serial.tools.list_ports, threading
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio

# --- 1. Global state ---
state = {
    "camera_detected": False,
    "ldr_value": None,
    "mode": "camera",  # "camera" or "ldr"
    "port": None,
    "last_update": None
}

# --- 2. Arduino setup ---
def find_arduino_port():
    for p in serial.tools.list_ports.comports():
        if 'usbmodem' in p.device or 'usbserial' in p.device or 'Arduino' in p.description:
            return p.device
    raise RuntimeError("Arduino port not found. Plug it in and check Tools→Port in Arduino IDE.")

def init_arduino():
    port = find_arduino_port()
    arduino = serial.Serial(port, 9600, timeout=1)
    time.sleep(2)
    state["port"] = port
    return arduino

arduino = init_arduino()

# --- 3. FastAPI setup ---
app = FastAPI(title="Hybrid Detection API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # you can restrict to your frontend later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 4. Background detection thread ---
def detection_loop():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Cannot open camera.")
        return

    prev_gray = None
    no_motion_frames = 0
    MOTION_THRESHOLD = 5000
    NO_MOTION_LIMIT = 5

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if prev_gray is None:
            prev_gray = gray
            continue

        diff = cv2.absdiff(prev_gray, gray)
        _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
        motion = cv2.countNonZero(thresh)

        # --- Camera Detection Logic ---
        if motion > MOTION_THRESHOLD:
            arduino.write(b'1')
            state.update({
                "camera_detected": True,
                "mode": "camera",
                "ldr_value": None,
                "last_update": time.time()
            })
            no_motion_frames = 0
        else:
            no_motion_frames += 1
            if no_motion_frames > NO_MOTION_LIMIT:
                arduino.write(b'0')
                state.update({
                    "camera_detected": False,
                    "mode": "ldr",
                    "last_update": time.time()
                })
                no_motion_frames = 0

        # --- Read any response from Arduino (LDR values) ---
        if arduino.in_waiting > 0:
            line = arduino.readline().decode('utf-8').strip()
            if line.startswith("LDR Value:"):
                try:
                    val = int(line.split(":")[1].strip())
                    state["ldr_value"] = val
                except:
                    pass

        prev_gray = gray
        time.sleep(0.3)

    cap.release()
    arduino.close()

# --- 5. Start background thread ---
thread = threading.Thread(target=detection_loop, daemon=True)
thread.start()

# --- 6. API Endpoints ---
@app.get("/")
def root():
    return {"message": "Hybrid Camera + LDR system running", "arduino_port": state["port"]}

@app.get("/status")
async def get_status():
    """
    Returns real-time system status for the frontend
    """
    return {
        "mode": state["mode"],
        "camera_detected": state["camera_detected"],
        "ldr_value": state["ldr_value"],
        "last_update": state["last_update"]
    }

@app.post("/set-mode")
async def set_mode(mode: str):
    """
    Force a mode manually from frontend (optional)
    """
    if mode == "camera":
        arduino.write(b'1')
    elif mode == "ldr":
        arduino.write(b'0')
    else:
        return {"error": "Invalid mode"}
    state["mode"] = mode
    return {"message": f"Mode set to {mode}"}