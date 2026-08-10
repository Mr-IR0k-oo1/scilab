// Bisection Root Finding Method in Scilab
if ~isdef("tol") then tol = 0.0001; end
if ~isdef("max_iter") then max_iter = 50; end

deff("y=f(x)", "y = x^3 - x - 2");

a = 1.0;
b = 2.0;

disp("Finding root for f(x) = x^3 - x - 2 in [1.0, 2.0]");

iter = 0;
while (b - a)/2 > tol & iter < max_iter
    c = (a + b) / 2;
    if f(c) == 0 then break; end
    if f(a)*f(c) < 0 then
        b = c;
    else
        a = c;
    end
    iter = iter + 1;
end

root_val = (a + b) / 2;
mprintf("Converged Root: %.6f in %d iterations\n", root_val, iter);
