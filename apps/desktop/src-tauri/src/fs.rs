use serde::{Deserialize, Serialize};
use std::path::{Path, PathBuf};
use tauri::Manager;
use tokio::fs;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DirEntry {
    pub name: String,
    pub path: String,
    pub is_dir: bool,
    pub size: u64,
    pub modified: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PathInfo {
    pub exists: bool,
    pub is_dir: bool,
    pub is_file: bool,
    pub size: u64,
    pub modified: String,
    pub extension: Option<String>,
}

#[tauri::command]
pub async fn read_text_file(path: String) -> Result<String, String> {
    fs::read_to_string(&path)
        .await
        .map_err(|e| format!("Failed to read file: {}", e))
}

#[tauri::command]
pub async fn write_text_file(path: String, content: String) -> Result<(), String> {
    if let Some(parent) = Path::new(&path).parent() {
        fs::create_dir_all(parent)
            .await
            .map_err(|e| format!("Failed to create parent directory: {}", e))?;
    }
    fs::write(&path, &content)
        .await
        .map_err(|e| format!("Failed to write file: {}", e))
}

#[tauri::command]
pub async fn list_directory(path: String) -> Result<Vec<DirEntry>, String> {
    let mut entries = Vec::new();
    let mut read_dir = fs::read_dir(&path)
        .await
        .map_err(|e| format!("Failed to read directory: {}", e))?;

    while let Some(entry) = read_dir
        .next_entry()
        .await
        .map_err(|e| format!("Failed to read entry: {}", e))?
    {
        let metadata = entry
            .metadata()
            .await
            .map_err(|e| format!("Failed to read metadata: {}", e))?;
        entries.push(DirEntry {
            name: entry.file_name().to_string_lossy().to_string(),
            path: entry.path().to_string_lossy().to_string(),
            is_dir: metadata.is_dir(),
            size: metadata.len(),
            modified: metadata
                .modified()
                .ok()
                .map(|t| {
                    let duration = t
                        .duration_since(std::time::UNIX_EPOCH)
                        .unwrap_or_default();
                    duration.as_secs().to_string()
                })
                .unwrap_or_default(),
        });
    }

    entries.sort_by(|a, b| {
        if a.is_dir != b.is_dir {
            b.is_dir.cmp(&a.is_dir)
        } else {
            a.name.cmp(&b.name)
        }
    });

    Ok(entries)
}

#[tauri::command]
pub async fn create_directory(path: String) -> Result<(), String> {
    fs::create_dir_all(&path)
        .await
        .map_err(|e| format!("Failed to create directory: {}", e))
}

#[tauri::command]
pub async fn remove_file(path: String) -> Result<(), String> {
    fs::remove_file(&path)
        .await
        .map_err(|e| format!("Failed to remove file: {}", e))
}

#[tauri::command]
pub async fn remove_directory(path: String) -> Result<(), String> {
    fs::remove_dir_all(&path)
        .await
        .map_err(|e| format!("Failed to remove directory: {}", e))
}

#[tauri::command]
pub async fn file_exists(path: String) -> bool {
    Path::new(&path).exists()
}

#[tauri::command]
pub async fn path_info(path: String) -> PathInfo {
    let path = Path::new(&path);
    let metadata = path.symlink_metadata().ok();

    PathInfo {
        exists: path.exists(),
        is_dir: metadata.as_ref().map(|m| m.is_dir()).unwrap_or(false),
        is_file: metadata.as_ref().map(|m| m.is_file()).unwrap_or(false),
        size: metadata.as_ref().map(|m| m.len()).unwrap_or(0),
        modified: metadata
            .and_then(|m| m.modified().ok())
            .map(|t| {
                t.duration_since(std::time::UNIX_EPOCH)
                    .unwrap_or_default()
                    .as_secs()
                    .to_string()
            })
            .unwrap_or_default(),
        extension: path.extension().map(|e| e.to_string_lossy().to_string()),
    }
}

#[tauri::command]
pub async fn get_app_data_dir(app: tauri::AppHandle) -> Result<String, String> {
    app.path()
        .app_data_dir()
        .map(|p| p.to_string_lossy().to_string())
        .map_err(|e| format!("Failed to get app data dir: {}", e))
}

#[tauri::command]
pub async fn get_documents_dir(app: tauri::AppHandle) -> Result<String, String> {
    app.path()
        .document_dir()
        .map(|p| p.to_string_lossy().to_string())
        .map_err(|e| format!("Failed to get documents dir: {}", e))
}

pub fn get_fossee_dir(app: &tauri::AppHandle) -> Result<PathBuf, String> {
    let docs = app
        .path()
        .document_dir()
        .map_err(|e| format!("Failed to get documents dir: {}", e))?;
    Ok(docs.join("FOSSEE"))
}

#[tauri::command]
pub async fn get_project_dir(app: tauri::AppHandle) -> Result<String, String> {
    get_fossee_dir(&app).map(|p| p.to_string_lossy().to_string())
}

#[tauri::command]
pub async fn create_project(name: String, tools: Vec<String>, app: tauri::AppHandle) -> Result<String, String> {
    let base = get_fossee_dir(&app)?;
    let project_dir = base.join(&name);

    if project_dir.exists() {
        return Err(format!("Project '{}' already exists", name));
    }

    let dirs = ["src", "data", "reports", "build"];
    for d in &dirs {
        fs::create_dir_all(project_dir.join(d))
            .await
            .map_err(|e| format!("Failed to create {} directory: {}", d, e))?;
    }

    let meta = serde_json::json!({
        "name": name,
        "version": "1.0",
        "tools": tools,
        "created": chrono_now()
    });

    let meta_str = serde_json::to_string_pretty(&meta)
        .map_err(|e| format!("Failed to serialize metadata: {}", e))?;

    fs::write(project_dir.join("project.json"), &meta_str)
        .await
        .map_err(|e| format!("Failed to write project metadata: {}", e))?;

    Ok(project_dir.to_string_lossy().to_string())
}

#[tauri::command]
pub async fn list_projects(app: tauri::AppHandle) -> Result<Vec<DirEntry>, String> {
    let base = get_fossee_dir(&app)?;

    if !base.exists() {
        return Ok(vec![]);
    }

    let mut entries = Vec::new();
    let mut read_dir = fs::read_dir(&base)
        .await
        .map_err(|e| format!("Failed to list projects: {}", e))?;

    while let Some(entry) = read_dir
        .next_entry()
        .await
        .map_err(|e| format!("Failed to read entry: {}", e))?
    {
        if !entry.metadata().await.map(|m| m.is_dir()).unwrap_or(false) {
            continue;
        }

        let project_json = entry.path().join("project.json");
        if !project_json.exists() {
            continue;
        }

        let meta_content = fs::read_to_string(&project_json).await.unwrap_or_default();
        let meta: serde_json::Value = serde_json::from_str(&meta_content).unwrap_or_default();

        let md = entry.metadata().await.ok();

        entries.push(DirEntry {
            name: meta["name"].as_str().unwrap_or(entry.file_name().to_str().unwrap_or("")).to_string(),
            path: entry.path().to_string_lossy().to_string(),
            is_dir: true,
            size: md.as_ref().map(|m| m.len()).unwrap_or(0),
            modified: md
                .as_ref()
                .and_then(|m| m.modified().ok())
                .map(|t| t.duration_since(std::time::UNIX_EPOCH).unwrap_or_default().as_secs().to_string())
                .unwrap_or_default(),
        });
    }

    Ok(entries)
}

#[tauri::command]
pub async fn rename_path(old_path: String, new_path: String) -> Result<(), String> {
    fs::rename(&old_path, &new_path)
        .await
        .map_err(|e| format!("Failed to rename: {}", e))
}

#[tauri::command]
pub async fn update_project_metadata(name: String, app: tauri::AppHandle) -> Result<(), String> {
    let base = get_fossee_dir(&app)?;
    let project_dir = base.join(&name);
    let meta_path = project_dir.join("project.json");

    if !meta_path.exists() {
        return Err(format!("Project '{}' not found", name));
    }

    let content = fs::read_to_string(&meta_path)
        .await
        .map_err(|e| format!("Failed to read project metadata: {}", e))?;

    let mut meta: serde_json::Value = serde_json::from_str(&content)
        .map_err(|e| format!("Failed to parse project metadata: {}", e))?;

    if let Some(obj) = meta.as_object_mut() {
        obj.insert("modified".to_string(), serde_json::Value::String(chrono_now()));
    }

    let new_content = serde_json::to_string_pretty(&meta)
        .map_err(|e| format!("Failed to serialize metadata: {}", e))?;

    fs::write(&meta_path, &new_content)
        .await
        .map_err(|e| format!("Failed to write project metadata: {}", e))
}

#[tauri::command]
pub async fn delete_project(name: String, app: tauri::AppHandle) -> Result<(), String> {
    let base = get_fossee_dir(&app)?;
    let project_dir = base.join(&name);

    if !project_dir.exists() {
        return Err(format!("Project '{}' not found", name));
    }

    fs::remove_dir_all(&project_dir)
        .await
        .map_err(|e| format!("Failed to delete project: {}", e))
}

fn chrono_now() -> String {
    use std::time::{SystemTime, UNIX_EPOCH};
    let now = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap_or_default();
    now.as_secs().to_string()
}
