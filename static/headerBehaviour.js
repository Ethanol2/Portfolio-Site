let lastScroll = 0;
const header = document.querySelector('.site-header');
const headerShow = 'header-show';
const headerHidden = 'header-hidden';
const scrollThreshold = 5;

const hamburger = document.querySelector('.hamburger');
const menu = document.querySelector('.hamburger-menu');

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;

    if (Math.abs(currentScroll - lastScroll) < scrollThreshold)
        return;
    
    if (currentScroll > lastScroll && currentScroll > header.offsetHeight)
    {
        header.classList.add(headerHidden);
        menu.classList.remove('open');
        hamburger.classList.remove('active');
    }
    else if (header.classList.contains(headerHidden))
    {
        header.classList.remove(headerHidden);
        
        header.classList.remove(headerShow);
        void header.offsetWidth;
        header.classList.add(headerShow);
    }

    lastScroll = currentScroll;
});

hamburger.addEventListener('click', () => {
  menu.classList.toggle('open');
  hamburger.classList.toggle('active');
});