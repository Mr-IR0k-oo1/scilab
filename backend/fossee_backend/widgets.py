from typing import Dict, List, Optional, Any
from .models import WidgetInstance, WidgetType, WidgetProperties, WidgetProperty

default_widget_types = [
    WidgetType(
        type="button", name="Button", category="input",
        properties=[
            WidgetProperty(name="text", type="string", label="Button Text", default="Button"),
            WidgetProperty(name="width", type="number", label="Width", default=80.0),
            WidgetProperty(name="height", type="number", label="Height", default=30.0),
        ]
    ),
    WidgetType(
        type="label", name="Label", category="display",
        properties=[
            WidgetProperty(name="text", type="string", label="Text", default="Label"),
            WidgetProperty(name="font_size", type="number", label="Font Size", default=12.0),
            WidgetProperty(name="color", type="string", label="Text Color", default="#000000"),
            WidgetProperty(name="align", type="string", label="Alignment", default="left", options=["left", "center", "right"]),
        ]
    )
]

widgets: Dict[str, WidgetInstance] = {}
widget_types: List[WidgetType] = default_widget_types
next_id: int = 1

def generate_id() -> str:
    global next_id
    id_str = f"widget-{next_id}"
    next_id += 1
    return id_str

def get_widget_type(type_id: str) -> Optional[WidgetType]:
    return next((t for t in widget_types if t.type == type_id), None)

def get_all_widget_types() -> List[WidgetType]:
    return widget_types

def get_widget_types_by_category(category: str) -> List[WidgetType]:
    return [t for t in widget_types if t.category == category]

def create_widget(type_id: str, properties: Optional[WidgetProperties] = None) -> WidgetInstance:
    wt = get_widget_type(type_id)
    if not wt:
        raise ValueError(f"Widget type '{type_id}' not found")
    
    props = properties if properties else WidgetProperties()
    for p in wt.properties:
        if getattr(props, p.name, None) is None:
            setattr(props, p.name, p.default)
            
    w_id = generate_id()
    w = WidgetInstance(id=w_id, type=type_id, properties=props)
    widgets[w_id] = w
    return w

def get_widget(widget_id: str) -> Optional[WidgetInstance]:
    return widgets.get(widget_id)

def destroy_widget(widget_id: str) -> bool:
    if widget_id in widgets:
        del widgets[widget_id]
        return True
    return False

def set_property(widget_id: str, name: str, value: Any) -> bool:
    if widget_id in widgets:
        w = widgets[widget_id]
        if hasattr(w.properties, name):
            setattr(w.properties, name, value)
            return True
    return False

def serialize_widget(widget_id: str) -> Optional[dict]:
    if widget_id in widgets:
        w = widgets[widget_id]
        return {"id": w.id, "type": w.type, "properties": w.properties.dict()}
    return None

def deserialize_widget(json_data: dict) -> WidgetInstance:
    w_type = json_data.get("type")
    wt = get_widget_type(w_type)
    if not wt:
        raise ValueError(f"Widget type '{w_type}' not found")
    
    w = WidgetInstance(**json_data)
    widgets[w.id] = w
    return w
