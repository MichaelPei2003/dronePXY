from send_body_ned_velocity import send_body_ned_velocity

def aim(bucket_x, bucket_y, ix, iy, last_error_x, last_error_y, vehicle):
    flag = 0#flag aimed
    # PID
    dt = 0.1
    kp = 0.2  # 比例参数
    ki = 0.1  # 积分参数
    kd = 0.5  # 微分参数
    
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
    
    print("sending SPD: ", vx, ", ", vy)
    
    send_body_ned_velocity(vx, vy, vehicle)
    
    if abs(error_x) < 10 and abs(error_y) < 10:
        flag = 1
        
    return ix, iy, last_error_x, last_error_y, flag
