use std::process::Stdio;
use std::sync::Arc;
use tokio::io::{AsyncBufReadExt, AsyncWriteExt, BufReader};
use tokio::process::{Child, Command};
use tokio::sync::Mutex;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ExecuteResult {
    pub output: String,
    pub error: Option<String>,
    pub success: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ScilabStatus {
    pub running: bool,
    pub version: Option<String>,
    pub pid: Option<u32>,
}

struct Inner {
    child: Option<Child>,
}

pub struct ScilabProcess {
    inner: Arc<Mutex<Inner>>,
}

impl ScilabProcess {
    pub fn new() -> Self {
        Self {
            inner: Arc::new(Mutex::new(Inner {
                child: None,
            })),
        }
    }

    pub async fn start(&self) -> Result<ScilabStatus, String> {
        let mut inner = self.inner.lock().await;

        if inner.child.is_some() {
            return Err("Scilab is already running".into());
        }

        let child = Command::new("scilab-cli")
            .args(["--nw", "--noecho"])
            .stdin(Stdio::piped())
            .stdout(Stdio::piped())
            .stderr(Stdio::piped())
            .kill_on_drop(true)
            .spawn()
            .map_err(|e| {
                if e.kind() == std::io::ErrorKind::NotFound {
                    "Scilab is not installed or not found in PATH. Install Scilab: https://www.scilab.org/download/scilab-2025.1.0".to_string()
                } else {
                    format!("Failed to start Scilab: {}", e)
                }
            })?;

        let pid = child.id();
        inner.child = Some(child);

        Ok(ScilabStatus {
            running: true,
            version: None,
            pid,
        })
    }

    pub async fn execute(&self, code: &str) -> Result<ExecuteResult, String> {
        let mut inner = self.inner.lock().await;

        let child = inner.child.as_mut().ok_or("Scilab is not running")?;

        let stdin = child.stdin.as_mut().ok_or("Failed to access stdin")?;
        let stdout = child.stdout.as_mut().ok_or("Failed to access stdout")?;

        let delimiter = "__SCILAB_END__";

        let wrapped = format!("{}\ndisp('{}');\n", code, delimiter);

        stdin.write_all(wrapped.as_bytes()).await.map_err(|e| format!("Failed to write to stdin: {}", e))?;
        stdin.flush().await.map_err(|e| format!("Failed to flush stdin: {}", e))?;

        let mut reader = BufReader::new(stdout);
        let mut output = String::new();
        let mut found_delimiter = false;

        let timeout = std::time::Duration::from_secs(30);
        let start = std::time::Instant::now();

        loop {
            if start.elapsed() > timeout {
                return Ok(ExecuteResult {
                    output,
                    error: Some("Execution timed out".into()),
                    success: false,
                });
            }

            let mut line = String::new();
            match tokio::time::timeout(
                std::time::Duration::from_millis(500),
                reader.read_line(&mut line),
            ).await {
                Ok(Ok(0)) => {
                    break;
                }
                Ok(Ok(_)) => {
                    if line.contains(delimiter) {
                        found_delimiter = true;
                        break;
                    }
                    output.push_str(&line);
                }
                Ok(Err(e)) => {
                    return Ok(ExecuteResult {
                        output,
                        error: Some(format!("Read error: {}", e)),
                        success: false,
                    });
                }
                Err(_) => {
                    continue;
                }
            }
        }

        Ok(ExecuteResult {
            output: output.trim_end().to_string(),
            error: None,
            success: found_delimiter,
        })
    }

    pub async fn stop(&self) -> Result<(), String> {
        let mut inner = self.inner.lock().await;

        if let Some(mut child) = inner.child.take() {
            let _ = child.kill().await;
            let _ = child.wait().await;
        }

        Ok(())
    }

    pub async fn status(&self) -> ScilabStatus {
        let inner = self.inner.lock().await;

        match &inner.child {
            Some(child) => ScilabStatus {
                running: true,
                version: None,
                pid: child.id(),
            },
            None => ScilabStatus {
                running: false,
                version: None,
                pid: None,
            },
        }
    }
}
