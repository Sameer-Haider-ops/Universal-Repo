from machine import Pin
import time

# Configure the IR sensor on Pin 16 with a pull-up resistor
ir_sensor = Pin(5, Pin.IN, Pin.PULL_UP)

# Configure the onboard LED as an output and keep it off (0)
led = Pin("LED", Pin.OUT)
led.value(0)

print("IR sensor monitoring for 1 -> 0 transition started...")

# Keep track of the previous sensor state
previous_state = ir_sensor.value()

while True:
    current_state = ir_sensor.value()
    
    # Detect transition from 1 to 0 (since active-LOW: 1 means clear, 0 means object)
    if previous_state == 1 and current_state == 0:
        print("Detected")
    
    # Update the previous state for the next check
    previous_state = current_state
    
    # Small delay to debounce/prevent spamming
    time.sleep(0.05)
    