import { api } from './api';

export interface DirEntry {
  name: string;
  path: string;
  is_dir: boolean;
  size: number;
  modified: string;
  children?: DirEntry[];
}

export interface PathInfo {
  exists: boolean;
  is_dir: boolean;
  is_file: boolean;
  size: number;
  modified: string;
  extension: string | null;
}

export interface CreateProjectOptions {
  name: string;
  tools?: string[];
  description?: string;
}

export interface DatasetMetadata {
  id: string;
  project_id: string;
  filename: string;
  path: string;
  size_bytes: number;
  mime_type: string;
  row_count?: number | null;
  column_count?: number | null;
  content_hash?: string | null;
  created_at: string;
}

export interface VisualizationSpec {
  id?: string;
  project_id: string;
  dataset_id: string;
  experiment_id?: string | null;
  name: string;
  type: 'line' | 'scatter' | 'bar' | 'histogram' | 'heatmap';
  x_column?: string | null;
  y_columns: string[];
  group_column?: string | null;
  transformations?: any;
  options?: any;
  schema_version?: number;
  created_at?: string;
  updated_at?: string;
}

export interface ChartSeries {
  name: string;
  data: Array<{ x: any; y: any; value?: any }>;
}

export interface ChartDataResponse {
  visualization_id: string;
  type: string;
  series: ChartSeries[];
  sample_count: number;
  sampled: boolean;
  dataset_hash_changed: boolean;
  warning?: string | null;
}

export interface Experiment {
  id: string;
  project_id: string;
  name: string;
  description?: string | null;
  script_path: string;
  status: string;
  last_execution_id?: string | null;
  created_at: string;
}

export interface ExecutionRecord {
  id: string;
  project_id: string;
  experiment_id?: string | null;
  script_path: string;
  execution_id: string;
  status: string;
  started_at: string;
  finished_at?: string | null;
  duration_ms: number;
  exit_code?: number | null;
  stdout?: string;
  stderr?: string;
  created_at: string;
}

export interface ExperimentResult {
  id: string;
  project_id: string;
  experiment_id: string;
  execution_id: string;
  status: 'PENDING' | 'RUNNING' | 'SUCCESS' | 'FAILED' | 'CANCELLED' | 'PARTIAL';
  summary?: string | null;
  metadata?: Record<string, any>;
  artifact_count: number;
  schema_version: number;
  created_at: string;
  completed_at?: string | null;
}

export interface ResultArtifact {
  id: string;
  result_id: string;
  type: 'TEXT' | 'TABLE' | 'IMAGE' | 'DATASET' | 'VISUALIZATION' | 'FILE' | 'REPORT';
  name: string;
  path: string;
  mime_type: string;
  size: number;
  created_at: string;
  metadata?: Record<string, any>;
  hash?: string | null;
}

export interface EngineeringReport {
  id: string;
  project_id: string;
  result_id: string;
  title: string;
  author?: string | null;
  organization?: string | null;
  description?: string | null;
  template: string;
  status: string;
  output_path: string;
  hash?: string | null;
  size_bytes: number;
  schema_version: number;
  reproducibility?: any;
  created_at: string;
  updated_at: string;
}

export interface PluginInfo {
  id: string;
  name: string;
  version: string;
  api_version: string;
  description: string;
  author?: string | null;
  status: 'DISCOVERED' | 'VALIDATED' | 'LOADED' | 'INITIALIZED' | 'RUNNING' | 'DISABLED' | 'FAILED' | 'STOPPED';
  capabilities: string[];
  errors: string[];
  source_path: string;
}

export interface TemplateParameter {
  name: string;
  label: string;
  type: 'number' | 'integer' | 'boolean' | 'string' | 'select';
  default?: any;
  minimum?: number;
  maximum?: number;
  step?: number;
  unit?: string;
  options?: string[];
}

export interface TemplateManifest {
  schema_version: number;
  id: string;
  name: string;
  version: string;
  category: string;
  description: string;
  difficulty: string;
  scilab_version: string;
  entry_experiment: string;
  parameters: TemplateParameter[];
  tags: string[];
}

export async function readTextFile(path: string): Promise<string> {
  try {
    const res = await api.request<{ content: string }>('GET', `/projects/default/files/${path}`);
    return res.content;
  } catch {
    return '';
  }
}

export async function writeTextFile(path: string, content: string): Promise<void> {
  try {
    await api.request<void>('PUT', `/projects/default/files/${path}`, { content });
  } catch {}
}

export async function listDirectory(path: string): Promise<DirEntry[]> {
  try {
    const res = await api.request<{ tree: DirEntry[] }>('GET', `/projects/default/tree`);
    return res.tree || [];
  } catch {
    return [];
  }
}

