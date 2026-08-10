// Series RC Circuit Transient Response in Scilab
if ~isdef("r_ohm") then r_ohm = 1000.0; end
if ~isdef("c_farad") then c_farad = 0.000001; end
if ~isdef("v_in") then v_in = 5.0; end

tau = r_ohm * c_farad; // Time constant tau = R * C
t = linspace(0, 5*tau, 200);
vc = v_in * (1 - exp(-t / tau));

mprintf("RC Circuit Parameter Analysis:\n");
mprintf("Resistance: %.1f Ohms, Capacitance: %.2e F\n", r_ohm, c_farad);
mprintf("Time Constant Tau (63.2%% charge time): %.4e s\n", tau);
mprintf("Voltage at 1 Tau: %.4f V\n", v_in * (1 - exp(-1)));
