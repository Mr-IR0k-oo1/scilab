// Linear Regression & Statistical Analysis in Scilab
if ~isdef("n_samples") then n_samples = 100; end

x = linspace(0, 10, n_samples)';
y = 2.5 * x + 1.2 + rand(x, "normal");

// Solve Least Squares: y = a*x + b
A = [x, ones(x)];
coef = A \ y;
slope = coef(1);
intercept = coef(2);

disp("Linear Regression Solver Result:");
mprintf("Fitted Equation: y = %.4f * x + %.4f\n", slope, intercept);
