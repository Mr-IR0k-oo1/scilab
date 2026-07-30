import type { FOSSEETool, FOSSEEToolId } from './types';

export const FOSSEE_TOOLS: Record<FOSSEEToolId, FOSSEETool> = {
  scilab: {
    id: 'scilab',
    name: 'Scilab',
    tagline: 'Scientific Computing',
    description: 'Open source scientific computing environment for numerical analysis, signal processing, and control systems.',
    icon: '⊡',
    color: '#ff3333',
    modules: ['editor', 'gui', 'viz', 'data', 'report', 'learn'],
  },
  xcos: {
    id: 'xcos',
    name: 'Xcos',
    tagline: 'Dynamic Systems Modeling',
    description: 'Graphical editor for modeling and simulation of hybrid dynamic systems, similar to Simulink.',
    icon: '◈',
    color: '#ffffff',
    modules: ['viz', 'data', 'report'],
  },
  esim: {
    id: 'esim',
    name: 'eSim',
    tagline: 'Circuit Design & Simulation',
    description: 'Open source EDA tool for circuit design, simulation, and PCB layout. Designed for electronics labs.',
    icon: '◎',
    color: '#aaaaaa',
    modules: ['viz', 'report'],
  },
  openmodelica: {
    id: 'openmodelica',
    name: 'OpenModelica',
    tagline: 'Modelica-Based Simulation',
    description: 'Open source Modelica environment for modeling, simulating, and optimizing complex physical systems.',
    icon: '▣',
    color: '#ff5555',
    modules: ['editor', 'viz', 'data', 'report'],
  },
};

export function getTool(id: FOSSEEToolId): FOSSEETool {
  return FOSSEE_TOOLS[id];
}

export function getTools(ids: FOSSEEToolId[]): FOSSEETool[] {
  return ids.map((id) => FOSSEE_TOOLS[id]).filter(Boolean);
}
