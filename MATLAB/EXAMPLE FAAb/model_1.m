%Some variables to set up the system. 
T_sim = 24;             %s
T_dag = 24;             %s
t_step = T_dag / 100000;  %s

P_solar = 10;           %W
P_wind = 0;             %W
P_houses = 2;           %W
P_generator = 7;        %W
P_gen_inertia = 3;    %W/s


P_elektrolyzer = 4.6;   %W
P_fuelcell = 1.2;       %W

V_stor = 100;           %cm^3 = ml
q_per_Watt = 2;         %cm^3 / min


% Trying an advanced input signal for solar
t = linspace(0, T_sim, T_sim / t_step + 1)';
omega = 4 * pi / T_dag;
A = 2;
solar_x_raw = A * cos(omega * t) + A;
solar_x = solar_x_raw .* (t >= T_dag / 4 & t <= T_dag * 3 / 4);
solar.time = [];
solar.signals.values = [solar_x];
solar.signals.dimensions = 1;

% Trying an advanced input signal for wind
t = linspace(0, T_sim, T_sim / t_step + 1)';
omega = 2 * pi / T_dag;
A = 0.5;
Offset = 1.5;
wind_x = A * cos(omega * t) + Offset + A;
wind.time = [];
wind.signals.values = [wind_x];
wind.signals.dimensions =1;

% Trying an advanced energy demand for households
t = linspace(0, T_sim, T_sim / t_step + 1)';
omega = 2 * pi / T_dag;
A = 1;
Offset = 2.5;
house_x1_raw = A * cos(3 * omega * t) - A;
house_x1 = house_x1_raw .* (t <= 1/3 * T_dag);
house_x2_raw = -1.5 * A * cos(3 * omega * t) + 1.5 * A;
house_x2 = house_x2_raw .* (t >= 2/3 * T_dag);
house.time = [];
house.signals.values = [house_x1 + house_x2 + Offset];
house.signals.dimensions =1;

f = 0:100001:0.1;

%plot(t, solar_x, 'k')
%hold on 
%plot(t, wind_x, 'g')
%hold on
plot(t, f, 'k')
xlabel('Time (Hours)')
ylabel('Power (Watt)')
xticks([0 4 8 12 16 20 24])
axis([0 24 0 6])
%legend('Solar Power', 'Wind Power', 'Power Demand')





