"""import  cv2, serial, time, serial.tools.list_ports

# --- 1. Auto-detect Arduino port on macOS ---
def find_arduino_port():
    for p in serial.tools.list_ports.comports():
        if 'usbmodem' in p.device or 'usbserial' in p.device or 'Arduino' in p.description:
            return p.device
    raise RuntimeError("Arduino port not found. Plug it in and check Tools→Port in Arduino IDE.")

port = find_arduino_port()
print("Using port:", port)

arduino = serial.Serial(port, 9600, timeout=1)
time.sleep(2)  # allow Arduino to reset

# --- 2. Open built-in camera ---
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError(
        "Cannot open camera. Allow Terminal/Python under System Settings → Privacy & Security → Camera."
    )

prev_gray = None
no_motion_frames = 0
MOTION_THRESHOLD = 5000
NO_MOTION_LIMIT = 5

print("Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if prev_gray is None:
        prev_gray = gray
        cv2.imshow("Camera", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        continue

    diff = cv2.absdiff(prev_gray, gray)
    _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
    motion = cv2.countNonZero(thresh)

    if motion > MOTION_THRESHOLD:
        arduino.write(b'1')
        print("📷 Object detected by camera")
        no_motion_frames = 0
    else:
        no_motion_frames += 1
        if no_motion_frames > NO_MOTION_LIMIT:
            arduino.write(b'0')
            print("⚙  No camera object → switching to LDR mode")
            no_motion_frames = 0

    prev_gray = gray
    cv2.imshow("Camera", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()"""