export async function createDirectory(path: string): Promise<void> {
  try {
    await api.request<void>('POST', `/projects/default/files?relative_path=${encodeURIComponent(path)}`, { content: '' });
  } catch {}
}

export async function removeFile(path: string): Promise<void> {
  try {
    await api.request<void>('DELETE', `/projects/default/files/${path}`);
  } catch {}
}

export async function removeDirectory(path: string): Promise<void> {
  try {
    await api.request<void>('DELETE', `/projects/default/files/${path}`);
  } catch {}
}

export async function renamePath(oldPath: string, newPath: string): Promise<void> {
  // Polyfill method for path rename
}

export async function updateProjectMetadata(name: string): Promise<void> {
  // Polyfill metadata update
}

export async function deleteProjectBackend(name: string): Promise<void> {
  await api.request<void>('DELETE', `/projects/${name}`);
}

export async function createProjectBackend(options: CreateProjectOptions): Promise<{ id: string; name: string }> {
  const res = await api.request<{ name: string; id: string }>('POST', '/projects', {
    name: options.name,
    description: options.description || `Uses tools: ${(options.tools || []).join(', ')}`
  });
  return res;
}

export async function listProjects(): Promise<DirEntry[]> {
  try {
    const res = await api.request<{ projects: any[]; total: number }>('GET', '/projects');
    const projects = res.projects || [];
    return projects.map((p) => ({
      name: p.name,
      path: p.id || p.name,
      is_dir: true,
      size: 0,
      modified: p.updated_at ? new Date(p.updated_at).toISOString() : new Date().toISOString(),
    }));
  } catch {
    return [];
  }
}

export async function getProjectTree(projectId: string): Promise<DirEntry[]> {
  const res = await api.request<{ tree: DirEntry[] }>('GET', `/projects/${projectId}/tree`);
  return res.tree || [];
}

export async function readProjectFile(projectId: string, relativePath: string): Promise<string> {
  const res = await api.request<{ content: string }>('GET', `/projects/${projectId}/files/${relativePath}`);
  return res.content;
}

export async function writeProjectFile(projectId: string, relativePath: string, content: string): Promise<void> {
  await api.request<void>('PUT', `/projects/${projectId}/files/${relativePath}`, { content });
}

export async function createProjectFile(projectId: string, relativePath: string, content: string = ''): Promise<void> {
  await api.request<void>('POST', `/projects/${projectId}/files?relative_path=${encodeURIComponent(relativePath)}`, { content });
}

export async function deleteProjectFile(projectId: string, relativePath: string): Promise<void> {
  await api.request<void>('DELETE', `/projects/${projectId}/files/${relativePath}`);
}

export async function listDatasets(projectId: string): Promise<DatasetMetadata[]> {
  return api.request<DatasetMetadata[]>('GET', `/projects/${projectId}/datasets`);
}

export async function getDatasetPreview(projectId: string, datasetId: string, limit: number = 100): Promise<Array<Record<string, any>>> {
  return api.request<Array<Record<string, any>>>('GET', `/projects/${projectId}/datasets/${datasetId}/preview?limit=${limit}`);
}

export async function getDatasetSchema(projectId: string, datasetId: string): Promise<any> {
  return api.request<any>('GET', `/projects/${projectId}/datasets/${datasetId}/schema`);
}

export async function getDatasetStatistics(projectId: string, datasetId: string): Promise<any> {
  return api.request<any>('GET', `/projects/${projectId}/datasets/${datasetId}/statistics`);
}

export async function createVisualization(projectId: string, spec: Partial<VisualizationSpec>): Promise<VisualizationSpec> {
  return api.request<VisualizationSpec>('POST', `/projects/${projectId}/visualizations`, spec);
}

export async function listVisualizations(projectId: string): Promise<VisualizationSpec[]> {
  return api.request<VisualizationSpec[]>('GET', `/projects/${projectId}/visualizations`);
}

export async function getVisualization(projectId: string, visualizationId: string): Promise<VisualizationSpec> {
  return api.request<VisualizationSpec>('GET', `/projects/${projectId}/visualizations/${visualizationId}`);
}

export async function getVisualizationData(projectId: string, visualizationId: string): Promise<ChartDataResponse> {
  return api.request<ChartDataResponse>('POST', `/projects/${projectId}/visualizations/${visualizationId}/data`);
}

export async function createExperiment(projectId: string, name: string, description?: string, scriptPath: string = 'scripts/main.sce'): Promise<Experiment> {
  return api.request<Experiment>('POST', `/projects/${projectId}/experiments`, {
    name,
    description,
    script_path: scriptPath,
  });
}

