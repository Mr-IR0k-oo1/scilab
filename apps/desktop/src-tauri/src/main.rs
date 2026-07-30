#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

mod fs;
mod scilab;
mod visualization;
mod widgets;

use scilab::{ExecuteResult, ScilabProcess, ScilabStatus};
use std::sync::Arc;
use tokio::sync::Mutex;

struct AppState {
    scilab: ScilabProcess,
}

#[tauri::command]
async fn start_scilab(state: tauri::State<'_, Arc<Mutex<AppState>>>) -> Result<ScilabStatus, String> {
    let state = state.lock().await;
    state.scilab.start().await
}

#[tauri::command]
async fn execute_code(
    state: tauri::State<'_, Arc<Mutex<AppState>>>,
    code: String,
) -> Result<ExecuteResult, String> {
    let state = state.lock().await;
    state.scilab.execute(&code).await
}

#[tauri::command]
async fn stop_scilab(state: tauri::State<'_, Arc<Mutex<AppState>>>) -> Result<(), String> {
    let state = state.lock().await;
    state.scilab.stop().await
}

#[tauri::command]
async fn scilab_status(state: tauri::State<'_, Arc<Mutex<AppState>>>) -> Result<ScilabStatus, String> {
    let state = state.lock().await;
    Ok(state.scilab.status().await)
}

fn main() {
    let state = Arc::new(Mutex::new(AppState {
        scilab: ScilabProcess::new(),
    }));

    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .manage(state)
        .invoke_handler(tauri::generate_handler![
            start_scilab,
            execute_code,
            stop_scilab,
            scilab_status,
            fs::read_text_file,
            fs::write_text_file,
            fs::list_directory,
            fs::create_directory,
            fs::remove_file,
            fs::remove_directory,
            fs::file_exists,
            fs::path_info,
            fs::get_app_data_dir,
            fs::get_documents_dir,
            fs::get_project_dir,
            fs::create_project,
            fs::list_projects,
            fs::rename_path,
            fs::update_project_metadata,
            fs::delete_project,
            // Visualization commands
            visualization::viz_create_chart,
            visualization::viz_get_chart,
            visualization::viz_update_chart,
            visualization::viz_update_chart_data,
            visualization::viz_destroy_chart,
            visualization::viz_export_chart,
            visualization::viz_get_supported_types,
            visualization::viz_set_theme,
            // Widget commands
            widgets::widget_get_widget_type,
            widgets::widget_get_all_widget_types,
            widgets::widget_get_widget_types_by_category,
            widgets::widget_create_widget,
            widgets::widget_get_widget,
            widgets::widget_destroy_widget,
            widgets::widget_set_property,
            widgets::widget_bind_property,
            widgets::widget_unbind_property,
            widgets::widget_serialize_widget,
            widgets::widget_deserialize_widget,
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}