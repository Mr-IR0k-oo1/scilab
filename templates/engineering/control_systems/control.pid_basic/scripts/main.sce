// PID Controller Simulation Script for Scilab Engine
// Calculates closed-loop step response for a second order plant

// Default parameter fallbacks if not bound
if ~isdef("kp") then kp = 1.0; end
if ~isdef("ki") then ki = 0.5; end
if ~isdef("kd") then kd = 0.1; end

disp("==================================================");
disp("Starting PID Controller Step Response Simulation");
mprintf("Parameters: Kp = %.2f, Ki = %.2f, Kd = %.2f\n", kp, ki, kd);
disp("==================================================");

// Time vector
t = 0:0.05:10;

// Define s-variable
s = poly(0, "s");

// Plant Transfer Function G(s) = 1 / (s^2 + 2s + 2)
G = 1 / (s^2 + 2*s + 2);

// PID Controller Transfer Function C(s) = Kp + Ki/s + Kd*s
C = kp + ki/s + kd*s;

// Closed-loop Transfer Function T(s) = (C * G) / (1 + C * G)
// Linear system simulation
sys = syslin("c", (C * G) / (1 + C * G));

// Step Response
y = csim("step", t, sys);

disp("Simulation completed successfully.");
mprintf("Final Steady State Response Value: %.4f\n", y($));
mprintf("Peak Value: %.4f\n", max(y));
