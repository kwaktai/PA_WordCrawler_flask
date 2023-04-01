const form = document.querySelector('form');
const translateBtn = document.getElementById('translate-btn');
const resultContainer = document.getElementById('result-container');
const result = document.getElementById('result');
form.addEventListener('submit', event => {
  event.preventDefault();
  const text = document.getElementById('text-input').value;
  if (text.trim() === '') {
    alert('Please enter some text.');
    return;
  }
  fetch('/translate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      text: text,
    }),
  })
    .then(response => response.json())
    .then(data => {
      result.innerText = data.translated_text;
      resultContainer.style.display = 'block';
    })
    .catch(error => {
      console.error('Error:', error);
      alert('An error occurred. Please try again later.');
    });
});
