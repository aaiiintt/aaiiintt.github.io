#!/usr/bin/env python3
"""
Jekyll Post Wizard - Main CLI
Generate blog posts using Claude and your writing style
"""
import os
import sys
import argparse
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich import print as rprint
from dotenv import load_dotenv

# Import our modules
from content_generator import ContentGenerator
from jekyll_formatter import JekyllFormatter


def main():
    # Load environment variables
    load_dotenv()
    
    console = Console()
    
    # Parse arguments
    parser = argparse.ArgumentParser(description="Generate Jekyll blog posts with Claude")
    parser.add_argument("topic", help="Blog post topic")
    parser.add_argument("--length", choices=["short", "medium", "long"], 
                       default="medium", help="Post length (default: medium)")
    parser.add_argument("--category", default="technology", 
                       help="Post category (default: technology)")
    parser.add_argument("--title", help="Custom post title (optional)")
    parser.add_argument("--draft", action="store_true", 
                       help="Save to _drafts instead of _posts")
    parser.add_argument("--dry-run", action="store_true", 
                       help="Generate but don't save")
    
    args = parser.parse_args()
    
    console.print(f"🧙 [bold blue]Jekyll Post Wizard[/bold blue]", style="bold")
    console.print(f"Generating {args.length} post about: [green]{args.topic}[/green]")
    
    try:
        # Check for style.txt
        if not Path("style.txt").exists():
            console.print("[red]❌ No style.txt found![/red]")
            console.print("Copy style_template.txt to style.txt and customize it first.")
            sys.exit(1)
        
        # Check for API key
        if not os.getenv('ANTHROPIC_API_KEY'):
            console.print("[red]❌ ANTHROPIC_API_KEY environment variable not set![/red]")
            console.print("Set your Anthropic API key in environment or .env file")
            sys.exit(1)
        
        # Generate content
        console.print("\n🤖 Generating content with Claude...")
        generator = ContentGenerator()
        content_data = generator.generate_content(args.topic, args.length)
        
        console.print(f"✅ Generated {content_data['word_count']} words")
        
        # Generate title variations if no custom title
        title = args.title
        if not title:
            console.print("🎯 Generating title options...")
            titles = generator.generate_title_variations(args.topic)
            
            if titles:
                console.print("\nTitle options:")
                for i, (key, option) in enumerate(titles.items(), 1):
                    console.print(f"  {i}. {option}")
                
                try:
                    choice = Prompt.ask("\nSelect title", choices=[str(i) for i in range(1, len(titles)+1)], default="1")
                except (KeyboardInterrupt, EOFError):
                    choice = "1"  # Default to first option in non-interactive mode
                title = list(titles.values())[int(choice)-1]
            else:
                title = args.topic
        
        console.print(f"📝 Using title: [green]{title}[/green]")
        
        # Format for Jekyll
        console.print("📄 Formatting for Jekyll...")
        formatter = JekyllFormatter()
        post_data = formatter.create_post_file(content_data, title, args.category)
        
        # Show preview
        console.print(f"\n📁 Post will be saved as: [blue]{post_data['filename']}[/blue]")
        console.print(f"🖼️  Image directory: [blue]images/{post_data['image_dir']}[/blue]")
        
        # Extract and show images needed
        images = formatter.extract_images_needed(post_data["content"])
        if images:
            console.print(f"\n🖼️  Images needed ({len(images)}):")
            for img in images:
                console.print(f"   • {img['filename']}: {img['alt']}")
        
        # Preview content
        try:
            show_preview = Confirm.ask("\nShow content preview?", default=False)
        except (KeyboardInterrupt, EOFError):
            show_preview = args.dry_run  # Show preview in dry-run mode by default
            
        if show_preview:
            console.print("\n" + "="*60)
            console.print(post_data["content"][:1000] + ("..." if len(post_data["content"]) > 1000 else ""))
            console.print("="*60)
        
        # Save or dry-run
        if args.dry_run:
            console.print("\n🏃 [yellow]Dry run - not saving files[/yellow]")
        else:
            try:
                save_post = Confirm.ask("\nSave post?", default=True)
            except (KeyboardInterrupt, EOFError):
                save_post = True  # Default to saving in non-interactive mode
                
            if save_post:
                # Modify path if draft
                if args.draft:
                    post_data["path"] = post_data["path"].replace("_posts", "_drafts")
                    console.print("📝 Saving as draft...")
                
                success = formatter.save_post(post_data)
                
                if success:
                    console.print(f"✅ [green]Post saved successfully![/green]")
                    console.print(f"📁 File: {post_data['path']}")
                    if images:
                        console.print(f"🖼️  Add images to: images/{post_data['image_dir']}/")
                else:
                    console.print("❌ [red]Failed to save post[/red]")
                    sys.exit(1)
    
    except KeyboardInterrupt:
        console.print("\n\n👋 Cancelled by user")
        sys.exit(0)
    except Exception as e:
        console.print(f"❌ [red]Error: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()