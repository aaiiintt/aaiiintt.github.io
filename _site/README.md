# AAIIINTT

The personal blog of Iain Tait ([@aaiiintt](https://twitter.com/aaiiintt)) - a collection of thoughts, experiments, and works in progress exploring technology, creativity, and culture.

**Live site:** https://www.aaiiintt.xyz

"aaiiintt" (Iain Tait's name sorted alphabetically) is a space for "thinkering" - thinking while tinkering with new ideas and technologies. Content ranges from AI and design deep dives to personal reflections and creative experiments.

## Quick Start

**Prerequisites:** Ruby and Bundler

```bash
git clone https://github.com/aaiiintt/aaiiintt.github.io.git
cd aaiiintt.github.io
bundle install
bundle exec jekyll serve
```

The site will be available at `http://127.0.0.1:4000/`.

## 🧙 Jekyll Post Wizard

This repository includes an AI-powered command-line tool that generates Jekyll blog posts in your unique writing style using Claude AI.

### Features
- **Style-Aware Generation** - Learns and replicates your personal writing voice
- **Jekyll-Ready Output** - Automatic front matter, proper formatting, and file naming
- **Smart Title Generation** - Multiple SEO-friendly title options
- **Interactive CLI** - Rich terminal interface with live previews

### Prerequisites
- **Python 3.6+** - [Download from python.org](https://python.org)
- **Anthropic API Key** - [Get yours from console.anthropic.com](https://console.anthropic.com/)

### Quick Setup

1. **Run automated setup:**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

2. **Configure API key:**
   - Edit the generated `.env` file
   - Replace `your_api_key_here` with your Anthropic API key

3. **Customize writing style:**
   - Edit `style.txt` with your writing preferences and examples
   - The more detailed, the better your results

4. **Generate your first post:**
   ```bash
   ./generate.py "The future of web development"
   ```

### Usage Examples
```bash
# Basic post generation
./generate.py "Your blog post topic"

# Advanced options
./generate.py "CSS Grid tips" --length long --category design
./generate.py "JavaScript trends" --draft
./generate.py "AI ethics" --dry-run
```

### Configuration Files
- **`.env`** - API configuration (copy from `.env.template`)
- **`style.txt`** - Your writing voice and style examples (most important!)
- **`.style_cache.json`** - Automatically generated cache (don't edit directly)

## Project Structure

```
├── _config.yml              # Jekyll configuration
├── _layouts/                # Template layouts
├── _includes/               # Reusable components (p5.js sketches, backgrounds)
├── _posts/                  # Blog posts
├── public/                  # Static assets (CSS, JS, favicons)
├── samples/                 # Interactive p5.js sketches and demos
├── images/                  # Blog post media assets
├── generate.py              # AI post generator
├── content_generator.py     # Claude AI integration
├── jekyll_formatter.py      # Jekyll-specific formatting
└── style.txt               # Writing style guide
```

## Features & Design Philosophy

Built with Swiss-Minimalism principles:
- **Monospaced Typography** - JetBrains Mono font throughout
- **Mathematical Precision** - Strict 65ch line lengths and rhythmic spacing
- **Interactive Elements** - p5.js sketches, animated canvas backgrounds, Tone.js integration
- **Jekyll Purity** - Leverages native Jekyll features, minimal client-side JavaScript

## Development

- **Local development:** `bundle exec jekyll serve`
- **Build:** `bundle exec jekyll build` 
- **Dependencies:** `bundle install`
- **Theme:** Custom Lanyon/Poole-based theme with Swiss-Minimalism modifications

### Troubleshooting

**Writing style seems outdated or wrong?**
```bash
# Clear the style cache to force refresh
rm .style_cache.json
```
The Post Wizard caches your `style.txt` for performance. If you update your writing style, delete the cache file to pick up changes.

**Post Wizard not working?**
- Check your `.env` file has a valid `ANTHROPIC_API_KEY`
- Ensure `style.txt` exists (copy from `style_template.txt` if needed)
- Activate your virtual environment: `source venv/bin/activate`

## License

Content licensed under [Creative Commons Zero v1.0 Universal](LICENSE.md)
