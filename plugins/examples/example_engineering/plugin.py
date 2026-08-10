from app.sdk import (
    GUIComponentMetadata,
    Plugin,
    PluginContext,
    VisualizationExtensionMetadata,
)


class ExampleEngineeringPlugin(Plugin):
    def initialize(self, context: PluginContext) -> None:
        super().initialize(context)
        if self.context:
            self.context.logger.info("Initializing ExampleEngineeringPlugin...")
            self.context.subscribe_event("experiment.completed", self.on_experiment_completed)

    def start(self) -> None:
        if self.context:
            self.context.logger.info("Starting ExampleEngineeringPlugin...")

    def stop(self) -> None:
        if self.context:
            self.context.logger.info("Stopping ExampleEngineeringPlugin...")

    def dispose(self) -> None:
        if self.context:
            self.context.logger.info("Disposing ExampleEngineeringPlugin...")

    def get_gui_components(self) -> list:
        return [
            GUIComponentMetadata(
                component_type="plugin_gauge",
                display_name="Engineering Analog Gauge",
                category="Instrumentation",
                schema_def={
                    "properties": {
                        "min_val": {"type": "number", "default": 0},
                        "max_val": {"type": "number", "default": 100},
                        "units": {"type": "string", "default": "RPM"},
                    }
                },
                renderer_metadata={"icon": "gauge-icon"},
                version="0.1.0",
            )
        ]

    def get_visualizations(self) -> list:
        return [
            VisualizationExtensionMetadata(
                type="polar_plot",
                name="Polar Radiation Diagram",
                schema_def={"angle_col": "theta", "radius_col": "gain"},
                input_requirements={"numeric_columns": 2},
                output_format="polar_series",
                version="0.1.0",
            )
        ]

    def on_experiment_completed(self, data: dict) -> None:
        if self.context:
            self.context.logger.info(f"Received experiment completion event in plugin: {data}")
