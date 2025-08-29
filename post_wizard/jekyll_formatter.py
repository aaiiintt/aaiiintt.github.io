"""
Jekyll formatter for Post Wizard
Converts generated content into Jekyll-ready format with proper front matter
"""
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import yaml


class JekyllFormatter:
    def __init__(self, jekyll_root: str = ".."):
        """Initialize with Jekyll site root directory"""
        self.jekyll_root = Path(jekyll_root)
        self.posts_dir = self.jekyll_root / "_posts"
        self.images_dir = self.jekyll_root / "images"
    
    def create_front_matter(self, content_data: Dict[str, Any], 
                          title: Optional[str] = None,
                          category: str = "technology") -> str:
        """Generate YAML front matter for Jekyll post"""
        
        # Use custom title or generate from topic
        post_title = title or content_data["topic"]
        
        # Generate date string
        date_str = datetime.now().strftime("%Y-%m-%d")
        
        front_matter = {
            "layout": "post",
            "title": post_title,
            "date": date_str,
            "category": category
        }
        
        # Convert to YAML
        yaml_content = yaml.dump(front_matter, default_flow_style=False, allow_unicode=True)
        
        return f"---\n{yaml_content}---\n\n"
    
    def process_image_placeholders(self, content: str, slug: str) -> str:
        """Convert [IMAGE: description] placeholders to Jekyll image includes"""
        
        def replace_image(match):
            description = match.group(1).strip()
            # Generate a filename from description
            filename = re.sub(r'[^\w\s-]', '', description.lower())
            filename = re.sub(r'[-\s]+', '-', filename) + '.webp'
            
            return f'{{% include image.html src="/images/{slug}/{filename}" alt="{description}" %}}'
        
        # Replace [IMAGE: ...] with Jekyll includes
        content = re.sub(r'\[IMAGE:\s*([^\]]+)\]', replace_image, content)
        
        return content
    
    def create_post_file(self, content_data: Dict[str, Any], 
                        title: Optional[str] = None,
                        category: str = "technology") -> Dict[str, str]:
        """Create complete Jekyll post file"""
        
        slug = content_data["slug"]
        date_str = datetime.now().strftime("%Y-%m-%d")
        filename = f"{date_str}-{slug}.md"
        
        # Create front matter
        front_matter = self.create_front_matter(content_data, title, category)
        
        # Process content
        content = content_data["content"]
        content = self.process_image_placeholders(content, f"{date_str}-{slug}")
        
        # Combine front matter and content
        full_content = front_matter + content
        
        return {
            "filename": filename,
            "content": full_content,
            "path": str(self.posts_dir / filename),
            "image_dir": f"{date_str}-{slug}"
        }
    
    def save_post(self, post_data: Dict[str, str]) -> bool:
        """Save post to Jekyll _posts directory"""
        try:
            # Ensure posts directory exists
            self.posts_dir.mkdir(exist_ok=True)
            
            # Write post file
            with open(post_data["path"], 'w', encoding='utf-8') as f:
                f.write(post_data["content"])
            
            # Create image directory
            image_dir = self.images_dir / post_data["image_dir"]
            image_dir.mkdir(exist_ok=True)
            
            return True
            
        except Exception as e:
            print(f"Error saving post: {e}")
            return False
    
    def get_existing_posts(self) -> list:
        """Get list of existing post files"""
        if not self.posts_dir.exists():
            return []
        
        return [f.name for f in self.posts_dir.glob("*.md")]
    
    def validate_front_matter(self, content: str) -> bool:
        """Validate YAML front matter in content"""
        if not content.startswith("---\n"):
            return False
        
        try:
            # Extract front matter
            parts = content.split("---\n", 2)
            if len(parts) < 3:
                return False
            
            yaml.safe_load(parts[1])
            return True
            
        except yaml.YAMLError:
            return False
    
    def extract_images_needed(self, content: str) -> list:
        """Extract list of images that need to be created from content"""
        images = []
        
        # Find Jekyll image includes
        includes = re.findall(r'{% include image\.html src="([^"]+)"[^%]*alt="([^"]*)"', content)
        
        for src, alt in includes:
            # Extract filename from path
            filename = src.split('/')[-1]
            images.append({
                "filename": filename,
                "alt": alt,
                "full_path": src
            })
        
        return images


if __name__ == "__main__":
    # Test the formatter
    formatter = JekyllFormatter()
    
    # Mock content data
    test_content = {
        "content": "# Test Post\n\nThis is a test with an image:\n\n[IMAGE: CSS Grid example layout]\n\nMore content here.",
        "topic": "CSS Grid Best Practices", 
        "slug": "css-grid-best-practices",
        "word_count": 100
    }
    
    post_data = formatter.create_post_file(test_content, category="design")
    
    print("Generated post:")
    print(f"Filename: {post_data['filename']}")
    print(f"Image dir: {post_data['image_dir']}")
    print("\nContent preview:")
    print(post_data["content"][:500] + "...")
    
    # Check what images are needed
    images = formatter.extract_images_needed(post_data["content"])
    print(f"\nImages needed: {len(images)}")
    for img in images:
        print(f"- {img['filename']}: {img['alt']}")