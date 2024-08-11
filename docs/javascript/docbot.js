// Function to show the docbot iframe
function showDocbotIframe() {
  const iframe = document.getElementById('docbot-iframe');

  iframe.style.display = 'block';

  iframe.focus();

  // Add event listener to close iframe when clicking outside
  document.addEventListener('click', function closeIframe(e) {
    if (!iframe.contains(e.target)) {
      iframe.style.display = 'none';
      // Reload the iframe
      iframe.src = iframe.src;
      document.removeEventListener('click', closeIframe);
    }
  });
}

// Listen for click events on the search input
document.addEventListener(
  'click',
  function (event) {
    if (event.target.matches('.md-search__input')) {
      event.preventDefault(); // Prevent default search behavior
      event.stopPropagation();
      showDocbotIframe();
    }
  },
  true,
); // Added 'true' for event capture

document.addEventListener('keydown', function (event) {
  // Check if the Escape key is pressed
  if (event.key === 'Escape') {
    const iframe = document.getElementById('docbot-iframe');
    if (iframe.style.display === 'block') {
      iframe.style.display = 'none';
      // Reload the iframe
      iframe.src = iframe.src;
    }
    return;
  }
  // Check if Command (Mac) or Control (Windows) + K is pressed
  if ((event.metaKey || event.ctrlKey) && event.key === 'k') {
    event.preventDefault(); // Prevent default browser behavior
    const iframe = document.getElementById('docbot-iframe');
    if (iframe.style.display === 'block') {
      iframe.style.display = 'none';
      // Reload the iframe
      iframe.src = iframe.src;
      return;
    }
    showDocbotIframe();
  }
});

// Create the iframe
function createDocbotIframe() {
  const iframe = document.createElement('iframe');
  iframe.id = 'docbot-iframe';
  iframe.src = 'https://wwwillchen-mesop-docs-bot.hf.space/'; // Replace with the actual URL
  iframe.style.position = 'fixed';
  iframe.style.display = 'none';
  iframe.style.top = '50%';
  iframe.style.left = '50%';
  iframe.style.transform = 'translate(-50%, -50%)';
  iframe.style.width = '80%';
  iframe.style.maxWidth = '720px';
  iframe.style.height = '80%';
  iframe.style.border = 'none';
  iframe.style.borderRadius = '16px';
  iframe.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.1)';
  iframe.style.zIndex = '9999';

  // Append the iframe to the body
  document.body.appendChild(iframe);

  return iframe;
}

createDocbotIframe();
