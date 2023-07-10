from dronekit import connect
from send_body_ned_velocity import send_body_ned_velocity
from arm_and_takeoff import arm_and_takeoff

vehicle = connect('/dev/ttyACM0', wait_ready=False)

arm_and_takeoff(1, vehicle)

while True:
    send_body_ned_velocity(1, 0, 0, vehicle)