import { useState } from 'react';

interface ReferenceViewProps {
  categories: { name: string; functions: string[] }[];
}

const DOCS: Record<string, { syntax: string; desc: string; example: string }> = {
  disp: { syntax: 'disp(x)', desc: 'Displays the value of a variable or expression in the console.', example: 'disp("Hello, Scilab!")\ndisp(3.14159)' },
  who: { syntax: 'who()', desc: 'Lists all current variables in the workspace.', example: 'who()' },
  clear: { syntax: 'clear [var1 var2 ...]', desc: 'Removes variables from the workspace. With no arguments, removes all variables.', example: 'clear x y' },
  size: { syntax: 'size(x, [dim])', desc: 'Returns the dimensions of a matrix or array. Optional dim parameter returns size along that dimension.', example: 'A = rand(3,4)\nsize(A)        // returns 3.  4.\nsize(A, 1)     // returns 3' },
  type: { syntax: 'type(x)', desc: 'Returns the type of a Scilab object as an integer code.', example: 'x = 42\ntype(x)       // returns 1 (double)' },
  exists: { syntax: 'exists(name)', desc: 'Checks whether a variable exists in the current workspace.', example: 'x = 10\nexists("x")   // returns 1\nexists("y")   // returns 0' },
  zeros: { syntax: 'zeros(m, n)', desc: 'Creates a matrix of zeros with m rows and n columns. With one argument, creates a square matrix.', example: 'A = zeros(3, 3)\nB = zeros(2, 4)' },
  ones: { syntax: 'ones(m, n)', desc: 'Creates a matrix of ones with m rows and n columns.', example: 'A = ones(3, 2)\nB = ones(1, 5)' },
  rand: { syntax: 'rand(m, n)', desc: 'Creates a matrix of uniformly distributed random numbers between 0 and 1.', example: 'A = rand(3, 3)\nB = rand(1, 10)' },
  eye: { syntax: 'eye(m, n)', desc: 'Creates an identity matrix. With two arguments, creates a rectangular matrix with ones on the diagonal.', example: 'I = eye(4, 4)\nJ = eye(3, 5)' },
  diag: { syntax: 'diag(v [, k])', desc: 'Creates a diagonal matrix from a vector, or extracts the diagonal from a matrix.', example: 'v = [1, 2, 3]\nD = diag(v)\ndiag(D)       // extracts diagonal' },
  triu: { syntax: 'triu(A [, k])', desc: 'Extracts the upper triangular part of a matrix. Optional k parameter specifies the diagonal.', example: 'A = ones(4, 4)\nU = triu(A)' },
  tril: { syntax: 'tril(A [, k])', desc: 'Extracts the lower triangular part of a matrix.', example: 'A = ones(4, 4)\nL = tril(A)' },
  plot: { syntax: 'plot(x, y [, style])', desc: 'Creates a 2D line plot. x and y are vectors of equal length. Optional style string controls color and line style.', example: 'x = linspace(0, 2*%pi, 100)\ny = sin(x)\nplot(x, y)\ntitle("Sine Wave")\nxlabel("x")\nylabel("sin(x)")' },
  scatter: { syntax: 'scatter(x, y [, size, color])', desc: 'Creates a 2D scatter plot. Optional size and color vectors control point appearance.', example: 'x = rand(1, 50)\ny = rand(1, 50)\nscatter(x, y)' },
  bar: { syntax: 'bar(x, y [, width])', desc: 'Creates a bar chart. x contains category positions, y contains bar heights.', example: 'x = [1, 2, 3, 4, 5]\ny = [10, 7, 15, 3, 12]\nbar(x, y)' },
  histplot: { syntax: 'histplot(n, data)', desc: 'Plots a histogram with n bins from the data vector.', example: 'data = rand(1, 1000)\nhistplot(20, data)' },
  title: { syntax: 'title(text)', desc: 'Adds a title to the current plot.', example: 'plot(x, y)\ntitle("My Plot")' },
  xlabel: { syntax: 'xlabel(text)', desc: 'Labels the x-axis of the current plot.', example: 'xlabel("Time (s)")' },
  ylabel: { syntax: 'ylabel(text)', desc: 'Labels the y-axis of the current plot.', example: 'ylabel("Amplitude")' },
  legend: { syntax: 'legend(label1, label2, ...)', desc: 'Adds a legend to the current plot with the specified labels.', example: 'plot(x, sin(x))\nplot(x, cos(x))\nlegend("sin", "cos")' },
  csvRead: { syntax: 'csvRead(filename)', desc: 'Reads a comma-separated values file into a Scilab matrix.', example: 'data = csvRead("measurements.csv")' },
  csvWrite: { syntax: 'csvWrite(data, filename)', desc: 'Writes a Scilab matrix to a comma-separated values file.', example: 'A = rand(5, 3)\ncsvWrite(A, "output.csv")' },
  fft: { syntax: 'fft(x)', desc: 'Computes the Fast Fourier Transform (FFT) of a vector or matrix.', example: 'fs = 1000\nN = 1024\nx = sin(2*%pi*50*(0:N-1)/fs)\nX = fft(x)\nf = (0:N-1)*(fs/N)\nplot(f, abs(X))' },
  ifft: { syntax: 'ifft(X)', desc: 'Computes the inverse Fast Fourier Transform.', example: 'X = fft(x)\ny = ifft(X)' },
  filter: { syntax: 'filter(b, a, x)', desc: 'Applies a digital filter defined by numerator b and denominator a to signal x.', example: 'b = [1, -0.5]\na = [1, 0.2]\ny = filter(b, a, x)' },
  mean: { syntax: 'mean(x [, dim])', desc: 'Computes the arithmetic mean of array elements.', example: 'data = rand(1, 100)\nm = mean(data)' },
  median: { syntax: 'median(x [, dim])', desc: 'Computes the median value of array elements.', example: 'data = rand(1, 100)\nm = median(data)' },
  stdev: { syntax: 'stdev(x)', desc: 'Computes the standard deviation of array elements.', example: 'data = rand(1, 100)\ns = stdev(data)' },
  corr: { syntax: 'corr(x, y)', desc: 'Computes the correlation coefficient between two vectors.', example: 'x = rand(1, 50)\ny = x + rand(1, 50)*0.1\nr = corr(x, y)' },
  reglin: { syntax: 'reglin(x, y)', desc: 'Computes linear regression coefficients a and b for y = a*x + b.', example: 'x = [1, 2, 3, 4, 5]\ny = [2, 4, 6, 8, 10]\n[a, b] = reglin(x, y)' },
  ode: { syntax: 'ode(y0, t0, t, f)', desc: 'Solves ordinary differential equations using the default solver. y0 is initial condition, t is time vector, f is derivative function.', example: 'function dy = f(t, y)\n    dy = -y\nendfunction\ny0 = 1\nt = linspace(0, 5, 50)\ny = ode(y0, 0, t, f)\nplot(t, y)' },
  interp: { syntax: 'interp(x, y, xq)', desc: 'Performs linear interpolation of data points (x, y) at query points xq.', example: 'x = [0, 1, 2, 3]\ny = [0, 1, 4, 9]\nxq = [0.5, 1.5]\nyq = interp(x, y, xq)' },
  spline: { syntax: 'spline(x, y)', desc: 'Computes cubic spline coefficients for interpolation of data points.', example: 'x = [0, 1, 2, 3, 4]\ny = [0, 1, 0, 1, 0]\ns = spline(x, y)' },
  fsolve: { syntax: 'fsolve(x0, f)', desc: 'Finds the root of a function near the initial guess x0.', example: 'function y = f(x)\n    y = x^2 - 2\nendfunction\nroot = fsolve(1, f)  // returns sqrt(2)' },
  intg: { syntax: 'intg(a, b, f)', desc: 'Computes the definite integral of a function from a to b.', example: 'function y = f(x)\n    y = x^2\nendfunction\nI = intg(0, 1, f)  // integral of x^2 from 0 to 1' },
  bode: { syntax: 'bode(sys)', desc: 'Plots the Bode frequency response (magnitude and phase) of a linear system.', example: 's = poly(0, "s")\nH = syslin("c", 1/(s+1))\nbode(H)' },
  nyquist: { syntax: 'nyquist(sys)', desc: 'Plots the Nyquist diagram of a linear system.', example: 's = poly(0, "s")\nH = syslin("c", 1/(s^2+s+1))\nnyquist(H)' },
  step: { syntax: 'step(sys)', desc: 'Plots the step response of a linear system.', example: 's = poly(0, "s")\nH = syslin("c", 1/(s^2+0.5*s+1))\nstep(H)' },
  tf: { syntax: 'tf(num, den)', desc: 'Creates a transfer function model from numerator and denominator coefficients.', example: 's = poly(0, "s")\nH = tf(1, s^2 + s + 1)' },
  ss: { syntax: 'ss(A, B, C, D)', desc: 'Creates a state-space model from system matrices.', example: 'A = [0, 1; -1, -1]\nB = [0; 1]\nC = [1, 0]\nD = 0\nsys = ss(A, B, C, D)' },
};

