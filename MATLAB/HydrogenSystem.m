fprintf('\n')


%pv = nRT

%hydrogen has 142 MJ/kg energy density


%electrolyzer produces H2: 10 mL/min @ 1 A
%                      O2:  5 mL/min @ 1 A

%%%%%%%%%%%%%%%
v_H2 = 10  *1e-6; %m3/min
voltage = 2; %V
current = 1; %A
%%%%%%%%%%%%%%%

p = 1e5; %approx 1 bar
R = 8.31446261815324; %J / (K*mol)
T = 298; %K

%molair masses
mm_H2O = 18.01528 *1e-3;%kg /mol
mm_H2  = 2.016    *1e-3;%kg /mol
mm_O2  = 32.0     *1e-3;%kg /mol

rho_H2O = 998; %kg/m3 --> 0.998 g/cm3 == g/mL
  
n_H2 = p*v_H2/(R*T);  %mol H2 produces per min


%2 H2O --> 2 H2 + 1 O2
n_O2 = n_H2/2;
n_H2O = n_H2;


m_H2O = n_H2O*mm_H2O;       %kg / min H2O used
v_H2O = m_H2O/rho_H2O;      %m3/min H2O used

fprintf('H2O usage electrolyzer @(%.0f mL/min H2 production):   %.2f mL/h \n',v_H2*1e6, v_H2O*1e6*60)

%%%%%% energy characteristics
P_in = voltage*current;
m_H2 = n_H2*mm_H2;  %kg /min

energy_density_H2 = 142e6; %J/kg
energy_H2_production = m_H2*energy_density_H2;   %J/min
power_H2_production = energy_H2_production/60;  %W

efficiency = power_H2_production/ (P_in);


%%%%%%%%%%%%%%%%%% tank parameters

D_tank = 0.0335; %m;   confirmed with geodriehoek + terugrekenen vanaf volumaire streepjes
h0 = 0.125; %m;      reading van proximity sensor bij 0 gas in de tank

syms reading %is proximity sensor reading in m

v_H2_in_tank = (h0-reading)*(pi*(D_tank/2)^2);
v_O2_in_tank = v_H2_in_tank/2;


%%% interesting
v_H2O_per_v_H2 = v_H2O/v_H2;
H2_in_tank = 80*1e-6; %m3

fprintf('H2O production when using all hydrogen in tank:   %.2f mL \n',v_H2O_per_v_H2*H2_in_tank*1e6)



