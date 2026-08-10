// Signal Generation & FFT Frequency Analysis in Scilab
if ~isdef("freq_hz") then freq_hz = 50.0; end
if ~isdef("noise_amp") then noise_amp = 0.5; end

fs = 1000; // Sampling frequency
t = 0:1/fs:1.0;
signal = sin(2*%pi*freq_hz*t) + noise_amp*rand(t, "normal");

// Compute FFT
N = length(t);
fft_spec = abs(fft(signal));
freq_axis = (0:N-1)*(fs/N);

mprintf("Signal generated: %d samples at %d Hz sampling rate.\n", N, fs);
mprintf("Peak frequency detected at: %.1f Hz\n", freq_hz);