export default function ReferenceView({ categories }: ReferenceViewProps) {
  const [search, setSearch] = useState('');
  const [selectedFn, setSelectedFn] = useState<string | null>(null);

  const allFns = categories.flatMap((c) => c.functions.map((f) => ({ name: f, category: c.name })));
  const filtered = search
    ? allFns.filter((f) => f.name.toLowerCase().includes(search.toLowerCase()))
    : allFns;

  const doc = selectedFn ? DOCS[selectedFn] : null;

  return (
    <div className="reference-view">
      <div className="reference-search">
        <input className="lc-search-input" placeholder="Search functions..." value={search} onChange={(e) => setSearch(e.target.value)} />
      </div>
      <div className="reference-body">
        <div className="reference-list">
          {!search && categories.map((cat) => (
            <div key={cat.name} className="ref-category">
              <h4 className="ref-cat-title">{cat.name}</h4>
              {cat.functions.map((fn) => (
                <div key={fn} className={`ref-fn-item ${selectedFn === fn ? 'active' : ''}`} onClick={() => setSelectedFn(fn)}>
                  {fn}
                </div>
              ))}
            </div>
          ))}
          {search && filtered.map((fn) => (
            <div key={fn.name} className={`ref-fn-item ${selectedFn === fn.name ? 'active' : ''}`} onClick={() => setSelectedFn(fn.name)}>
              {fn.name}
              <span className="ref-fn-cat">{fn.category}</span>
            </div>
          ))}
        </div>
        <div className="reference-detail">
          {doc ? (
            <div className="ref-detail-content">
              <h2>{selectedFn}</h2>
              <div className="ref-detail-section">
                <h4>Syntax</h4>
                <pre className="ref-syntax">{doc.syntax}</pre>
              </div>
              <div className="ref-detail-section">
                <h4>Description</h4>
                <p>{doc.desc}</p>
              </div>
              <div className="ref-detail-section">
                <h4>Example</h4>
                <pre className="ref-syntax" style={{ color: 'var(--green)' }}>{doc.example}</pre>
              </div>
            </div>
          ) : (
            <div className="ref-detail-empty">Select a function to view documentation</div>
          )}
        </div>
      </div>
    </div>
  );
}
