# Hand Gesture Control for Subway Surfers

A real-time hand gesture recognition system that lets you control Subway Surfers using your webcam. Use natural hand movements to play the game without touching your keyboard!

## 🎮 Controls

- **👆 Point UP** → Jump (Up Arrow)
- **👈 Point LEFT** → Steer Left (Left Arrow)
- **👉 Point RIGHT** → Steer Right (Right Arrow) 
- **✊ Make FIST** → Roll/Duck (Down Arrow)

## 🚀 Features

- **Ultra-low latency** (50ms response time)
- **Optimized for gaming** with minimal delay
- **Stable gesture detection** with anti-jitter technology
- **Natural hand movements** - no need for precise positioning
- **Real-time visual feedback** showing detected gestures

## 📋 Requirements

- Python 3.7-3.11
- Webcam
- OpenCV
- CVZone
- PyAutoGUI
- NumPy

## 🛠️ Installation

1. Clone this repository:
```bash
git clone https://github.com/AdamMHaq/subway-surfers-hand-control.git
cd subway-surfers-hand-control
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## 🎯 Usage

1. **Open Subway Surfers** in your browser and focus the game window
2. **Run the script**:
```bash
python testing.py
```
3. **Position your hand** in front of the webcam
4. **Use hand gestures** to control the game:
   - Point in different directions for movement
   - Make a fist for rolling/ducking
   - Keep hand open and flat for no input

5. **Press 'q'** in the camera window to quit

## ⚡ Performance Tips

- Ensure good lighting for better hand detection
- Keep your hand clearly visible in the camera frame
- The system processes every other frame for maximum speed
- Use a fist gesture for the fastest roll response

## 🔧 Configuration

You can adjust these settings in the code:

- `COOLDOWN_SECONDS`: Time between key presses (default: 0.05s)
- `DIRECTION_THRESHOLD`: Sensitivity for direction detection (default: 35°)
- `FRAME_WIDTH/HEIGHT`: Camera resolution (default: 160x120 for speed)
