document.addEventListener('DOMContentLoaded', () => {
  // Upload documents
  const uploadForm = document.getElementById('upload-form');
  const uploadStatus = document.getElementById('upload-status');
  uploadForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const files = document.getElementById('docs').files;
    if (!files.length) return;
    const formData = new FormData();
    for (const file of files) formData.append('files', file);
    uploadStatus.textContent = 'Uploading...';
    try {
      const res = await fetch('/ingest/', { method: 'POST', body: formData });
      const data = await res.json();
      uploadStatus.textContent = data.status === 'Documents ingested' ? 'Uploaded!' : 'Error: ' + (data.status || 'Unknown error');
    } catch (err) {
      uploadStatus.textContent = 'Upload failed.';
    }
  });

  // Query
  const queryForm = document.getElementById('query-form');
  const responseBox = document.getElementById('response-box');
  const responseText = document.getElementById('response');
  const citationsList = document.getElementById('citations');
  queryForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const query = document.getElementById('query').value;
    const role = document.getElementById('role').value;
    const formData = new FormData();
    formData.append('query', query);
    if (role) formData.append('role', role);
    responseText.textContent = 'Loading...';
    citationsList.innerHTML = '';
    responseBox.classList.remove('hidden');
    try {
      const res = await fetch('/query/', { method: 'POST', body: formData });
      const data = await res.json();
      responseText.textContent = data.response || 'No answer.';
      citationsList.innerHTML = (data.citations || []).map(c => `<li>${c}</li>`).join('');
    } catch (err) {
      responseText.textContent = 'Error fetching response.';
    }
  });

  // Feedback
  const feedbackForm = document.getElementById('feedback-form');
  const feedbackStatus = document.getElementById('feedback-status');
  let lastQuery = '';
  let lastResponse = '';
  queryForm.addEventListener('submit', (e) => {
    lastQuery = document.getElementById('query').value;
    lastResponse = responseText.textContent;
  });
  document.getElementById('helpful-yes').onclick = async () => {
    await sendFeedback(true);
  };
  document.getElementById('helpful-no').onclick = async () => {
    await sendFeedback(false);
  };
  async function sendFeedback(helpful) {
    if (!lastQuery || !lastResponse) return;
    const role = document.getElementById('role').value;
    const formData = new FormData();
    formData.append('query', lastQuery);
    formData.append('response', lastResponse);
    formData.append('helpful', helpful);
    if (role) formData.append('role', role);
    feedbackStatus.textContent = 'Sending...';
    try {
      const res = await fetch('/feedback/', { method: 'POST', body: formData });
      const data = await res.json();
      feedbackStatus.textContent = data.status === 'success' ? 'Thank you for your feedback!' : 'Error: ' + (data.message || 'Unknown error');
    } catch (err) {
      feedbackStatus.textContent = 'Feedback failed.';
    }
  }
}); 