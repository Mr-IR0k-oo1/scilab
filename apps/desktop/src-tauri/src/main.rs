#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use std::sync::Mutex;
use tauri::{RunEvent, Manager};
use tauri_plugin_shell::process::CommandChild;
use tauri_plugin_shell::ShellExt;
use std::process::Command;

enum BackendChild {
    Sidecar(CommandChild),
    Std(std::process::Child),
}

struct BackendProcess {
    child: Option<BackendChild>,
}

fn main() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .setup(|app| {
            let child_proc = match app.shell().sidecar("fossee-backend") {
                Ok(mut command) => {
                    match command.spawn() {
                        Ok((_rx, child_proc)) => {
                            println!("Started Python backend sidecar");
                            Some(BackendChild::Sidecar(child_proc))
                        }
                        Err(e) => {
                            eprintln!("Failed to spawn Python backend sidecar: {}", e);
                            None
                        }
                    }
                }
                Err(e) => {
                    eprintln!("Could not find sidecar (perhaps not running in release mode or missing sidecar configuration): {}", e);
                    
                    // Fallback to dev mode
                    let cwd = std::env::current_dir().unwrap_or_default();
                    let backend_dir = if cwd.join("backend").exists() {
                        cwd.join("backend")
                    } else {
                        cwd
                    };

                    let python_bin = if backend_dir.join("venv/bin/python").exists() {
                        backend_dir.join("venv/bin/python").to_str().unwrap().to_string()
                    } else {
                        "python3".to_string()
                    };

                    Command::new(python_bin)
                        .arg("-m")
                        .arg("uvicorn")
                        .arg("fossee_backend.main:app")
                        .arg("--host")
                        .arg("127.0.0.1")
                        .arg("--port")
                        .arg("8747")
                        .current_dir(backend_dir)
                        .spawn()
                        .ok()
                        .map(BackendChild::Std)
                }
            };

            app.manage(Mutex::new(BackendProcess { child: child_proc }));
            Ok(())
        })
        .build(tauri::generate_context!())
        .expect("error while running tauri application")
        .run(|app_handle, event| {
            if let RunEvent::Exit = event {
                if let Some(state) = app_handle.try_state::<Mutex<BackendProcess>>() {
                    if let Ok(mut bp) = state.lock() {
                        if let Some(child) = bp.child.take() {
                            match child {
                                BackendChild::Sidecar(c) => { let _ = c.kill(); },
                                BackendChild::Std(mut c) => { let _ = c.kill(); let _ = c.wait(); },
                            }
                            println!("Killed Python backend");
                        }
                    }
                }
            }
        });
}