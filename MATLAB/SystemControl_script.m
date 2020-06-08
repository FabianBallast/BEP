% Base parameters %
T_sim = 10; %s
k_m_t = 23.8e-3; 
R_turbine = 0.15; %m
max_tank_capacity = 80e-9; %m^3
d_tank = 0.07; %m
R_load = 1e3; %Ohm
J_WT = 5.245e-6; %kgm^2
omega_0 = 100: %rpm


ex = xlsread('C:\Users\thequ\Documents\GitHub\BEP\BEP\MATLAB\MockDataSystem.xlsx');
[rows, columns] = size(ex);

for row = 1 : rows
   if isnan(ex(rows - row + 1, 1))
       ex(rows - row + 1, :) = [];
   end
end

% Place the Excel file values into variables
n = ex(1, :)';
t =  ex(2, :)';
omega_m_x = ex(3, :)';
v_wind_x = ex(4, :)';
I_solar_x = ex(5, :)';
V_grid_x = ex(6, :)';
I_LED_set_x = ex(7, :)';
h_H2_x = ex(8, :)';
V_EL_x = ex(9, :)';
V_FC_x = ex(10, :)';

% % Add an empty time vector for each variable and assign x-values
I_solar.time = [];
I_solar.signals.values = [I_solar_x];
I_solar.signals.dimensions = 1;


omega_m.time = [];
omega_m.signals.values = [omega_m_x];
omega_m.signals.dimensions = 1;

v_wind.time = [];
v_wind.signals.values = [v_wind_x];
v_wind.signals.dimensions = 1;

V_grid.time = [];
V_grid.signals.values = [V_grid_x];
V_grid.signals.dimensions = 1;

I_LED_set.time = [];
I_LED_set.signals.values = [I_LED_set_x];
I_LED_set.signals.dimensions = 1;

h_H2.time = [];
h_H2.signals.values = [h_H2_x];
h_H2.signals.dimensions = 1;

V_EL.time = [];
V_EL.signals.values = [V_EL_x];
V_EL.signals.dimensions = 1;

V_FC.time = [];
V_FC.signals.values = [V_FC_x];
V_FC.signals.dimensions = 1;






