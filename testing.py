"""
Hand-to-arrow mapper for Subway Surfers (using cvzone).
Maps hand gestures to arrow keys:
 - left  -> Left Arrow
 - right -> Right Arrow
 - up    -> Up Arrow (jump)
 - fist  -> Down Arrow (roll)

Usage:
  1. Open the game in your browser and focus the game window.
  2. Run this script. Position your hand in front of the webcam.
  3. Use different hand gestures to control:
       - Point left to steer left
       - Point right to steer right  
       - Point up to jump
       - Make a FIST to roll (down)
       - Hand flat/open with no clear direction = neutral (no input)

Author: ChatGPT (Optimized)
"""

import time
import collections
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import pyautogui

# ---------- Config ----------
FRAME_WIDTH = 160    # Even smaller for maximum speed
FRAME_HEIGHT = 120   # Even smaller for maximum speed

# Sensitivity threshold for direction detection (in degrees)
DIRECTION_THRESHOLD = 35.0  # Wider for more stable detection
MIN_CONFIDENCE_FRAMES = 1   # Immediate response

COOLDOWN_SECONDS = 0.05  # Ultra fast response (50ms)
SKIP_FRAMES = 1          # Process every other frame
STABILITY_THRESHOLD = 15 # Minimum distance for stable detection

# Disable pyautogui failsafe for better gaming experience
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0      # Remove default pause between commands

# ----------------------------
def is_roll_gesture(landmarks):
    """
    Fast fist detection for roll action.
    Returns True if hand is closed (fist = roll), False if fingers are extended.
    """
    # Use squared distances to avoid expensive sqrt calculations
    wrist_x, wrist_y = landmarks[0][0], landmarks[0][1]
    
    fingers_extended = 0
    
    # Check each finger using squared distances (faster than np.linalg.norm)
    finger_pairs = [(8, 6), (12, 10), (16, 14), (20, 18)]  # (tip, pip) pairs
    
    for tip_idx, pip_idx in finger_pairs:
        tip_x, tip_y = landmarks[tip_idx][0], landmarks[tip_idx][1]
        pip_x, pip_y = landmarks[pip_idx][0], landmarks[pip_idx][1]
        
        # Squared distance from wrist (avoid sqrt)
        tip_dist_sq = (tip_x - wrist_x)**2 + (tip_y - wrist_y)**2
        pip_dist_sq = (pip_x - wrist_x)**2 + (pip_y - wrist_y)**2
        
        if tip_dist_sq > pip_dist_sq:
            fingers_extended += 1
    
    # If 2 or fewer fingers are extended, it's a fist (roll action)
    return fingers_extended <= 2

def get_hand_gesture(landmarks):
    """
    Ultra-fast hand gesture detection with stability.
    Returns: 'roll' for fist, angle for pointing direction, or None for neutral.
    """
    # Check for fist (roll action) first - this is fastest
    if is_roll_gesture(landmarks):
        return 'roll'
    
    # Fast calculation using basic arithmetic
    wrist_x, wrist_y = landmarks[0][0], landmarks[0][1]
    
    # Use only middle and index finger for faster calculation
    avg_x = (landmarks[8][0] + landmarks[12][0]) / 2
    avg_y = (landmarks[8][1] + landmarks[12][1]) / 2
    
    # Direction vector
    dx = avg_x - wrist_x
    dy = avg_y - wrist_y
    
    # Stability check - must be pointing clearly in a direction
    distance_sq = dx*dx + dy*dy
    if distance_sq < STABILITY_THRESHOLD*STABILITY_THRESHOLD:
        return None  # Too close/ambiguous, consider neutral
    
    # Fast angle calculation
    import math
    angle = math.degrees(math.atan2(-dy, dx))
    return (angle + 360) % 360

def angle_to_direction(angle):
    """Fast angle to direction conversion (no down direction - fist is used for roll)."""
    # Simplified range checking for speed - only left, right, up
    if angle <= DIRECTION_THRESHOLD or angle >= (360 - DIRECTION_THRESHOLD):
        return 'right'
    elif (90 - DIRECTION_THRESHOLD) <= angle <= (90 + DIRECTION_THRESHOLD):
        return 'up'
    elif (180 - DIRECTION_THRESHOLD) <= angle <= (180 + DIRECTION_THRESHOLD):
        return 'left'
    # No down direction - fist handles roll action
    return None

