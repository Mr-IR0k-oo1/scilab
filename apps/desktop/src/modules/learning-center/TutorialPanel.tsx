import { useState } from 'react';

const TUTORIALS = [
  {
    title: 'Create Your First Chart',
    steps: [
      { id: 's1', title: 'Create a New Project', instruction: 'Click File → New Project. Name it "My First Chart".', hint: 'Press Ctrl+N or go to File > New Project.' },
      { id: 's2', title: 'Import Data', instruction: 'Go to Data Studio → Import Data. Select a CSV file.', hint: 'Use csvRead("file.csv") in the editor to load data.' },
      { id: 's3', title: 'Create Chart', instruction: 'Open Visualization Studio and select "Line" chart type.', hint: 'Use plot(x, y) directly in the Script Editor.' },
      { id: 's4', title: 'Customize', instruction: 'Change the chart title and axis labels in the config panel.', hint: 'Add title(), xlabel(), and ylabel() to your script.' },
      { id: 's5', title: 'Export', instruction: 'Click Export PNG to save your chart as an image.', hint: 'Use xs2png(0, "chart.png") in Scilab.' },
    ],
  },
  {
    title: 'Data Analysis Pipeline',
    steps: [
      { id: 'd1', title: 'Import Dataset', instruction: 'Load a CSV file using the Data Studio import dialog.', hint: 'csvRead loads data, size() checks dimensions.' },
      { id: 'd2', title: 'Clean Data', instruction: 'Add transform steps: filter rows, drop nulls, rename columns.', hint: 'Use find() to locate null values: find(isnan(data)).' },
      { id: 'd3', title: 'Compute Statistics', instruction: 'Switch to the Stats tab to view column statistics.', hint: 'mean(), median(), stdev(), and corr() are useful.' },
      { id: 'd4', title: 'Visualize Results', instruction: 'Create a bar chart or histogram of the results.', hint: 'bar() for categories, histplot() for distributions.' },
      { id: 'd5', title: 'Generate Report', instruction: 'Go to Report Generator and add your chart.', hint: 'Use csvWrite() to export processed data first.' },
    ],
  },
  {
    title: 'Signal Processing Basics',
    steps: [
      { id: 'p1', title: 'Generate Signal', instruction: 'Create a sine wave: t = linspace(0, 1, 1000); x = sin(2*%pi*50*t);', hint: 'linspace creates evenly spaced points.' },
      { id: 'p2', title: 'Add Noise', instruction: 'Add random noise: y = x + 0.1*rand(1,1000);', hint: 'rand() generates uniform random numbers.' },
      { id: 'p3', title: 'Compute FFT', instruction: 'Use fft() to compute the frequency spectrum.', hint: 'fft() computes the Fast Fourier Transform.' },
      { id: 'p4', title: 'Plot Spectrum', instruction: 'Plot magnitude vs. frequency: plot(f, abs(X)).', hint: 'abs() gives magnitude, f is the frequency axis.' },
      { id: 'p5', title: 'Filter Signal', instruction: 'Apply a low-pass filter using filter().', hint: 'Design filter coefficients b, a and use y = filter(b, a, x).' },
    ],
  },
];

export default function TutorialPanel() {
  const [tutorialIdx, setTutorialIdx] = useState(0);
  const [currentStep, setCurrentStep] = useState(0);
  const [completed, setCompleted] = useState<Set<string>>(new Set());
  const [showHint, setShowHint] = useState(false);

  const tutorial = TUTORIALS[tutorialIdx];
  const step = tutorial.steps[currentStep];

  const markDone = () => {
    setCompleted((prev) => new Set(prev).add(step.id));
    setShowHint(false);
    if (currentStep < tutorial.steps.length - 1) setCurrentStep((s) => s + 1);
  };

  const switchTutorial = (idx: number) => {
    setTutorialIdx(idx);
    setCurrentStep(0);
    setCompleted(new Set());
    setShowHint(false);
  };

  return (
    <div className="tutorial-panel">
      <div className="tutorial-sidebar">
        <div style={{ display: 'flex', gap: 4, marginBottom: 12 }}>
          {TUTORIALS.map((t, i) => (
            <button
              key={i}
              className={`lc-cat-btn ${i === tutorialIdx ? 'active' : ''}`}
              onClick={() => switchTutorial(i)}
              style={{ fontSize: 10 }}
            >
              {t.title}
            </button>
          ))}
        </div>
        <h3>{tutorial.title}</h3>
        <div className="tutorial-progress">
          <div className="tutorial-progress-bar" style={{ width: `${((currentStep + 1) / tutorial.steps.length) * 100}%` }} />
        </div>
        <div className="tutorial-step-list">
          {tutorial.steps.map((s, i) => (
            <div
              key={s.id}
              className={`tutorial-step-item ${i === currentStep ? 'active' : ''} ${completed.has(s.id) ? 'done' : ''}`}
              onClick={() => setCurrentStep(i)}
            >
              <span className="tutorial-step-num">{completed.has(s.id) ? '#' : i + 1}</span>
              <span>{s.title}</span>
            </div>
          ))}
        </div>
      </div>
      <div className="tutorial-content">
        <h2>{step.title}</h2>
        <p className="tutorial-instruction">{step.instruction}</p>
        {showHint && (
          <div style={{ padding: '8px 16px', background: 'var(--accent-dim)', borderRadius: 'var(--radius)', color: 'var(--accent)', fontSize: 12, marginBottom: 16, maxWidth: 500 }}>
            {step.hint}
          </div>
        )}
        <div className="tutorial-actions">
          <button className="ecosystem-btn primary" onClick={markDone}>
            {currentStep < tutorial.steps.length - 1 ? 'Next Step' : 'Complete'}
          </button>
          <button className="ecosystem-btn" onClick={() => setShowHint(!showHint)}>
            {showHint ? 'Hide Hint' : 'Hint'}
          </button>
        </div>
        <div className="tutorial-step-indicator">
          Step {currentStep + 1} of {tutorial.steps.length} | {completed.size} completed
        </div>
      </div>
    </div>
  );
}
