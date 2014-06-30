// When the extension is first installed, set default settings
chrome.runtime.onInstalled.addListener(function(details) {
    localStorage["capsule_toolkit_enabled"] = true;
});

// Listen for changes whenever the URL of any tab is changed
chrome.tabs.onUpdated.addListener(function(id, info, tab) {
    // We don't want to load if tabs haven't finished loading, and only if we're at the right URL
    if (tab.status !== "complete") { return; }
    if (tab.url.toLowerCase().indexOf("rethinkdb.capsulecrm.com") === -1) { return; }

    if (localStorage["capsule_toolkit_enabled"] == "true") {
        // Show the page action in this tab
        chrome.pageAction.show(tab.id);
        // Inject the content script we're loading in the background for Capsule
        chrome.tabs.executeScript(null, { "file": "js/jquery-2.1.1.min.js"});
        chrome.tabs.executeScript(null, { "file": "js/app.js" });
    }
});

// When the icon is clicked, show a settings popup
chrome.pageAction.onClicked.addListener(function(tab) {
    chrome.pageAction.show(tab.id);
});
