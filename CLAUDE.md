# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a personal blog site built with Jekyll and hosted on GitHub Pages. The site features:
- Jekyll static site generator using the Lanyon theme (based on Poole)
- Interactive p5.js sketches and visualizations
- Blog posts in Markdown format
- Custom CSS and JavaScript enhancements
- Animated canvas backgrounds and interactive elements

## Development Commands

### Local Development
- `bundle exec jekyll serve` - Start local development server with live reload
- `bundle exec jekyll build` - Build the site for production
- `bundle install` - Install Ruby dependencies

### Dependencies
- Ruby gems managed via Bundler (see Gemfile)
- Uses `github-pages` gem for GitHub Pages compatibility
- `jekyll-paginate` for pagination support

## Site Architecture

### Directory Structure
- `_posts/` - Blog posts in Markdown format with YAML front matter
- `_drafts/` - Draft posts not yet published
- `_layouts/` - Jekyll template layouts (default, post, page)
- `_includes/` - Reusable template components
- `_site/` - Generated static site (ignored in git)
- `images/` - Blog post images and media assets
- `samples/` - Interactive p5.js sketches and demos
- `public/` - Static assets (CSS, JS, icons)

### Key Files
- `_config.yml` - Jekyll configuration and site metadata
- `index.html` - Home page template
- `about.md` - About page content
- `samples/sketch.html` - Interactive p5.js animation showcase

### Custom Components
- `_includes/p5_sketch.html` - Embeds p5.js sketches in blog posts via iframe
- `_includes/site_background.html` - Animated canvas background
- Interactive text animations with sound effects using Tone.js and p5.js

### Content Management
- Blog posts use standard Jekyll naming convention: `YYYY-MM-DD-title.md`
- Images stored in `images/` with subdirectories by post topic
- Interactive demos in `samples/` directory as standalone HTML files

### Styling and Assets
- Custom CSS in `public/css/main.css` and `syntax.css` 
- JavaScript functionality in `public/js/script.js`
- Responsive design with mobile-friendly touch interactions

## Design Philosophy

This site follows Swiss-Minimalism principles with code-centric typography:

### Core Principles
- **Monospaced Typography**: Uses high-quality monospaced fonts (JetBrains Mono) for all text
- **Mathematical Precision**: Strict line lengths (max-width: 65ch) and rhythmic vertical spacing  
- **Functional Aesthetics**: ASCII characters for dividers, celebrating terminal aesthetics
- **Elimination of Superfluous Elements**: Every element must justify its existence
- **Jekyll Purity**: Leverage Jekyll's native features, avoid unnecessary client-side JavaScript

### Development Guidelines
- Write clean, semantic HTML with minimal, purposeful CSS
- Hand-crafted CSS only - avoid frameworks
- Prioritize readability, performance, and typographic correctness
- Use programming ligatures and font-feature-settings for enhanced monospace rendering
- Maintain consistent 65ch content width for optimal readability

## Site Configuration
- Base URL: https://www.aaiiintt.xyz
- Timezone: Europe/London
- Author: Iain Tait (@aaiiintt)
- Theme based on Lanyon/Poole with custom modifications