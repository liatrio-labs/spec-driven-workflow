/**
 * Navigation Component
 * Dynamically injects navigation into pages
 */
(function () {
    'use strict';

    // Get current page filename, handling both root and subdirectory paths
    const pathParts = window.location.pathname.split('/');
    const currentPage = pathParts[pathParts.length - 1] || 'index.html';

    // Determine base path for navigation links
    const isReferencePage = pathParts.includes('references');
    const basePath = isReferencePage ? '../' : '';

    const navLinks = [
        { href: basePath + 'index.html', text: 'SDD Playbook' },
        { href: basePath + 'comparison.html', text: 'Comparison' },
        { href: basePath + 'developer-experience.html', text: 'Developer Experience' },
        { href: basePath + 'common-questions.html', text: 'Common Questions' },
        { href: basePath + 'video-overview.html', text: 'Video Overview' },
        { href: basePath + 'reference-materials.html', text: 'Reference Materials' }
    ];

    function createNavigation() {
        const header = document.querySelector('header');
        if (!header) return;

        const navHTML = `
            <nav>
                <div class="nav-container">
                    <div class="logo">
                        <a href="https://liatrio.com" target="_blank" rel="noopener noreferrer">
                            <img src="${basePath}assets/images/logo-liatrio.svg" alt="Liatrio" class="logo-img">
                        </a>
                    </div>
                    <ul class="nav-links">
                        ${navLinks.map(link => {
            // Extract filename from href for comparison
            const linkPage = link.href.split('/').pop();
            const isActive = linkPage === currentPage ? ' class="active"' : '';
            return `<li><a href="${link.href}"${isActive}>${link.text}</a></li>`;
        }).join('')}
                    </ul>
                </div>
            </nav>
        `;

        header.innerHTML = navHTML;
    }

    // Run when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', createNavigation);
    } else {
        createNavigation();
    }
})();
