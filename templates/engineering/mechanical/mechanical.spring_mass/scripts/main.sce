// Mass-Spring-Damper ODE Solver in Scilab
if ~isdef("mass_kg") then mass_kg = 2.0; end
if ~isdef("k_spring") then k_spring = 100.0; end
if ~isdef("c_damping") then c_damping = 2.0; end

wn = sqrt(k_spring / mass_kg); // Natural frequency rad/s
zeta = c_damping / (2 * sqrt(mass_kg * k_spring)); // Damping ratio

disp("Mechanical Vibration Parameters:");
mprintf("Natural Frequency wn: %.2f rad/s (%.2f Hz)\n", wn, wn / (2*%pi));
mprintf("Damping Ratio Zeta: %.4f\n", zeta);

if zeta < 1 then
    disp("System Condition: Underdamped Oscillatory Response");
elseif zeta == 1 then
    disp("System Condition: Critically Damped");
else
    disp("System Condition: Overdamped Non-oscillatory");
end
