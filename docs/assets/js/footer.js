/**
 * Footer Component
 * Dynamically injects footer into pages
 */
(function() {
    'use strict';

    function createFooter() {
        const footer = document.querySelector('footer');
        if (!footer) return;

        const currentYear = new Date().getFullYear();

        const footerHTML = `
            <div class="container">
                <p>&copy; ${currentYear} Liatrio. All rights reserved.</p>
                <div class="footer-links">
                    <a href="https://liatrio.com/privacy-policy" target="_blank" rel="noopener noreferrer">Privacy Policy</a>
                </div>
            </div>
        `;

        footer.innerHTML = footerHTML;
    }

    // Run when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', createFooter);
    } else {
        createFooter();
    }
})();
