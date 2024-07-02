const urlParams = new URLSearchParams(window.location.search);
const demoParam = urlParams.get('demo') || '';

const iframe = document.createElement('iframe');
iframe.src = 'https://mesop-tdcukehw6q-uc.a.run.app/' + demoParam;
iframe.className = 'full-screen-iframe';
document.body.appendChild(iframe);
