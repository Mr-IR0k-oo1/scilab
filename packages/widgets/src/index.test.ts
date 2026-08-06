import { test, expect } from "bun:test";
import { WIDGET_DEFINITIONS } from "./index";

test("@scilab-studio/widgets definitions count", () => {
  expect(WIDGET_DEFINITIONS.length).toBe(10);
});

test("contains all required v0.1 widget types", () => {
  const types = WIDGET_DEFINITIONS.map((w) => w.type);
  expect(types).toContain("button");
  expect(types).toContain("label");
  expect(types).toContain("text-field");
  expect(types).toContain("slider");
  expect(types).toContain("checkbox");
  expect(types).toContain("dropdown");
  expect(types).toContain("panel");
  expect(types).toContain("image");
  expect(types).toContain("table");
  expect(types).toContain("plot");
});
