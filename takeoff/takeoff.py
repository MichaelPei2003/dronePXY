from dronekit import connect
from arm_and_takeoff import arm_and_takeoff

#connect to drone 
connection_string ='/dev/ttyACM0' #Com of current FCM connection
print('Connectingto vehicle on: %s' % connection_string) 
vehicle = connect(connection_string, wait_ready=False) 


arm_and_takeoff(1, vehicle) #arm_and_takeoff(aTargetAltitude, vehicle)

print("起飞测试程序运行结束，请接管飞行器...")