"""
Style caching system for Jekyll Post Wizard
Reads and caches style.txt for efficient content generation
"""
import json
import hashlib
import os
from pathlib import Path
from typing import Optional, Dict, Any


class StyleCache:
    def __init__(self, style_file: str = "style.txt", cache_file: str = ".style_cache.json"):
        self.style_file = Path(style_file)
        self.cache_file = Path(cache_file)
        self.cached_style: Optional[Dict[str, Any]] = None
        self.style_hash: Optional[str] = None
    
    def get_file_hash(self, file_path: Path) -> str:
        """Generate MD5 hash of file contents"""
        if not file_path.exists():
            return ""
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return hashlib.md5(content.encode('utf-8')).hexdigest()
    
    def load_cache(self) -> Optional[Dict[str, Any]]:
        """Load cached style data if it exists"""
        if not self.cache_file.exists():
            return None
        
        try:
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None
    
    def save_cache(self, style_data: Dict[str, Any], file_hash: str):
        """Save style data and hash to cache"""
        cache_data = {
            "hash": file_hash,
            "style": style_data
        }
        
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2)
        except IOError as e:
            print(f"Warning: Could not save cache: {e}")
    
    def parse_style_file(self) -> Dict[str, Any]:
        """Parse style.txt into structured data"""
        if not self.style_file.exists():
            raise FileNotFoundError(f"Style file not found: {self.style_file}")
        
        with open(self.style_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Simple parser for markdown-style sections
        sections = {}
        current_section = None
        current_content = []
        
        for line in content.split('\n'):
            line = line.strip()
            
            # Check for section headers (## Section Name)
            if line.startswith('## '):
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = line[3:].strip()
                current_content = []
            elif current_section and line:
                current_content.append(line)
        
        # Add the last section
        if current_section:
            sections[current_section] = '\n'.join(current_content).strip()
        
        return {
            "raw_content": content,
            "sections": sections
        }
    
    def get_style(self) -> Dict[str, Any]:
        """Get cached style or parse and cache style.txt"""
        current_hash = self.get_file_hash(self.style_file)
        
        # Check if we have a valid cache
        if self.cached_style and self.style_hash == current_hash:
            return self.cached_style
        
        # Try to load from cache file
        cached_data = self.load_cache()
        if cached_data and cached_data.get("hash") == current_hash:
            self.cached_style = cached_data["style"]
            self.style_hash = current_hash
            return self.cached_style
        
        # Parse style file and cache it
        print("Parsing style.txt...")
        style_data = self.parse_style_file()
        
        self.cached_style = style_data
        self.style_hash = current_hash
        self.save_cache(style_data, current_hash)
        
        return style_data
    
    def get_style_prompt(self) -> str:
        """Get formatted style guide for Claude prompts"""
        style_data = self.get_style()
        
        return f"""
WRITING STYLE GUIDE:
{style_data['raw_content']}

Use this style guide to write content that matches my voice, tone, and preferences exactly.
Pay special attention to the structure, technical depth, and common phrases I use.
"""


if __name__ == "__main__":
    # Test the style cache
    cache = StyleCache()
    try:
        style = cache.get_style()
        print("Style sections found:")
        for section in style.get("sections", {}):
            print(f"- {section}")
    except FileNotFoundError:
        print("No style.txt found. Copy style_template.txt to style.txt and customize it.")