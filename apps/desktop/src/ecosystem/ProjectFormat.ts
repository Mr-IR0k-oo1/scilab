import type { FOSSEEProject, FOSSEEToolId, WorkspaceFile } from './types';

export function createProject(name: string, tools: FOSSEEToolId[], projectPath?: string): FOSSEEProject {
  const now = new Date().toISOString();
  return {
    version: '1.0',
    name,
    path: projectPath ?? `/${name}`,
    tools,
    created: now,
    modified: now,
  };
}

export function buildWorkspaceTree(project: FOSSEEProject): WorkspaceFile[] {
  const nodes: WorkspaceFile[] = [
    { name: project.name, type: 'folder', path: `/${project.name}`, children: [] },
  ];
  const root = nodes[0];
  if (!root.children) return nodes;

  root.children.push({ name: 'project.fossee', type: 'file', path: `/${project.name}/project.fossee` });

  const toolDirMap: Record<string, string> = {
    scilab: 'Scilab',
    xcos: 'Xcos',
    esim: 'eSim',
    openmodelica: 'OpenModelica',
  };

  for (const t of project.tools) {
    const dirName = toolDirMap[t] ?? t;
    root.children.push({
      name: dirName,
      type: 'folder',
      path: `/${project.name}/${dirName}`,
      children: [
        { name: 'main.sce', type: 'file', path: `/${project.name}/${dirName}/main.sce` },
        { name: 'data', type: 'folder', path: `/${project.name}/${dirName}/data`, children: [] },
        { name: 'reports', type: 'folder', path: `/${project.name}/${dirName}/reports`, children: [] },
      ],
    });
  }

  root.children.push(
    { name: 'datasets', type: 'folder', path: `/${project.name}/datasets`, children: [] },
    { name: 'assets', type: 'folder', path: `/${project.name}/assets`, children: [] },
    { name: 'docs', type: 'folder', path: `/${project.name}/docs`, children: [] },
  );

  return nodes;
}
