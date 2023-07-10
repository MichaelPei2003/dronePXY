import cv2
import numpy as np
import socket
import time
import pigpio
from dronekit import connect
import sys
sys.path.append("takeoff")
from arm_and_takeoff import arm_and_takeoff
from send_body_ned_velocity import send_body_ned_velocity
from aim import aim

vehicle = connect("192.168.130.182:14550", wait_ready=False) 

pi = pigpio.pi()  # 连接到pigpiod守护进程

servo_pin = 14
servo_min = 1000  # 舵机最小脉冲宽度
servo_max = 2000  # 舵机最大脉冲宽度
servo_mid = (servo_max - servo_min) / 2 + servo_min

pi.set_servo_pulsewidth(servo_pin, 0)  # 停止初始位置抖动
pi.set_servo_pulsewidth(servo_pin, servo_min)  # 最小位置

cap = cv2.VideoCapture(0)

# 设置编码参数
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

# 创建套接字
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 8000))
server_socket.listen(0)

print("等待地面站连接...")
client_socket, client_address = server_socket.accept()
print("地面站连接成功")

#client_socket.setblocking(False)
interval = 0.1  # 设置轮询间隔

run_servo = 0

#initialize PID parameter
ix = 0
iy = 0
last_error_x = 0
last_error_y = 0
flag_to_release = 0
flag_aimed = 1 #avoid getting 0 value

#takeoff and leave takeoff area
arm_and_takeoff(1, vehicle) #arm_and_takeoff(aTargetAltitude, vehicle)
for i in range(10):
    send_body_ned_velocity(0.8, 0, 0, vehicle)
    time.sleep(1)

while True:
    # 读取一帧图像
    ret, frame = cap.read()

    # 编码图像
    result, imgencode = cv2.imencode('.jpg', frame, encode_param)

    # 将图像转换成字符格式
    data = np.array(imgencode)
    stringData = data.tobytes()

    # 发送图像大小
    client_socket.send(str(len(stringData)).ljust(16).encode())

    # 发送图像数据
    client_socket.send(stringData)


#    显示图像
#    cv2.imshow('frame', frame)

    try:
         #接收数据
        coord = client_socket.recv(4096)
        coord_str = coord.decode("utf-8")
        if coord_str != '0':
            x, y, flag_servo = coord_str.split(",")
            bucket_x = int(x)
            bucket_y = int(y)
            print("(",x,",",y,")",flag_servo)
            if int(flag_servo) == 1 and run_servo == 0 :
                try:
                    pi.set_servo_pulsewidth(servo_pin, servo_max)  # 最大位置
                    time.sleep(1)
                    run_servo = 1
                except:
                     pass
        else:
            #如果没用检测到任何东西则直飞
            #如果一直未检测到目标飞行器不会自动停止！！！
            send_body_ned_velocity(0.8, 0, 0, vehicle)#(vx, vy, vz, vehicle)，单位m/s
            flag_aimed == 0
            print(0)
        print(flag_aimed)
        if flag_aimed == 0:    
            ix, iy, last_error_x, last_error_y, flag_aimed = aim(bucket_x, bucket_y, ix, iy, last_error_x, last_error_y, vehicle)
    
        #print('1')
    except BlockingIOError:
        # 如果没有新的数据到达，则等待一段时间再次尝试接收
        time.sleep(interval)
    except BrokenPipeError:
        time.sleep(interval)
    except ConnectionResetError:
        time.sleep(interval)
    except ValueError:
        # 关舵机
        pi.set_servo_pulsewidth(servo_pin, servo_min)  # 最小位置
        time.sleep(1)
        pi.set_servo_pulsewidth(servo_pin, 0)
        pi.stop()  # 断开与pigpiod守护进程的连接

        # 关闭连接
        client_socket.close()
        server_socket.close()

    except socket.error as e:
        # 发生其他错误，退出循循环
        print("Error receiving data:")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 关舵机
pi.set_servo_pulsewidth(servo_pin, servo_min)  # 最小位置
pi.set_servo_pulsewidth(servo_pin, 0)  
pi.stop()  # 断开与pigpiod守护进程的连接

# 关闭连接
client_socket.close()
server_socket.close()
