%%#####################Fan###########
air_flow_fan = 222.6 /3600; %m3/s,  org: 222.6 m3/h
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


fprintf('\n')
%##############################Calculations#################
A_fan = ((diameter_fan/2)^2 *pi);
air_speed_fan_out = air_flow_fan/A_fan;
fprintf('Air speed of outflow fan:   %.2f m/s \n',air_speed_fan_out)

diameter_diverged_flow = diameter_fan + 2*tan(deg2rad(diverge_angle))*d_turb_to_fan; 
A_diverged_flow = ((diameter_diverged_flow/2)^2 *pi);
air_speed_turbine_in = air_flow_fan/A_diverged_flow;

fprintf('Air speed of inflow turbine:   %.2f m/s \n',air_speed_turbine_in)


desired_tip_speed_ratio_lambda = 2.1; %see research

angular_velocity_desired = 2*desired_tip_speed_ratio_lambda*air_speed_turbine_in/diameter_turbine;  %rad/s
rpm_desired_turbine = angular_velocity_desired/(2*pi) *60

%%%%%%Reynolds 
rho = 1.225 %kg/m3
chord_length = 0.01971


