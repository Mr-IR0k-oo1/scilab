export type FOSSEEToolId = 'scilab' | 'xcos' | 'esim' | 'openmodelica';

export interface FOSSEETool {
  id: FOSSEEToolId;
  name: string;
  tagline: string;
  description: string;
  icon: string;
  color: string;
  modules: string[];
}

export interface FOSSEEProject {
  version: string;
  name: string;
  path: string;
  tools: FOSSEEToolId[];
  created: string;
  modified: string;
}

export interface WorkspaceFile {
  name: string;
  type: 'file' | 'folder';
  path: string;
  children?: WorkspaceFile[];
}
