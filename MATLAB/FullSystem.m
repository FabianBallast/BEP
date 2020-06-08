%% General model parameters %%
T_sim = 2; %s
R_load = 1e3; %Ohm
R_LED_max = 75/4; %Ohm
P_max_SP = 0.5; %W
P_max_LED = 12*0.16*4; %W
rho_air = 1.225; %kg/m^3
pwm_timer = 1/50;
t_sample = pwm_timer/10;

% Turbine parameters %
k_m_t = 23.8e-3; 
R_turbine = 0.15; %m
J_wind = 5.245e-6; %kgm^2
omega_0 = 100; %rpm
lambda_opt = 2.1; %lambda = R*omega/V_w
P_max_WT = 0.2; %W
a_friction = 0;
b_friction = 0;
K_v = 0;

% Hydrogen parameters %
max_tank_capacity = 80e-9; %m^3
d_tank = 0.07; %m
P_max_EL = 3; %W
P_max_FC = 1; %W

%% Excel variables %%
ex1 = xlsread('..\MATLAB\FullSystemData.xlsx','Sheet1');
ex2 = xlsread('..\MATLAB\FullSystemData.xlsx','Sheet2');
ex3 = xlsread('..\MATLAB\FullSystemData.xlsx','Sheet3');

% Places the Excel file values into variables
n = 50;
t =  ex1(2, :)';
r_WT_x = ex1(3, :)';
r_SP_x = ex1(4, :)';
r_LED_x = ex1(5, :)';
lambda_data_x  = ex1(6, :)';
r_wind_data_x = ex1(7, :)';
V_w_data_x = ex1(8,:)';
r_PS_x = ex1(9,:)';
C_T_matrix = ex2(2:12,2:21)';
r_solar_data_x = ex3(1,:)';
I_SP_data_x = ex3(2,:)';

% Add an empty time vector for each variable and assign x-values
[rows, columns] = size(lambda_data_x);

for row = 1 : rows
   if isnan(lambda_data_x(rows - row + 1, 1))
       lambda_data_x(rows - row + 1, :) = [];
   end
end


step_size = T_sim/n;%s

r_WT.time = [];
r_WT.signals.values = [r_WT_x];
r_WT.signals.dimensions = 1;

r_SP.time = [];
r_SP.signals.values = [r_SP_x];
r_SP.signals.dimensions = 1;

r_LED.time = [];
r_LED.signals.values = [r_LED_x];
r_LED.signals.dimensions = 1;

lambda_data.time = [];
lambda_data.signals.values = [lambda_data_x];
lambda_data.signals.dimensions = 1;

r_wind_data.time = [];
r_wind_data.signals.values = [r_wind_data_x];
r_wind_data.signals.dimensions = 1;

V_w_data.time = [];
V_w_data.signals.values = [V_w_data_x];
V_w_data.signals.dimensions = 1;

r_solar_data.time = [];
r_solar_data.signals.values = [r_solar_data_x];
r_solar_data.signals.dimensions = 1;

I_SP_data.time = [];
I_SP_data.signals.values = [I_SP_data_x];
I_SP_data.signals.dimensions = 1;


r_PS.time = [];
r_PS.signals.values = [r_PS_x];
r_PS.signals.dimensions = 1;