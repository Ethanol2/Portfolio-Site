document.querySelectorAll('a[href]').forEach(link => {
  if (link.hostname !== window.location.hostname) {
    link.target = '_blank';
    link.rel = 'noopener noreferrer';
  }
});