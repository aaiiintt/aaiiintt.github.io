# 🧙 Jekyll Post Wizard

The Jekyll Post Wizard is a powerful command-line tool that uses the magic of AI (specifically, Claude) to help you write Jekyll blog posts in your own unique style.

It analyzes your writing, understands your voice, and generates high-quality content that sounds just like you. It's the perfect assistant for when you have an idea but not the time to write, or when you just need a little help getting started.

## Features

-   **AI-Powered Content Generation:** Leverages the power of Claude to generate blog posts on any topic.
-   **Style Emulation:** Analyzes your `style.txt` file to learn and replicate your personal writing style.
-   **Automatic Jekyll Formatting:** Creates Jekyll-ready markdown files with proper front matter.
-   **Smart Title Suggestions:** Generates multiple title options for you to choose from.
-   **Image Placeholders:** Intelligently suggests where images could be placed in your post.
-   **Easy to Use:** Simple command-line interface for a smooth workflow.

## Prerequisites

-   Python 3.6+
-   An API key from [Anthropic](https://www.anthropic.com/)

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd post_wizard
    ```

2.  **Run the setup script:**
    ```bash
    ./setup.sh
    ```
    This will create a Python virtual environment, install the necessary dependencies, and create the configuration files for you.

## Configuration

Before you can start generating posts, you need to configure two files:

1.  **.env:** This file stores your Anthropic API key. Copy the `.env.template` file to `.env` and add your API key:
    ```bash
    cp .env.template .env
    ```
    Then, open `.env` and add your key:
    ```
    ANTHROPIC_API_KEY=your_api_key_here
    ```

2.  **style.txt:** This is the most important file for getting the AI to sound like you. It's your personal writing style guide. Open `style.txt` and fill it with examples of your writing, your common phrases, and your preferences for tone and structure. The more detailed you are, the better the results will be.

## Usage

Generating a new post is as simple as running the `generate.py` script with your desired topic.

### Basic Usage

```bash
./generate.py "A blog post about the future of AI"
```

### Advanced Options

You can customize the generation process with the following options:

-   `--length`: Choose the length of the post (`short`, `medium`, `long`).
-   `--category`: Specify the category for the post.
-   `--title`: Provide a custom title for the post.
-   `--draft`: Save the post to the `_drafts` directory instead of `_posts`.
-   `--dry-run`: Generate the post but don't save it to a file.

**Example:**

```bash
./generate.py "The importance of open-source software" --length long --category technology
```

## How It Works

The Jekyll Post Wizard works in a few simple steps:

1.  **Style Analysis:** It reads your `style.txt` file to understand your writing style.
2.  **Content Generation:** It sends a carefully crafted prompt to the Claude API, including your topic and style guide, to generate the blog post content.
3.  **Title Creation:** It generates multiple title options for you to choose from.
4.  **Jekyll Formatting:** It adds the necessary YAML front matter and formats the content for Jekyll.
5.  **File Creation:** It saves the final post to the `_posts` or `_drafts` directory and creates a corresponding image directory.

## Customization

This tool is designed to be customizable. You can modify the following files to suit your needs:

-   **`content_generator.py`:** This file contains the logic for interacting with the Claude API. You can change the model, the prompt, and the parameters to fine-tune the content generation process.
-   **`jekyll_formatter.py`:** This file handles the formatting of the post for Jekyll. You can change the front matter fields, the image placeholder format, and the file structure.
-   **`style_template.txt`:** This is the template for the `style.txt` file. You can add more sections or change the existing ones to create a more detailed style guide.

## Contributing

Contributions are welcome! If you have any ideas for how to improve this tool, please open an issue or submit a pull request.
