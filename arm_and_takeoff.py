from dronekit import VehicleMode
import time 

def arm_and_takeoff(aTargetAltitude, vehicle):
    print("Basic pre-armchecks")
    #If problem occurs do following loop 
    while not vehicle.is_armable: 
        print(" Waiting for vehicle to initialise...") 
        print(vehicle.mode)
        if(vehicle.mode =='INITIALISING'):
            print("vehicle is initialising...")
        if(vehicle.gps_0.fix_type is None):
            print("gps_0.fix_type is None...")
        if(vehicle.gps_0.fix_type <= 1):
            print("gps_0.fix_type <= 1...")
        if(vehicle._ekf_predposhorizabs):
            print("EKF pre-arm is checking...")
        print(vehicle.mode != 'INITIALISING' and (vehicle.gps_0.fix_type is not None and vehicle.gps_0.fix_type > 1) and vehicle._ekf_predposhorizabs)
        time.sleep(1)
         
    #Pre-arm check passed, arm vehicle
    print("Arming motors...")
    vehicle.mode = VehicleMode("GUIDED")
    print("Vehicle mode: GUIDED")
    vehicle.armed = True
    print("Vehicle armed")
    
    #if not armed do following loop
    while not vehicle.armed:
        print("Waiting for arming...")
        time.sleep(1)
    
    print("Taking off")
    vehicle.simple_takeoff(aTargetAltitude)
    
    # 在无人机上升到目标高度之前，阻塞程序 
    while True: 
        print(" Altitude: ",vehicle.location.global_relative_frame.alt) 
        # 当高度上升到目标高度的0.95倍时，即认为达到了目标高度，退出循环 
        #vehicle.location.global_relative_frame.alt为相对于home点的高度 
        if vehicle.location.global_relative_frame.alt>= aTargetAltitude * 0.95: 
            print("Reached targetaltitude") 
            break 
        # 等待1s 
        time.sleep(1) 