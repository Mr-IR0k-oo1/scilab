from typing import List, Dict, Any

EXAMPLES: List[Dict[str, Any]] = [
    {
        "id": "ex-1",
        "title": "Control Systems: Step Response",
        "category": "Control Systems",
        "description": "Analyze second-order system step response using Scilab syslin and csim functions.",
        "difficulty": "Intermediate",
        "code": "s = %s;\nG = 1 / (s^2 + 2*0.5*s + 1);\nt = 0:0.1:10;\ny = csim('step', t, G);\nplot(t, y);\nxgrid();\nxtitle('Second-Order Step Response', 'Time (s)', 'Amplitude');"
    },
    {
        "id": "ex-2",
        "title": "Signal Processing: FFT Analysis",
        "category": "Signal Processing",
        "description": "Compute Fast Fourier Transform of a multi-tone signal with random noise.",
        "difficulty": "Beginner",
        "code": "fs = 1000;\nt = 0:1/fs:1-1/fs;\nx = sin(2*%pi*50*t) + 0.5*sin(2*%pi*120*t);\ny = fft(x);\nf = fs*(0:(length(x)/2))/length(x);\nplot(f, abs(y(1:length(f))));\nxtitle('Spectrum Analysis', 'Frequency (Hz)', 'Magnitude');"
    },
    {
        "id": "ex-3",
        "title": "Matrix Operations & Linear Algebra",
        "category": "Mathematics",
        "description": "Eigenvalue decomposition, matrix inversion, and solving linear systems A*x = b.",
        "difficulty": "Beginner",
        "code": "A = [4, 1, -1; 2, 7, 1; 1, -3, 12];\nb = [3; 19; 31];\nx = A\\b;\ndisp('Solution x =');\ndisp(x);\n[V, D] = spec(A);\ndisp('Eigenvalues =');\ndisp(diag(D));"
    }
]

TUTORIALS: List[Dict[str, Any]] = [
    {
        "id": "tut-1",
        "title": "Getting Started with Scilab Syntax",
        "sections": [
            {"title": "Variables and Matrices", "content": "In Scilab, everything is a matrix. Variables do not require explicit declaration. Assign values directly: A = [1 2; 3 4];"},
            {"title": "Plotting Basics", "content": "Use plot(x, y) to generate 2D plots. Add xgrid() for grid lines and xtitle(title, xlabel, ylabel) for labels."}
        ]
    },
    {
        "id": "tut-2",
        "title": "Building Scilab GUI Applications",
        "sections": [
            {"title": "The uicontrol function", "content": "uicontrol creates interactive GUI components inside a figure window, such as pushbuttons, edit boxes, and sliders."},
            {"title": "Connecting Callbacks", "content": "Set the 'callback' property to execute a Scilab command or script when the user interacts with the control."}
        ]
    }
]

REFERENCE: List[Dict[str, Any]] = [
    {"name": "plot", "syntax": "plot(x, y, [style])", "description": "2D line plot", "category": "Graphics"},
    {"name": "csim", "syntax": "y = csim(u, t, sl)", "description": "Simulation of linear system response", "category": "Control"},
    {"name": "fft", "syntax": "y = fft(x)", "description": "Fast Fourier Transform", "category": "Signal"},
    {"name": "syslin", "syntax": "sl = syslin(domain, num, den)", "description": "Linear system definition", "category": "Control"},
    {"name": "spec", "syntax": "[V, D] = spec(A)", "description": "Eigenvalues and eigenvectors", "category": "Math"}
]