def send_key(key):
    """Send key press with error handling."""
    try:
        pyautogui.press(key)
        print(f"Sent key: {key} at {time.time():.2f}")
    except Exception as e:
        print(f"Error sending key: {e}")

def main():
    """Ultra-optimized main function with minimal latency."""
    cap = cv2.VideoCapture(0)
    
    # Aggressive camera optimization for speed
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
    cap.set(cv2.CAP_PROP_FPS, 60)  # Higher FPS for responsiveness
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Minimize buffer lag
    cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)  # Disable autofocus to reduce jitter
    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)  # Reduce auto-exposure
    
    detector = HandDetector(detectionCon=0.6, maxHands=1)  # Lower for max speed

    last_sent = {'left': 0, 'right': 0, 'up': 0, 'down': 0}
    frame_count = 0
    last_gesture = None  # For stability

    print("Starting OPTIMIZED hand gesture control:")
    print("- Point UP to JUMP")
    print("- Point LEFT/RIGHT to STEER") 
    print("- Make a FIST to ROLL (much faster!)")
    print("- Hand flat/open = NEUTRAL (no input)")
    print("Focus your browser with the game tab. Press 'q' to quit.")

    while True:
        success, img = cap.read()
        if not success:
            break

        frame_count += 1
        
        # More aggressive frame skipping for ultra-low latency
        if frame_count % (SKIP_FRAMES + 1) != 0:
            # Still show frame but don't process - reduces jitter
            if frame_count % 4 == 0:  # Update display less frequently
                cv2.imshow("Hand Control (q=quit)", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            continue

        # Mirror once and store to avoid repeated flipping
        img = cv2.flip(img, 1)
        
        # Minimal hand detection - no visual processing
        hands, _ = detector.findHands(img, flipType=False, draw=False)

        action = None

        if hands:
            hand = hands[0]
            landmarks = hand["lmList"]
            
            try:
                # Get gesture (roll, angle, or None)
                gesture = get_hand_gesture(landmarks)
                
                if gesture == 'roll':
                    direction = 'down'  # Fist = roll (down arrow)
                elif isinstance(gesture, (int, float)):
                    direction = angle_to_direction(gesture)
                else:
                    direction = None
                
                # Stability check - only change if gesture is consistent or significantly different
                if direction != last_gesture:
                    if direction is not None:  # New valid gesture
                        last_gesture = direction
                    elif last_gesture is not None:  # Lost gesture, wait a bit before going neutral
                        direction = last_gesture  # Keep last direction briefly
                
                # Minimal, stable visual feedback (only update when necessary)
                if landmarks and frame_count % 3 == 0:  # Update visual less frequently
                    wrist = landmarks[0]
                    if gesture == 'roll':
                        cv2.circle(img, (wrist[0], wrist[1]), 15, (0, 0, 255), 2)
                    elif isinstance(gesture, (int, float)):
                        # Simpler line drawing
                        avg_x = int((landmarks[8][0] + landmarks[12][0]) / 2)
                        avg_y = int((landmarks[8][1] + landmarks[12][1]) / 2)
                        cv2.line(img, (wrist[0], wrist[1]), (avg_x, avg_y), (0, 255, 0), 2)
                
                # Simple status display (update less frequently)
                if frame_count % 5 == 0:
                    status_text = "ROLL" if direction == 'down' else (direction.upper() if direction else "OK")
                    status_color = (0, 0, 255) if direction == 'down' else ((0, 255, 0) if direction else (255, 255, 255))
                    cv2.putText(img, status_text, (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, status_color, 2)

                # Send key if direction detected and cooldown passed
                now = time.time()
                if direction and now - last_sent[direction] > COOLDOWN_SECONDS:
                    action = direction
                    last_sent[direction] = now

                # Ultra-fast key sending with minimal cooldown
                now = time.time()
                if direction and now - last_sent[direction] > COOLDOWN_SECONDS:
                    action = direction
                    last_sent[direction] = now

            except Exception:
                pass  # Silent error handling for max speed

        # Send key action immediately
        if action:
            send_key(action)

        # Reduced display updates to prevent jitter
        if frame_count % 2 == 0:  # Update display every other processed frame
            cv2.imshow("Hand Control", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