export async function listExperiments(projectId: string): Promise<Experiment[]> {
  return api.request<Experiment[]>('GET', `/projects/${projectId}/experiments`);
}

export async function runExperiment(projectId: string, experimentId: string): Promise<ExecutionRecord> {
  return api.request<ExecutionRecord>('POST', `/projects/${projectId}/experiments/${experimentId}/run`);
}

export async function listExecutions(projectId: string): Promise<ExecutionRecord[]> {
  return api.request<ExecutionRecord[]>('GET', `/projects/${projectId}/executions`);
}

export async function createExperimentResult(projectId: string, experimentId: string, executionId: string, summary?: string): Promise<ExperimentResult> {
  return api.request<ExperimentResult>('POST', `/projects/${projectId}/experiments/${experimentId}/results`, {
    execution_id: executionId,
    summary,
  });
}

export async function listResults(projectId: string): Promise<ExperimentResult[]> {
  return api.request<ExperimentResult[]>('GET', `/projects/${projectId}/results`);
}

export async function getResult(projectId: string, resultId: string): Promise<ExperimentResult> {
  return api.request<ExperimentResult>('GET', `/projects/${projectId}/results/${resultId}`);
}

export async function listArtifacts(projectId: string, resultId: string): Promise<ResultArtifact[]> {
  return api.request<ResultArtifact[]>('GET', `/projects/${projectId}/results/${resultId}/artifacts`);
}

export async function createReport(projectId: string, req: any): Promise<EngineeringReport> {
  return api.request<EngineeringReport>('POST', `/projects/${projectId}/reports`, req);
}

export async function listReports(projectId: string): Promise<EngineeringReport[]> {
  return api.request<EngineeringReport[]>('GET', `/projects/${projectId}/reports`);
}

export async function getReport(projectId: string, reportId: string): Promise<EngineeringReport> {
  return api.request<EngineeringReport>('GET', `/projects/${projectId}/reports/${reportId}`);
}

export function getReportDownloadUrl(projectId: string, reportId: string, format: 'html' | 'pdf' = 'html'): string {
  return `/api/v1/projects/${projectId}/reports/${reportId}/download?format=${format}`;
}

export async function listPlugins(): Promise<PluginInfo[]> {
  return api.request<PluginInfo[]>('GET', '/plugins');
}

export async function getPlugin(pluginId: string): Promise<PluginInfo> {
  return api.request<PluginInfo>('GET', `/plugins/${pluginId}`);
}

export async function enablePlugin(pluginId: string): Promise<{ id: string; enabled: boolean; status: string }> {
  return api.request<{ id: string; enabled: boolean; status: string }>('POST', `/plugins/${pluginId}/enable`);
}

export async function disablePlugin(pluginId: string): Promise<{ id: string; disabled: boolean; status: string }> {
  return api.request<{ id: string; disabled: boolean; status: string }>('POST', `/plugins/${pluginId}/disable`);
}

export async function listPluginCapabilities(): Promise<string[]> {
  return api.request<string[]>('GET', '/plugins/capabilities');
}

export async function listPluginGuiComponents(): Promise<any[]> {
  return api.request<any[]>('GET', '/plugins/gui-components');
}

export async function listPluginVisualizations(): Promise<any[]> {
  return api.request<any[]>('GET', '/plugins/visualizations');
}

export async function listTemplates(category?: string, query?: string): Promise<TemplateManifest[]> {
  let url = '/templates';
  const params: string[] = [];
  if (category) params.push(`category=${encodeURIComponent(category)}`);
  if (query) params.push(`query=${encodeURIComponent(query)}`);
  if (params.length) url += `?${params.join('&')}`;
  return api.request<TemplateManifest[]>('GET', url);
}

export async function getTemplateCategories(): Promise<string[]> {
  return api.request<string[]>('GET', '/templates/categories');
}

export async function getTemplate(templateId: string): Promise<TemplateManifest> {
  return api.request<TemplateManifest>('GET', `/templates/${templateId}`);
}

export async function validateTemplate(templateId: string): Promise<any> {
  return api.request<any>('POST', `/templates/${templateId}/validate`);
}

export async function createProjectFromTemplate(templateId: string, projectName: string, description?: string, parameters?: Record<string, any>): Promise<{ id: string; name: string }> {
  return api.request<{ id: string; name: string }>('POST', `/templates/${templateId}/create-project`, {
    project_name: projectName,
    description,
    parameters: parameters || {},
  });
}

export async function tryInvokeFs<T>(fn: () => Promise<T>): Promise<{ ok: true; value: T } | { ok: false; error: string }> {
  try {
    const value = await fn();
    return { ok: true, value };
  } catch (err) {
    return { ok: false, error: String(err) };
  }
}
