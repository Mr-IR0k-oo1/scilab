// 1D Transient Heat Conduction Model in Scilab
if ~isdef("k_thermal") then k_thermal = 205.0; end // Aluminum k = 205 W/mK
if ~isdef("t_source") then t_source = 100.0; end

length_m = 0.5;
nodes = 50;
dx = length_m / (nodes - 1);
x = linspace(0, length_m, nodes);

// Temperature vector initialized to ambient 25 deg C
T = 25.0 * ones(x);
T(1) = t_source; // Boundary condition at x = 0

mprintf("Heat Conduction Analysis:\n");
mprintf("Thermal Conductivity k: %.1f W/(m K)\n", k_thermal);
mprintf("Boundary Source Temp: %.1f deg C, Rod Length: %.2f m\n", t_source, length_m);
mprintf("Temperature at Midpoint (x=0.25m): %.2f deg C\n", T(int(nodes/2)));
