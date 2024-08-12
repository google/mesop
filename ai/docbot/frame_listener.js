// Listen for 'focus' message from the parent window
window.addEventListener('message', function (event) {
  if (event.data === 'focus') {
    // Find the textarea element
    const textarea = document.querySelector('textarea');
    console.log('focusing on textarea', textarea);
    // If the textarea is found, focus on it
    if (textarea) {
      textarea.focus();
    } else {
      console.warn('Textarea not found for focus');
    }
  }
});

window.addEventListener('keydown', function (event) {
  if (event.key === 'Escape') {
    if (document.activeElement) {
      document.activeElement.blur();
    }
    // Send a message to the parent window to close this iframe
    window.parent.postMessage('closeDocbot', '*');
  }
});
