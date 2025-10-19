const axios = require("axios");

// ====== CONFIG ======
const ITEM_ID = "SKU-123";
const POST_URL = "http://127.0.0.1:1880/sensor"; // Node-RED endpoint (we'll set up next)
const INTERVAL_MS = 5000; // send every 5 seconds
// ====================

function randomStock() {
  // Simulate stock values (0–40, sometimes low to trigger reorder)
  return Math.max(0, Math.floor(15 + (Math.random() * 30 - Math.random() * 30)));
}

async function tick() {
  const payload = {
    item_id: ITEM_ID,
    stock_level: randomStock(),
    ts: new Date().toISOString(),
  };

  try {
    const res = await axios.post(POST_URL, payload, { timeout: 3000 });
    console.log(`[POST ${res.status}]`, JSON.stringify(payload));
  } catch (err) {
    console.log(`[POST ERR] ${err.message}`, JSON.stringify(payload));
  }
}

console.log("Sensor simulator started.");
console.log(`Posting to: ${POST_URL} every ${INTERVAL_MS / 1000}s`);
setInterval(tick, INTERVAL_MS);
