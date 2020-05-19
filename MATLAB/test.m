%Dit is een test voor Git met Matlab. 
global k_v R_m k_t
T_max = 11.67; %mNm
i_max = 0.54; %A
i_min = 0.05; %A
V = 12; %V
no_load_rpm = 4500; %rpm

k_t = T_max / i_max; %mNm/A

T_friction = k_t * i_min; %mNm
R_m = V / i_max; %Ohm

k_rpm = no_load_rpm / (V + i_min * R_m); %rpm/Volt

k_v =  30 / pi / k_rpm; %Volt / (rad/s)

[V_ex, I_ex, T_e] = motor_calculations(1000, 100000000);
a = 600 * k_t / 1000;

function [V, I, T] = motor_calculations(omega, R_load)
    global k_v R_m k_t
    V = k_v * omega;
    I = V / (R_m + R_load);
    T = k_t * I;
end




