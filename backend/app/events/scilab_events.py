from typing import Any, Dict
from app.events.event_bus import global_event_bus

# Event Type Constants
SCILAB_DETECTED = "ScilabDetected"
SCILAB_STARTED = "ScilabStarted"
SCILAB_STOPPED = "ScilabStopped"
SCILAB_EXECUTION_STARTED = "ScilabExecutionStarted"
SCILAB_OUTPUT_RECEIVED = "ScilabOutputReceived"
SCILAB_EXECUTION_FINISHED = "ScilabExecutionFinished"
SCILAB_EXECUTION_FAILED = "ScilabExecutionFailed"
SCILAB_EXECUTION_CANCELLED = "ScilabExecutionCancelled"


def publish_scilab_event(event_type: str, data: Dict[str, Any]) -> None:
    """Publish a Scilab event to the global Phase 1 EventBus."""
    global_event_bus.publish(event_type, data)
