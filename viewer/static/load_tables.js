window.addEventListener('load', async () => {
  try {
    const sentencesResponse = await fetch('/csv?file=sentences_data.csv');
    const wordsResponse = await fetch('/csv?file=words_data.csv');

    if (sentencesResponse.ok && wordsResponse.ok) {
      const sentencesHtml = await sentencesResponse.text();
      const wordsHtml = await wordsResponse.text();

      document.getElementById('sentences').innerHTML = sentencesHtml;
      document.getElementById('words').innerHTML = wordsHtml;
    } else {
      console.error('Failed to load CSV data');
    }
  } catch (err) {
    console.error(err);
  }
});

async function submitText() {
  const text = document.getElementById('input-text').value;
  const response = await fetch('/process_text', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: `text=${encodeURIComponent(text)}`,
  });

  if (response.ok) {
    const result = await response.json();
    console.log(result);
  } else {
    console.error('Failed to submit text');
  }
}

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
      console.log('Text processed successfully');
    } else {
      console.error('Failed to process text');
    }
  } catch (err) {
    console.error(err);
  }
});
