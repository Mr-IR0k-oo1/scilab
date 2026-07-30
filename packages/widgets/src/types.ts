export interface Widget {
  id: string;
  type: WidgetType;
  x: number;
  y: number;
  width: number;
  height: number;
  props: Record<string, string>;
}

export type WidgetType = 'button' | 'label' | 'text-field' | 'slider' | 'checkbox' | 'plot' | 'panel';

export interface WidgetDefinition {
  type: WidgetType;
  label: string;
  icon: string;
  defaultWidth: number;
  defaultHeight: number;
}

export const WIDGET_DEFINITIONS: WidgetDefinition[] = [
  { type: 'button', label: 'Button', icon: '⬜', defaultWidth: 120, defaultHeight: 36 },
  { type: 'label', label: 'Label', icon: 'T', defaultWidth: 150, defaultHeight: 24 },
  { type: 'text-field', label: 'Text Field', icon: '▭', defaultWidth: 200, defaultHeight: 32 },
  { type: 'slider', label: 'Slider', icon: '─○─', defaultWidth: 200, defaultHeight: 30 },
  { type: 'checkbox', label: 'Checkbox', icon: '☑', defaultWidth: 150, defaultHeight: 24 },
  { type: 'plot', label: 'Plot', icon: '📊', defaultWidth: 400, defaultHeight: 300 },
  { type: 'panel', label: 'Panel', icon: '▢', defaultWidth: 300, defaultHeight: 200 },
];
