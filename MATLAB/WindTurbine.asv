%%#####################Fan###########
air_flow_fan = 222.6/3600; %m3/s,  org: 222.6 m3/h
rpm_fan      = 3300; %rpm

P_in_fan     = 22; %W
diameter_fan = 0.12; %m

diverge_angle = 20; %degrees

%%###################Turbine##############
d_turb_to_fan = 0.05; %m, distance between turbine and fan
diameter_turbine = 0.15; %m


%%###assumptions#########
%# - all produced air flow reaches the turbine
%# - the air flow of the fan diverges with an angle of approximately 20 degrees
%# - temperature of the air is 20 degrees Celsius


fprintf('\n')
%##############################Calculations#################
A_fan = ((diameter_fan/2)^2 - (0.065/2)^2)*pi;
air_speed_fan_out = air_flow_fan/A_fan;
fprintf('Air speed of outflow fan:            %.2f m/s \n',air_speed_fan_out)

diameter_diverged_flow = diameter_fan + 2*tan(deg2rad(diverge_angle))*d_turb_to_fan; 
A_diverged_flow = ((diameter_diverged_flow/2)^2 *pi);
air_speed_turbine_in = air_flow_fan/A_diverged_flow;

fprintf('Air speed of inflow turbine:         %.2f m/s \n',air_speed_turbine_in)

desired_tip_speed_ratio_lambda = 2.1; %see research

angular_velocity_desired = 2*desired_tip_speed_ratio_lambda*air_speed_turbine_in/diameter_turbine;  %rad/s
rpm_desired_turbine = angular_velocity_desired/(2*pi) *60;
fprintf('Optimal turbine rpm:                 %.2f rpm \n',rpm_desired_turbine)

%%%%%%Reynolds 
rho = 1.225; %kg/m3
nu = 1.516e-5; %m^2/s
chord_length = 0.01971;

Reynolds_turbine = air_speed_turbine_in*chord_length/nu; %Re
fprintf('Reynolds number of inflow turbine:   %.2f\n',Reynolds_turbine)

%%%%%%% DC MOTOR BEREKENINGEN %%%%%%%%
C_T = 0.6;
n = rpm_desired_turbine/60; %omw/s
turbine_thrust = 1000*0.5*rho*(pi/4*diameter_fan^2)*air_speed_turbine_in^2*C_T; %N
turbine_torque = turbine_thrust*diameter_fan/2;
fprintf('Torque deliverd by turbine:          %.2f mNm \n',turbine_torque) %given lambda = 2.1

max_torque = 11.67; %mNm
nominal_voltage = 12; %V
noload_voltage = 6; %V
min_current = 0.05; %A
max_current = 0.54; %A

%%%%% Kt and torque estimates %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
omega_noload = 220*2*pi; %rad/s
K_v = omega_noload/(nominal_voltage - noload_voltage);
K_t = 60*1000/(2*pi*K_v); %mNm/A
fprintf('estimated torque constant:           %.2f mNm/A \n',K_t)

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
k_t_motor = (max_torque)/(max_current-min_current); %mNm/A
fprintf('Torque constant of DC motor:         %.2f mNm/A \n',k_t_motor)

terminal_resistance = nominal_voltage/max_current; %Ohm
fprintf('estimated terminal resistance:       %.2f Ohm \n',terminal_resistance)

load = 200; %Ohm


turbine_torque_netto = turbine_torque;

i = turbine_torque_netto / k_t_motor; %A
r_tot = terminal_resistance + load; %Ohm
omega_1 = i * r_tot / (k_t_motor / 1000); %rad/s


%omega = (30/pi)*(turbine_torque*(terminal_resistance + resistance)/(k_t_motor^2)); %rpm
omega = omega_1 * 30 / pi;
fprintf('Rotational speed of DC motor:        %.2f rpm \n',omega)

back_emf = k_t_motor/1000*omega*(pi/30); %V
fprintf('estimated DC motor voltage:          %.2f V \n',back_emf)

DC_power = 1000*back_emf^2/(load + terminal_resistance);
fprintf('estimated DC motor power:            %.2f mW \n',DC_power)

















