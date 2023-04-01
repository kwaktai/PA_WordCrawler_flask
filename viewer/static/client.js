document.getElementById('input_form').addEventListener('submit', async event => {
  event.preventDefault();

  const text = document.getElementById('text').value;

  try {
    const response = await fetch('/process_text', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({ text }),
    });

    if (response.ok) {
      const data = await response.json();
      document.getElementById('results').textContent = JSON.stringify(data, null, 2);
    } else {
      console.error('Failed to process text');
    }
  } catch (err) {
    console.error(err);
  }
});
