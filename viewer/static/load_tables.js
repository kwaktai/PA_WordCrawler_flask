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
