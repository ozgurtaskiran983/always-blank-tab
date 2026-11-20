// Keeps an empty New Tab at the far right of every browser window.
const NEWTAB_URLS = new Set([
  "", "about:blank",
  "chrome://newtab/", "brave://newtab/",
  "chrome://new-tab-page/", "brave://new-tab-page/"
]);

function isEmptyNewTab(tab) {
  // While a tab is loading, its address appears in pendingUrl first
  const url = tab.pendingUrl || tab.url || "";
  return NEWTAB_URLS.has(url);
}

const timers = new Map();

// Debounce: many tab events can fire at once; run the check only once
function schedule(windowId, delay = 150) {
  if (windowId == null || windowId < 0) return;
  clearTimeout(timers.get(windowId));
  timers.set(windowId, setTimeout(() => ensure(windowId), delay));
}

async function ensure(windowId) {
  timers.delete(windowId);
  let win;
  try {
    win = await chrome.windows.get(windowId, { populate: true });
  } catch { return; } // window was closed
  if (win.type !== "normal" || !win.tabs.length) return;

  const tabs = win.tabs.sort((a, b) => a.index - b.index);
  const last = tabs[tabs.length - 1];
  if (isEmptyNewTab(last)) return; // already has a blank tab on the right

  try {
    // Reuse an inactive blank tab elsewhere by moving it to the end
    const spare = tabs.find(t => isEmptyNewTab(t) && !t.active && !t.pinned);
    if (spare) {
      await chrome.tabs.move(spare.id, { windowId, index: -1 });
    } else {
      await chrome.tabs.create({ windowId, active: false, index: tabs.length });
    }
  } catch (e) {
    // Tabs can't be edited while the user is dragging one; retry shortly
    schedule(windowId, 500);
  }
}

chrome.tabs.onCreated.addListener(t => schedule(t.windowId));
chrome.tabs.onUpdated.addListener((id, info, t) => {
  if (info.url !== undefined || info.status === "loading") schedule(t.windowId);
});
chrome.tabs.onRemoved.addListener((id, info) => {
  if (!info.isWindowClosing) schedule(info.windowId);
});
chrome.tabs.onMoved.addListener((id, info) => schedule(info.windowId));
chrome.tabs.onAttached.addListener((id, info) => schedule(info.newWindowId));
chrome.tabs.onDetached.addListener((id, info) => schedule(info.oldWindowId));
chrome.windows.onCreated.addListener(w => schedule(w.id));

async function ensureAll() {
  const wins = await chrome.windows.getAll({ windowTypes: ["normal"] });
  wins.forEach(w => schedule(w.id));
}
chrome.runtime.onStartup.addListener(ensureAll);
chrome.runtime.onInstalled.addListener(ensureAll);
