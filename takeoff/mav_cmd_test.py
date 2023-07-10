from dronekit import connect, VehicleMode
from pymavlink import mavutil

#connect to drone 
connection_string ='192.168.31.85:14550' #Com of current FCM connection
vehicle=connect(connection_string, wait_ready = False)

print("connected")

vehicle.mode = VehicleMode("GUIDED")
vehicle.armed = True

# vehicle.simple_takeoff(1)

def takeoff(alt, self):
    altitude = float(alt)
    self._master.mav.command_long_send(0, 0, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
                                          0, 0, 0, 0, 0, 0, 1, altitude)

takeoff(2, vehicle)