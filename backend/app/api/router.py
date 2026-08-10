import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.api.routes import datasets, health, plugins, projects, reports, results, scilab, system, templates, visualizations, workspace
from app.core.logging import logger

api_router = APIRouter()

api_router.include_router(health.router, tags=["Health"])
api_router.include_router(system.router, tags=["System"])
api_router.include_router(workspace.router, tags=["Workspaces"])
api_router.include_router(projects.router, tags=["Projects"])
api_router.include_router(scilab.router, tags=["Scilab Runtime"])
api_router.include_router(datasets.router, tags=["Datasets Engine"])
api_router.include_router(visualizations.router, tags=["Visualization Engine"])
api_router.include_router(results.router, tags=["Results Engine"])
api_router.include_router(reports.router, tags=["Report Engine"])
api_router.include_router(plugins.router, tags=["Plugin SDK & Extensions"])
api_router.include_router(templates.router, tags=["Engineering Template Library"])


@api_router.websocket("/ws/scilab")
async def scilab_websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    logger.info("Scilab WebSocket client connected")
    try:
        await websocket.send_text(json.dumps({
            "type": "session_connected",
            "message": "Connected to Scilab Runtime Stream"
        }))
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)
            cmd_type = payload.get("type")
            if cmd_type == "execute":
                cmd = payload.get("command", "")
                await websocket.send_text(json.dumps({
                    "type": "execution_started",
                    "command": cmd,
                }))
                from app.services.scilab_service import ScilabService
                res = await ScilabService.execute_command(
                    command=cmd,
                    websocket_broadcaster=lambda msg: websocket.send_text(json.dumps(msg))
                )
                await websocket.send_text(json.dumps({
                    "type": "execution_finished",
                    "execution_id": res.id,
                    "success": res.success,
                    "stdout": res.stdout,
                    "stderr": res.stderr,
                }))
    except WebSocketDisconnect:
        logger.info("Scilab WebSocket client disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
