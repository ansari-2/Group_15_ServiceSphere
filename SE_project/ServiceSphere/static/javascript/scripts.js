document.addEventListener('DOMContentLoaded', function() {
    const faqHeaders = document.querySelectorAll('.faq-item h3');
    faqHeaders.forEach(header => {
        header.addEventListener('click', () => {
            const p = header.nextElementSibling;
            p.style.display = p.style.display === 'block' ? 'none' : 'block';
        });
    });
});
