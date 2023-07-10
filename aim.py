from send_body_ned_velocity import send_body_ned_velocity
import math

def aim(bucket_x, bucket_y, ix, iy, last_error_x, last_error_y, vehicle):
    flag = 0#flag aimed
    # PID
    dt = 0.1
    kp = 0.0002  # 比例参数
    ki = 0.0001  # 积分参数
    kd = 0.0005  # 微分参数
    
    self_x = 320
    self_y = 240
    
    error_x = bucket_x - self_x
    error_y = bucket_y - self_y
    
    px = error_x
    py = error_y
    ix += error_x * dt
    iy += error_y * dt
    dx = (error_x - last_error_x)/dt
    dy = (error_y - last_error_y)/dt
    last_error_x = error_x
    last_error_y = error_y
    vx = kp * px + ki * ix + kd * dx
    vy = kp * py + ki * iy + kd * dy
    
    send_body_ned_velocity(vx, vy, vehicle)
    
    if abs(error_x) < 1 and abs(error_y) < 1:
        flag = 1
        
    return ix, iy, last_error_x, last_error_y, flag
