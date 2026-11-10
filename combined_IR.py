from machine import Pin
import time

# Configure Sensor A and Sensor B with pull-up resistors
sensor_a = Pin(5, Pin.IN, Pin.PULL_UP)
sensor_b = Pin(16, Pin.IN, Pin.PULL_UP)

# Configure the onboard LED as an output and keep it off (0)
led = Pin("LED", Pin.OUT)
led.value(0)

print("Directional Door Monitor Started...")

# Track previous states for edge detection (1 -> 0 transition)
prev_a = sensor_a.value()
prev_b = sensor_b.value()

# Timeout window (in seconds) to complete the full crossing sequence
sequence_timeout = 1.0  
triggered_sensor = None
timer_start = 0

while True:
    led.value(0) # Ensure LED remains off
    
    curr_a = sensor_a.value()
    curr_b = sensor_b.value()
    
    current_time = time.time()
    
    # Check if a timeout occurred waiting for the second sensor
    if triggered_sensor and (current_time - timer_start > sequence_timeout):
        triggered_sensor = None # Reset sequence if too much time passed
    
    # Detect 1 -> 0 transition on Sensor A
    if prev_a == 1 and curr_a == 0:
        if triggered_sensor == 'B':
            print("Leaving")  # B triggered first, then A -> Leaving
            triggered_sensor = None
        else:
            triggered_sensor = 'A'
            timer_start = time.time()
            
    # Detect 1 -> 0 transition on Sensor B
    if prev_b == 1 and curr_b == 0:
        if triggered_sensor == 'A':
            print("Entering") # A triggered first, then B -> Entering
            triggered_sensor = None
        else:
            triggered_sensor = 'B'
            timer_start = time.time()
            
    # Update previous states
    prev_a = curr_a
    prev_b = curr_b
    
    # Small delay for stability and CPU breathing room
    time.sleep(0.02)