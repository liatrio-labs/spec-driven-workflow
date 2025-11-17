# SDD Playbook Site

This directory contains code for the Spec-Driven Development (SDD) Playbook website on GitHub Pages.

## Structure

```text
docs/
├── index.html          # Main playbook page
├── assets/
│   ├── css/
│   │   └── styles.css  # Main stylesheet
│   ├── js/             # JavaScript files
│   ├── images/
│   └── fonts/         # Embedded font files (generated)
└── README.md           # This file
```

## Usage

### Local Development

Open `index.html` in a web browser to view the site locally.

### Embedding Fonts

To embed fonts locally (removing dependency on Google Fonts CDN):

```bash
# Run the font embedding script
python3 embed-fonts.py
```

This script will:

- Download DM Sans font files from Google Fonts
- Save them to `assets/fonts/`
- Update all HTML files to use embedded fonts instead of CDN links

**Note**: Font files are gitignored by default. Run the script before deploying to GitHub Pages, or add it to your CI/CD pipeline.

### GitHub Pages Deployment

For GitHub Pages deployment, this directory can be configured as the source for the site. See `GITHUB_PAGES_COMPATIBILITY.md` for details.

The GitHub Actions workflow (`.github/workflows/pages.yml`) can be configured to run `embed-fonts.py` automatically before deployment.

## Customization

The site uses CSS custom properties (variables) defined in `assets/css/styles.css` for easy theming:

- `--bg-light`: Main background color
- `--bg-section`: Section background color
- `--text-primary`: Primary text color
- `--text-secondary`: Secondary text color
- `--accent-green`: Green accent color (#89df00)
- `--border-color`: Border color
- `--box-bg`: Box/card background color

## Reference

Original site: https://spec-driven-development-2qtxmt3.gamma.site/playbook
