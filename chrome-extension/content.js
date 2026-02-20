// Auto-injects on every page - ready for future enhancements
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.action === "getPageText") {
    sendResponse(document.body.innerText.substring(0, 10000));
  }
});