from dronekit import connect, VehicleMode
from arm_and_takeoff import arm_and_takeoff
import time

#connect to drone
connection_string ='192.168.130.160:14550' #RPI's IP, port is always 14550
print('Connectingto vehicle on: %s' % connection_string) 
vehicle = connect(connection_string, wait_ready=False) 
arm_and_takeoff(5, vehicle) #arm_and_takeoff(aTargetAltitude, vehicle)

time.sleep(10)

vehicle.mode = VehicleMode("RTL")