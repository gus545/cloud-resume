// The counter API lives in the cloud-resume-backend repo. Its URL is set at
// build time (COUNTER_API_URL) and written to config.js by scripts/build.sh.
const API_URL = window.COUNTER_API_URL;

async function updateVisitorCount() {
  const counter = document.querySelector('.visit-counter');
  if (!API_URL) {
    if (counter) counter.hidden = true;
    return;
  }

  try {
    const response = await fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ path: window.location.pathname }),
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    document.getElementById('visit-count').textContent = data.visit_count;
  } catch (error) {
    console.error('Failed to fetch visitor count:', error);
  }
}

updateVisitorCount();
