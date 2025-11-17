# SDD Playbook Site

This directory contains a local recreation of the Spec-Driven Development (SDD) Playbook website originally built with Gamma.app.

## Structure

```text
playbook-site/
├── index.html          # Main playbook page
├── assets/
│   ├── css/
│   │   └── styles.css  # Main stylesheet
│   ├── js/             # JavaScript files (if needed)
│   └── images/
│       └── logo-liatrio.svg  # Liatrio logo
└── README.md           # This file
```

## Usage

Open `index.html` in a web browser to view the site locally.

For GitHub Pages deployment, this directory can be configured as the source for the site.

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
