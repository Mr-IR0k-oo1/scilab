use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::default::Default;
use std::sync::{Arc, Mutex};
use tauri::AppHandle;

// Define the data structures for the widget API
#[derive(Debug, Clone, Serialize, Deserialize, Default)]
pub struct WidgetInstance {
    pub id: String,
    pub r#type: String,
    pub properties: WidgetProperties,
}

#[derive(Debug, Clone, Serialize, Deserialize, Default)]
pub struct WidgetProperties {
    pub name: Option<String>,
    pub value: Option<serde_json::Value>,
    pub label: Option<String>,
    pub text: Option<String>,
    pub placeholder: Option<String>,
    pub default_value: Option<serde_json::Value>,
    pub max_length: Option<usize>,
    pub min: Option<f64>,
    pub max: Option<f64>,
    pub step: Option<f64>,
    pub checked: Option<bool>,
    pub options: Option<Vec<String>>,
    pub default_index: Option<usize>,
    pub chart_reference: Option<String>,
    pub aspect_ratio: Option<f64>,
    pub rows: Option<usize>,
    pub columns: Option<usize>,
    pub data_source: Option<String>,
    pub border_style: Option<String>,
    pub background_color: Option<String>,
    pub children: Option<Vec<String>>,
    pub width: Option<u32>,
    pub height: Option<u32>,
    pub font_size: Option<u32>,
    pub color: Option<String>,
    pub align: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct WidgetType {
    pub r#type: String,
    pub name: String,
    pub category: String,
    pub properties: Vec<WidgetProperty>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct WidgetProperty {
    pub name: String,
    pub r#type: String, // string, number, boolean, color, etc.
    pub label: String,
    pub default: Option<serde_json::Value>,
    pub options: Option<Vec<String>>, // For dropdown/select properties
}

// Widget JSON for serialization
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct WidgetJSON {
    pub id: String,
    pub r#type: String,
    pub properties: WidgetProperties,
}

// Command response types
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GetWidgetTypeResult {
    pub widget_type: Option<WidgetType>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GetAllWidgetTypesResult {
    pub types: Vec<WidgetType>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GetWidgetTypesByCategoryResult {
    pub types: Vec<WidgetType>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CreateWidgetResult {
    pub widget: WidgetInstance,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GetWidgetResult {
    pub widget: Option<WidgetInstance>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SetPropertyResult {
    pub success: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct BindPropertyResult {
    pub success: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct UnbindPropertyResult {
    pub success: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SerializeWidgetResult {
    pub json: WidgetJSON,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DeserializeWidgetResult {
    pub widget: WidgetInstance,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct WidgetResult {
    pub success: bool,
}

// Widget state management
struct WidgetState {
    widgets: Mutex<HashMap<String, WidgetInstance>>,
    widget_types: Mutex<Vec<WidgetType>>,
    next_id: Mutex<u32>,
}

impl WidgetState {
    fn new() -> Self {
        // Initialize with some basic widget types
        let mut widget_types = vec![
            WidgetType {
                r#type: "button".to_string(),
                name: "Button".to_string(),
                category: "input".to_string(),
                properties: vec![
                    WidgetProperty {
                        name: "text".to_string(),
                        r#type: "string".to_string(),
                        label: "Button Text".to_string(),
                        default: Some(serde_json::Value::String("Button".to_string())),
                        options: None,
                    },
                    WidgetProperty {
                        name: "width".to_string(),
                        r#type: "number".to_string(),
                        label: "Width".to_string(),
                        default: Some(serde_json::Value::Number(serde_json::Number::from_f64(80.0).unwrap())),
                        options: None,
                    },
                    WidgetProperty {
                        name: "height".to_string(),
                        r#type: "number".to_string(),
                        label: "Height".to_string(),
                        default: Some(serde_json::Value::Number(serde_json::Number::from_f64(30.0).unwrap())),
                        options: None,
                    },
                ],
            },
            WidgetType {
                r#type: "label".to_string(),
                name: "Label".to_string(),
                category: "display".to_string(),
                properties: vec![
                    WidgetProperty {
                        name: "text".to_string(),
                        r#type: "string".to_string(),
                        label: "Text".to_string(),
                        default: Some(serde_json::Value::String("Label".to_string())),
                        options: None,
                    },
                    WidgetProperty {
                        name: "font_size".to_string(),
                        r#type: "number".to_string(),
                        label: "Font Size".to_string(),
                        default: Some(serde_json::Value::Number(serde_json::Number::from_f64(12.0).unwrap())),
                        options: None,
                    },
                    WidgetProperty {
                        name: "color".to_string(),
                        r#type: "string".to_string(),
                        label: "Text Color".to_string(),
                        default: Some(serde_json::Value::String("#000000".to_string())),
                        options: None,
                    },
                    WidgetProperty {
                        name: "align".to_string(),
                        r#type: "string".to_string(),
                        label: "Alignment".to_string(),
                        default: Some(serde_json::Value::String("left".to_string())),
                        options: Some(vec!["left".to_string(), "center".to_string(), "right".to_string()]),
                    },
                ],
            },
            WidgetType {
                r#type: "textfield".to_string(),
                name: "Text Field".to_string(),
                category: "input".to_string(),
                properties: vec![
                    WidgetProperty {
                        name: "placeholder".to_string(),
                        r#type: "string".to_string(),
                        label: "Placeholder".to_string(),
                        default: Some(serde_json::Value::String("Enter text...".to_string())),
                        options: None,
                    },
                    WidgetProperty {
                        name: "default_value".to_string(),
                        r#type: "string".to_string(),
                        label: "Default Value".to_string(),
                        default: Some(serde_json::Value::String("".to_string())),
                        options: None,
                    },
                    WidgetProperty {
                        name: "max_length".to_string(),
                        r#type: "number".to_string(),
                        label: "Max Length".to_string(),
                        default: Some(serde_json::Value::Number(100.into())),
                        options: None,
                    },
                ],
            },
            WidgetType {
                r#type: "numberinput".to_string(),
                name: "Number Input".to_string(),
                category: "input".to_string(),
                properties: vec![
                    WidgetProperty {
                        name: "min".to_string(),
                        r#type: "number".to_string(),
                        label: "Minimum Value".to_string(),
                        default: Some(serde_json::Value::Number(serde_json::Number::from_f64(0.0).unwrap())),
                        options: None,
                    },
                    WidgetProperty {
                        name: "max".to_string(),
                        r#type: "number".to_string(),
                        label: "Maximum Value".to_string(),
                        default: Some(serde_json::Value::Number(serde_json::Number::from_f64(100.0).unwrap())),
                        options: None,
                    },
                    WidgetProperty {
                        name: "step".to_string(),
                        r#type: "number".to_string(),
                        label: "Step Size".to_string(),
                        default: Some(serde_json::Value::Number(serde_json::Number::from_f64(1.0).unwrap())),
                        options: None,
                    },
                    WidgetProperty {
                        name: "default_value".to_string(),
                        r#type: "number".to_string(),
                        label: "Default Value".to_string(),
                        default: Some(serde_json::Value::Number(serde_json::Number::from_f64(0.0).unwrap())),
                        options: None,
                    },
                ],
            },
            WidgetType {
                r#type: "checkbox".to_string(),
                name: "Checkbox".to_string(),
                category: "input".to_string(),
                properties: vec![
                    WidgetProperty {
                        name: "label".to_string(),
                        r#type: "string".to_string(),
                        label: "Checkbox Label".to_string(),
                        default: Some(serde_json::Value::String("Checkbox".to_string())),
                        options: None,
                    },
                    WidgetProperty {
                        name: "checked".to_string(),
                        r#type: "boolean".to_string(),
                        label: "Checked".to_string(),
                        default: Some(serde_json::Value::Bool(false)),
                        options: None,
                    },
                ],
            },
            WidgetType {
                r#type: "dropdown".to_string(),
                name: "Dropdown".to_string(),
                category: "input".to_string(),
                properties: vec![
                    WidgetProperty {
                        name: "options".to_string(),
                        r#type: "array".to_string(),
                        label: "Options".to_string(),
                        default: Some(serde_json::Value::Array(vec![
                            serde_json::Value::String("Option 1".to_string()),
                            serde_json::Value::String("Option 2".to_string()),
                            serde_json::Value::String("Option 3".to_string()),
                        ])),
                        options: None,
                    },
                    WidgetProperty {
                        name: "default_index".to_string(),
                        r#type: "number".to_string(),
                        label: "Default Selection".to_string(),
                        default: Some(serde_json::Value::Number(0.into())),
                        options: None,
                    },
                ],
            },
            WidgetType {
                r#type: "plotcontainer".to_string(),
                name: "Plot Container".to_string(),
                category: "display".to_string(),
                properties: vec![
                    WidgetProperty {
                        name: "chart_reference".to_string(),
                        r#type: "string".to_string(),
                        label: "Chart Reference".to_string(),
                        default: None,
                        options: None,
                    },
                    WidgetProperty {
                        name: "aspect_ratio".to_string(),
                        r#type: "number".to_string(),
                        label: "Aspect Ratio".to_string(),
                        default: Some(serde_json::Value::Number(serde_json::Number::from_f64(1.0).unwrap())),
                        options: None,
                    },
                ],
            },
            WidgetType {
                r#type: "table".to_string(),
                name: "Table".to_string(),
                category: "display".to_string(),
                properties: vec![
                    WidgetProperty {
                        name: "rows".to_string(),
                        r#type: "number".to_string(),
                        label: "Number of Rows".to_string(),
                        default: Some(serde_json::Value::Number(serde_json::Number::from_f64(5.0).unwrap())),
                        options: None,
                    },
                    WidgetProperty {
                        name: "columns".to_string(),
                        r#type: "number".to_string(),
                        label: "Number of Columns".to_string(),
                        default: Some(serde_json::Value::Number(serde_json::Number::from_f64(3.0).unwrap())),
                        options: None,
                    },
                    WidgetProperty {
                        name: "data_source".to_string(),
                        r#type: "string".to_string(),
                        label: "Data Source".to_string(),
                        default: None,
                        options: None,
                    },
                ],
            },
            WidgetType {
                r#type: "panel".to_string(),
                name: "Panel".to_string(),
                category: "container".to_string(),
                properties: vec![
                    WidgetProperty {
                        name: "border_style".to_string(),
                        r#type: "string".to_string(),
                        label: "Border Style".to_string(),
                        default: Some(serde_json::Value::String("none".to_string())),
                        options: Some(vec!["none".to_string(), "solid".to_string(), "dashed".to_string(), "dotted".to_string()]),
                    },
                    WidgetProperty {
                        name: "background_color".to_string(),
                        r#type: "string".to_string(),
                        label: "Background Color".to_string(),
                        default: Some(serde_json::Value::String("transparent".to_string())),
                        options: None,
                    },
                    WidgetProperty {
                        name: "children".to_string(),
                        r#type: "array".to_string(),
                        label: "Child Widgets".to_string(),
                        default: Some(serde_json::Value::Array(vec![])),
                        options: None,
                    },
                ],
            },
        ];

        Self {
            widgets: Mutex::new(HashMap::new()),
            widget_types: Mutex::new(widget_types),
            next_id: Mutex::new(1),
        }
    }

    fn generate_id(&self) -> String {
        let mut id = self.next_id.lock().unwrap();
        let result = format!("widget-{}", *id);
        *id += 1;
        result
    }

    fn get_widget_type(&self, type_id: &str) -> Option<WidgetType> {
        let types = self.widget_types.lock().unwrap();
        types.iter().find(|t| t.r#type == type_id).cloned()
    }

    fn get_all_widget_types(&self) -> Vec<WidgetType> {
        let types = self.widget_types.lock().unwrap();
        types.clone()
    }

    fn get_widget_types_by_category(&self, category: &str) -> Vec<WidgetType> {
        let types = self.widget_types.lock().unwrap();
        types.iter()
            .filter(|t| t.category == category)
            .cloned()
            .collect()
    }

    fn create_widget(&self, type_id: String, properties: Option<WidgetProperties>) -> Result<WidgetInstance, String> {
        // Validate that the widget type exists
        let widget_type = self.get_widget_type(&type_id);
        if widget_type.is_none() {
            return Err(format!("Widget type '{}' not found", type_id));
        }

        let id = self.generate_id();
        let mut widget = WidgetInstance {
            id: id.clone(),
            r#type: type_id,
            properties: properties.unwrap_or_default(),
        };

        // Set default properties based on the widget type
        if let Some(ref widget_type) = widget_type {
            for prop in &widget_type.properties {
                // If the property doesn't have a value set, use the default
                let prop_name = &prop.name;
                let is_set = match prop_name.as_str() {
                    "text" => widget.properties.text.is_some(),
                    "value" => widget.properties.value.is_some(),
                    "label" => widget.properties.label.is_some(),
                    "placeholder" => widget.properties.placeholder.is_some(),
                    "default_value" => widget.properties.default_value.is_some(),
                    "max_length" => widget.properties.max_length.is_some(),
                    "min" => widget.properties.min.is_some(),
                    "max" => widget.properties.max.is_some(),
                    "step" => widget.properties.step.is_some(),
                    "checked" => widget.properties.checked.is_some(),
                    "options" => widget.properties.options.is_some(),
                    "default_index" => widget.properties.default_index.is_some(),
                    "chart_reference" => widget.properties.chart_reference.is_some(),
                    "aspect_ratio" => widget.properties.aspect_ratio.is_some(),
                    "rows" => widget.properties.rows.is_some(),
                    "columns" => widget.properties.columns.is_some(),
                    "data_source" => widget.properties.data_source.is_some(),
                    "border_style" => widget.properties.border_style.is_some(),
                    "background_color" => widget.properties.background_color.is_some(),
                    "children" => widget.properties.children.is_some(),
                    "width" => widget.properties.width.is_some(),
                    "height" => widget.properties.height.is_some(),
                    "font_size" => widget.properties.font_size.is_some(),
                    "color" => widget.properties.color.is_some(),
                    "align" => widget.properties.align.is_some(),
                    _ => false,
                };

                if !is_set {
                    // Set the default value
                    match prop_name.as_str() {
                        "text" => widget.properties.text = prop.default.clone().and_then(|v| v.as_str().map(String::from)),
                        "value" => widget.properties.value = prop.default.clone(),
                        "label" => widget.properties.label = prop.default.clone().and_then(|v| v.as_str().map(String::from)),
                        "placeholder" => widget.properties.placeholder = prop.default.clone().and_then(|v| v.as_str().map(String::from)),
                        "default_value" => widget.properties.default_value = prop.default.clone(),
                        "max_length" => widget.properties.max_length = prop.default.clone().and_then(|v| v.as_u64().map(|x| x as usize)),
                        "min" => widget.properties.min = prop.default.clone().and_then(|v| v.as_f64()),
                        "max" => widget.properties.max = prop.default.clone().and_then(|v| v.as_f64()),
                        "step" => widget.properties.step = prop.default.clone().and_then(|v| v.as_f64()),
                        "checked" => widget.properties.checked = prop.default.clone().and_then(|v| v.as_bool()),
                        "options" => widget.properties.options = prop.default.clone().and_then(|v| v.as_array().map(|arr| {
                            arr.iter()
                                .filter_map(|v| v.as_str().map(String::from))
                                .collect()
                        })),
                        "default_index" => widget.properties.default_index = prop.default.clone().and_then(|v| v.as_u64().map(|x| x as usize)),
                        "chart_reference" => widget.properties.chart_reference = prop.default.clone().and_then(|v| v.as_str().map(String::from)),
                        "aspect_ratio" => widget.properties.aspect_ratio = prop.default.clone().and_then(|v| v.as_f64()),
                        "rows" => widget.properties.rows = prop.default.clone().and_then(|v| v.as_u64().map(|x| x as usize)),
                        "columns" => widget.properties.columns = prop.default.clone().and_then(|v| v.as_u64().map(|x| x as usize)),
                        "data_source" => widget.properties.data_source = prop.default.clone().and_then(|v| v.as_str().map(String::from)),
                        "border_style" => widget.properties.border_style = prop.default.clone().and_then(|v| v.as_str().map(String::from)),
                        "background_color" => widget.properties.background_color = prop.default.clone().and_then(|v| v.as_str().map(String::from)),
                        "children" => widget.properties.children = prop.default.clone().and_then(|v| v.as_array().map(|arr| {
                            arr.iter()
                                .filter_map(|v| v.as_str().map(String::from))
                                .collect()
                        })),
                        "width" => widget.properties.width = prop.default.clone().and_then(|v| v.as_u64().map(|x| x as u32)),
                        "height" => widget.properties.height = prop.default.clone().and_then(|v| v.as_u64().map(|x| x as u32)),
                        "font_size" => widget.properties.font_size = prop.default.clone().and_then(|v| v.as_u64().map(|x| x as u32)),
                        "color" => widget.properties.color = prop.default.clone().and_then(|v| v.as_str().map(String::from)),
                        "align" => widget.properties.align = prop.default.clone().and_then(|v| v.as_str().map(String::from)),
                        _ => {}
                    }
                }
            }
        }

        let mut widgets = self.widgets.lock().unwrap();
        widgets.insert(id.clone(), widget.clone());

        Ok(widget)
    }

    fn get_widget(&self, widget_id: &str) -> Option<WidgetInstance> {
        let widgets = self.widgets.lock().unwrap();
        widgets.get(widget_id).cloned()
    }

    fn destroy_widget(&self, widget_id: &str) -> bool {
        let mut widgets = self.widgets.lock().unwrap();
        widgets.remove(widget_id).is_some()
    }

    fn set_property(&self, widget_id: &str, name: String, value: serde_json::Value) -> bool {
        let mut widgets = self.widgets.lock().unwrap();
        if let Some(widget) = widgets.get_mut(widget_id) {
            match name.as_str() {
                "text" => widget.properties.text = value.as_str().map(String::from),
                "value" => widget.properties.value = Some(value),
                "label" => widget.properties.label = value.as_str().map(String::from),
                "placeholder" => widget.properties.placeholder = value.as_str().map(String::from),
                "default_value" => widget.properties.default_value = Some(value),
                "max_length" => widget.properties.max_length = value.as_u64().map(|x| x as usize),
                "min" => widget.properties.min = value.as_f64(),
                "max" => widget.properties.max = value.as_f64(),
                "step" => widget.properties.step = value.as_f64(),
                "checked" => widget.properties.checked = value.as_bool(),
                "options" => widget.properties.options = value.as_array().map(|arr| {
                    arr.iter()
                        .filter_map(|v| v.as_str().map(String::from))
                        .collect()
                }),
                "default_index" => widget.properties.default_index = value.as_u64().map(|x| x as usize),
                "chart_reference" => widget.properties.chart_reference = value.as_str().map(String::from),
                "aspect_ratio" => widget.properties.aspect_ratio = value.as_f64(),
                "rows" => widget.properties.rows = value.as_u64().map(|x| x as usize),
                "columns" => widget.properties.columns = value.as_u64().map(|x| x as usize),
                "data_source" => widget.properties.data_source = value.as_str().map(String::from),
                "border_style" => widget.properties.border_style = value.as_str().map(String::from),
                "background_color" => widget.properties.background_color = value.as_str().map(String::from),
                "width" => widget.properties.width = value.as_u64().map(|x| x as u32),
                "height" => widget.properties.height = value.as_u64().map(|x| x as u32),
                "font_size" => widget.properties.font_size = value.as_u64().map(|x| x as u32),
                "color" => widget.properties.color = value.as_str().map(String::from),
                "align" => widget.properties.align = value.as_str().map(String::from),
                "children" => widget.properties.children = value.as_array().map(|arr| {
                    arr.iter()
                        .filter_map(|v| v.as_str().map(String::from))
                        .collect()
                }),
                _ => return false, // Unknown property
            }
            true
        } else {
            false
        }
    }

    fn bind_property(&self, widget_id: &str, name: String, expression: String) -> bool {
        // In a real implementation, we would store the binding and update the property
        // when the expression value changes
        // For now, we'll just store it as a property value for simplicity
        let mut widgets = self.widgets.lock().unwrap();
        if let Some(widget) = widgets.get_mut(widget_id) {
            match name.as_str() {
                "text" => widget.properties.text = Some(expression),
                "value" => widget.properties.value = Some(serde_json::Value::String(expression)),
                "label" => widget.properties.label = Some(expression),
                "placeholder" => widget.properties.placeholder = Some(expression),
                "default_value" => widget.properties.default_value = Some(serde_json::Value::String(expression)),
                "chart_reference" => widget.properties.chart_reference = Some(expression),
                _ => return false, // Not a bindable property
            }
            true
        } else {
            false
        }
    }

    fn unbind_property(&self, widget_id: &str, name: String) -> bool {
        // In a real implementation, we would remove the binding
        // For now, we'll just set the property to None or a default value
        let mut widgets = self.widgets.lock().unwrap();
        if let Some(widget) = widgets.get_mut(widget_id) {
            match name.as_str() {
                "text" => widget.properties.text = None,
                "value" => widget.properties.value = None,
                "label" => widget.properties.label = None,
                "placeholder" => widget.properties.placeholder = None,
                "default_value" => widget.properties.default_value = None,
                "chart_reference" => widget.properties.chart_reference = None,
                _ => return false, // Not a bindable property
            }
            true
        } else {
            false
        }
    }

    fn serialize_widget(&self, widget_id: &str) -> Option<WidgetJSON> {
        let widgets = self.widgets.lock().unwrap();
        widgets.get(widget_id).map(|widget| WidgetJSON {
            id: widget.id.clone(),
            r#type: widget.r#type.clone(),
            properties: widget.properties.clone(),
        })
    }

    fn deserialize_widget(&self, json: WidgetJSON) -> Result<WidgetInstance, String> {
        // Validate that the widget type exists
        let widget_type = self.get_widget_type(&json.r#type);
        if widget_type.is_none() {
            return Err(format!("Widget type '{}' not found", json.r#type));
        }

        let widget = WidgetInstance {
            id: json.id,
            r#type: json.r#type,
            properties: json.properties,
        };

        let mut widgets = self.widgets.lock().unwrap();
        widgets.insert(widget.id.clone(), widget.clone());

        Ok(widget)
    }
}

// Widget command implementations
#[tauri::command]
pub fn widget_get_widget_type(
    _app_handle: tauri::AppHandle,
    type_id: String,
) -> Result<GetWidgetTypeResult, String> {
    let state = WidgetState::new();
    let widget_type = state.get_widget_type(&type_id);
    Ok(GetWidgetTypeResult { widget_type })
}

#[tauri::command]
pub fn widget_get_all_widget_types(
    _app_handle: tauri::AppHandle,
) -> Result<GetAllWidgetTypesResult, String> {
    let state = WidgetState::new();
    let types = state.get_all_widget_types();
    Ok(GetAllWidgetTypesResult { types })
}

#[tauri::command]
pub fn widget_get_widget_types_by_category(
    _app_handle: tauri::AppHandle,
    category: String,
) -> Result<GetWidgetTypesByCategoryResult, String> {
    let state = WidgetState::new();
    let types = state.get_widget_types_by_category(&category);
    Ok(GetWidgetTypesByCategoryResult { types })
}

#[tauri::command]
pub fn widget_create_widget(
    _app_handle: tauri::AppHandle,
    type_id: String,
    properties: Option<WidgetProperties>,
) -> Result<CreateWidgetResult, String> {
    let state = WidgetState::new();
    let widget = state.create_widget(type_id, properties)?;
    Ok(CreateWidgetResult { widget })
}

#[tauri::command]
pub fn widget_get_widget(
    _app_handle: tauri::AppHandle,
    widget_id: String,
) -> Result<GetWidgetResult, String> {
    let state = WidgetState::new();
    let widget = state.get_widget(&widget_id);
    Ok(GetWidgetResult { widget })
}

#[tauri::command]
pub fn widget_destroy_widget(
    _app_handle: tauri::AppHandle,
    widget_id: String,
) -> Result<WidgetResult, String> {
    let state = WidgetState::new();
    let success = state.destroy_widget(&widget_id);
    Ok(WidgetResult { success })
}

#[tauri::command]
pub fn widget_set_property(
    _app_handle: tauri::AppHandle,
    widget_id: String,
    name: String,
    value: serde_json::Value,
) -> Result<SetPropertyResult, String> {
    let state = WidgetState::new();
    let success = state.set_property(&widget_id, name, value);
    Ok(SetPropertyResult { success })
}

#[tauri::command]
pub fn widget_bind_property(
    _app_handle: tauri::AppHandle,
    widget_id: String,
    name: String,
    expression: String,
) -> Result<BindPropertyResult, String> {
    let state = WidgetState::new();
    let success = state.bind_property(&widget_id, name, expression);
    Ok(BindPropertyResult { success })
}

#[tauri::command]
pub fn widget_unbind_property(
    _app_handle: tauri::AppHandle,
    widget_id: String,
    name: String,
) -> Result<UnbindPropertyResult, String> {
    let state = WidgetState::new();
    let success = state.unbind_property(&widget_id, name);
    Ok(UnbindPropertyResult { success })
}

#[tauri::command]
pub fn widget_serialize_widget(
    _app_handle: tauri::AppHandle,
    widget_id: String,
) -> Result<SerializeWidgetResult, String> {
    let state = WidgetState::new();
    let json = state.serialize_widget(&widget_id)
        .ok_or_else(|| "Widget not found".to_string())?;
    Ok(SerializeWidgetResult { json })
}

#[tauri::command]
pub fn widget_deserialize_widget(
    _app_handle: tauri::AppHandle,
    json: WidgetJSON,
) -> Result<DeserializeWidgetResult, String> {
    let state = WidgetState::new();
    let widget = state.deserialize_widget(json)?;
    Ok(DeserializeWidgetResult { widget })
}