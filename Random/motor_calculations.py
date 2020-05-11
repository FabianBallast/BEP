def find_kt(T_max, U, R):
    counter_torque = T_max
    i = U / R

    return round(counter_torque / i, 2)

def find_equi_vel(kt, T_fric, T_aero, T_wind, R_load, R_motor):

    T_counter_torque = T_wind - T_aero - T_fric
    i = T_counter_torque / kt
    E = i * (R_load + R_motor)
    
    return round(E / kt, 2)

print(find_equi_vel(8.59, 0.06, 0.15, 4, 4, 800.2))