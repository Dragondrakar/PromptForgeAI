const API_URL = "http://localhost:8000";
const TOKEN = "super-secret-dev-key-change-in-production";   // ← same as backend

function showTab(n) {
  document.getElementById("prompt-tab").style.display = n === 0 ? "block" : "none";
  document.getElementById("data-tab").style.display = n === 1 ? "block" : "none";
}

async function optimizePrompt() {
  const input = document.getElementById("prompt-input").value;
  const res = await fetch(`${API_URL}/optimize`, {
    method: "POST",
    headers: { "Content-Type": "application/json", "Authorization": `Bearer ${TOKEN}` },
    body: JSON.stringify({ input })
  });
  const data = await res.json();
  document.getElementById("result").textContent = data.optimized;
}

async function scrapeData() {
  let url = document.getElementById("url-input").value;
  if (!url) {
    chrome.tabs.query({active: true, currentWindow: true}, tabs => {
      url = tabs[0].url;
      document.getElementById("url-input").value = url;
      doScrape(url);
    });
  } else {
    doScrape(url);
  }
}

async function doScrape(url) {
  const query = document.getElementById("query-input").value || "extract all key information";
  const res = await fetch(`${API_URL}/scrape`, {
    method: "POST",
    headers: { "Content-Type": "application/json", "Authorization": `Bearer ${TOKEN}` },
    body: JSON.stringify({ url, query })
  });
  const data = await res.json();
  document.getElementById("data-result").textContent = JSON.stringify(data.data, null, 2);
}