mabaedits
# TN Skills Robotics Competition - Master Plan

## 🎯 Project Overview
Raspberry Pi 5 robot for line following, QR code detection, color matching, and object manipulation.

---

## 1️⃣ COMPONENTS & THEIR PURPOSE

### 🧠 Raspberry Pi 5 (Main Controller)
- Runs **Python + OpenCV**
- Controls:
  - Motors (via L298)
  - Line sensors
  - Camera (QR + color)
  - Buzzer
- Handles **decision logic + state machine**

### 🚗 Motors + L298 Motor Driver
- Provides:
  - Direction control
  - Speed control (PWM)
- Drives robot movement in:
  - Line following
  - Free navigation
  - Turning for vision tasks

### 👁️ TCRT5000L – 5 Channel IR Line Sensor
- Used **ONLY in Zone A**
- Detects:
  - Black line (0)
  - White surface (1)
- Middle sensor used as **primary reference**

### 📷 Raspberry Pi Camera
- Used **ONLY in Zone B**
- Detects:
  - QR codes (`tn-red / tn-green / tn-blue`)
  - Wall colors
- Robot **stops before vision detection**

### 🔊 Buzzer
- Audio confirmation for:
  - End of Zone A
  - Each correct object placement
  - Final completion

### 🔋 External Battery
- Powers **ONLY motors via L298**
- Prevents Pi reboot / voltage drop

---

## 2️⃣ FINAL GPIO PIN MAP (ROBUST & CONFLICT-FREE)

### 🔌 L298 Motor Driver → Raspberry Pi 5

| Function              | L298 Pin  | Pi GPIO            | Notes         |
| --------------------- | --------- | ------------------ | ------------- |
| Left motor direction  | IN1       | GPIO 17            | Direction     |
| Left motor direction  | IN2       | GPIO 18            | Direction     |
| Right motor direction | IN3       | GPIO 22            | Direction     |
| Right motor direction | IN4       | GPIO 23            | Direction     |
| Left motor speed      | ENA       | GPIO 12            | PWM           |
| Right motor speed     | ENB       | GPIO 13            | PWM           |
| Common Ground         | GND       | GND                | **MANDATORY** |
| Motor Power           | +12V / VS | External Battery + | Motors only   |

### 👁️ TCRT5000L → Raspberry Pi 5

| Sensor Channel  | GPIO        |
| --------------- | ----------- |
| S1 (Leftmost)   | GPIO 5      |
| S2              | GPIO 6      |
| **S3 (Center)** | **GPIO 16** |
| S4              | GPIO 19     |
| S5 (Rightmost)  | GPIO 26     |
| VCC             | 5V          |
| GND             | GND         |

✔️ No PWM conflict  
✔️ No camera conflict  
✔️ Stable digital inputs

### 🔊 Buzzer

| Buzzer | GPIO    |
| ------ | ------- |
| +      | GPIO 21 |
| –      | GND     |

### 📷 Pi Camera
- Connected via **CSI ribbon**
- Uses **no GPIO pins**
- Accessed via OpenCV

---

## 3️⃣ TASKS & EXECUTION FLOW (ZONE-WISE)

### 🟩 ZONE A – LINE FOLLOWING (200 POINTS)

**Sensors Used:**
- TCRT5000L only

**Logic:**
- Read 5 sensors
- Center sensor priority
- Left/right correction using PWM

**Completion Condition:**
- Detect black end square
- Stop motors
- Play buzzer for 1 second

**State:**
```
STATE_LINE_FOLLOW
```

---

### 🟦 TRANSITION: ZONE A → ZONE B

**Actions:**
- Stop robot
- Disable IR reading
- Enable camera
- Switch state

```
STATE_QR_SCAN
```

---

### 🟨 ZONE B – QR CODE DETECTION (100 POINTS)

**Sensors Used:**
- Pi Camera

**Logic:**
- Robot stops
- Capture frame
- Decode QR text:
  - `tn-red`
  - `tn-green`
  - `tn-blue`

**Output:**
- Save detected color
- Short beep

---

### 🟥 ZONE B – COLOR DETECTION (100 POINTS)

**Sensors Used:**
- Pi Camera

**Logic:**
- Rotate slowly
- Detect wall color using HSV
- Match QR color

```
STATE_COLOR_LOCATE
```

---

### 🟪 ZONE B – OBJECT DRAG / PUSH (ATTEMPT)

**Mechanism:**
- Passive fork / front bumper
- Push object toward black drop box

**Logic:**
- Move forward slowly
- Use timed movement (no odometry)
- Stop after estimated distance

```
STATE_OBJECT_PUSH
```

⚠️ Partial success still gives points

---

### 🔊 BUZZER LOGIC

| Event             | Beep  |
| ----------------- | ----- |
| Zone A complete   | 1 sec |
| Correct placement | 1 sec |
| Final completion  | 5 sec |

---

## 4️⃣ MASTER STATE MACHINE (SIMPLE & SAFE)

```
START
 ↓
LINE_FOLLOW
 ↓
ZONE_A_COMPLETE → BEEP
 ↓
QR_SCAN
 ↓
COLOR_DETECT
 ↓
MOVE_TO_OBJECT
 ↓
PUSH_OBJECT
 ↓
BEEP
 ↓
REPEAT (for next color)
 ↓
FINAL_BEEP
STOP
```

---

## 🔥 FINAL ADVICE (VERY IMPORTANT)

- **DO NOT change pin map now**
- **DO NOT add new sensors**
- **Tune only PWM values**
- Focus on **Zone A stability first**

---

## 📁 Project Structure

```
tnskills/
├── README.md              # This file
├── config.py              # GPIO pin configuration
├── main.py                # Main state machine
├── motor_controller.py    # L298 motor control
├── line_sensor.py         # TCRT5000L sensor reading
├── camera_handler.py      # QR + color detection
├── buzzer.py              # Buzzer control
└── requirements.txt       # Python dependencies
```

