import { test, expect } from "bun:test";
import { getStore, setStore, openTab, closeTab, resetTabs, enterProject, leaveProject } from "./store";
import type { FOSSEEProject } from "@/ecosystem/types";

test("store initial state and updates", () => {
  const initial = getStore();
  expect(initial.sidebarOpen).toBe(true);

  setStore({ sidebarOpen: false });
  expect(getStore().sidebarOpen).toBe(false);

  setStore({ sidebarOpen: true });
});

test("store tabs management", () => {
  resetTabs();
  expect(getStore().tabs.length).toBe(0);

  openTab({ id: "t1", title: "Tab 1", module: "editor" });
  expect(getStore().tabs.length).toBe(1);
  expect(getStore().activeTab).toBe("t1");

  openTab({ id: "t2", title: "Tab 2", module: "gui" });
  expect(getStore().tabs.length).toBe(2);
  expect(getStore().activeTab).toBe("t2");

  closeTab("t1");
  expect(getStore().tabs.length).toBe(1);
  expect(getStore().tabs[0].id).toBe("t2");

  resetTabs();
});

test("store project lifecycle", () => {
  const dummyProj: FOSSEEProject = {
    id: "p1",
    name: "Test Project",
    tools: ["scilab"],
    path: "/tmp/p1",
    version: "0.1.0",
    created: "2026-08-06",
    modified: "2026-08-06",
  };
  enterProject(dummyProj);

  expect(getStore().inProject).toBe(true);
  expect(getStore().project?.name).toBe("Test Project");

  leaveProject();
  expect(getStore().inProject).toBe(false);
  expect(getStore().project).toBeNull();
});
