const API_URL = 'https://p8rsbd7mrh.execute-api.us-east-2.amazonaws.com/Prod/counter';

async function updateVisitorCount() {
  try {
    const path = window.location.pathname;
    const response = await fetch(API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ path }),
    });
    const data = await response.json();
    document.getElementById('visit-count').textContent = data.visit_count;
  } catch (error) {
    console.error('Failed to fetch visitor count:', error);
  }
}

// Call on page load
updateVisitorCount();
