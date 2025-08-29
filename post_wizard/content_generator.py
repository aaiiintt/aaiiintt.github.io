"""
Content generator using Claude API
Generates blog post content based on topic and cached writing style
"""
import os
from typing import Dict, Any, Optional
from datetime import datetime
import anthropic
from style_cache import StyleCache


class ContentGenerator:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize Claude client"""
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is required")
        
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.style_cache = StyleCache()
    
    def generate_content(self, topic: str, length: str = "medium") -> Dict[str, Any]:
        """Generate blog post content for given topic"""
        
        # Get style guide
        style_prompt = self.style_cache.get_style_prompt()
        
        # Create length guidance
        length_guide = {
            "short": "500-800 words, focused on a single concept",
            "medium": "1000-1500 words, thorough exploration with examples", 
            "long": "2000+ words, comprehensive deep-dive with multiple examples"
        }
        
        target_length = length_guide.get(length, length_guide["medium"])
        
        # Generate slug from topic
        from slugify import slugify
        short_topic = ' '.join(topic.split()[:4])
        slug = slugify(short_topic)
        
        # Create the prompt
        prompt = f"""
{style_prompt}

TASK: Write a blog post about "{topic}"

REQUIREMENTS:
- Length: {target_length}
- Follow the writing style guide exactly
- Use markdown formatting
- Include practical examples where relevant
- Add image placeholders where they would enhance the content (use format: [IMAGE: Description of image needed])
- Structure the content with appropriate headings
- End with actionable takeaways

IMPORTANT: Write ONLY the blog post content. Do not include YAML front matter or Jekyll-specific formatting - just the markdown content that will go inside the post.

Begin writing:
"""

        try:
            # Call Claude API
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=4000,
                temperature=0.7,
                messages=[{
                    "role": "user", 
                    "content": prompt
                }]
            )
            
            content = response.content[0].text
            
            return {
                "content": content,
                "topic": topic,
                "slug": slug,
                "length": length,
                "generated_at": datetime.now().isoformat(),
                "word_count": len(content.split())
            }
            
        except Exception as e:
            raise RuntimeError(f"Failed to generate content: {e}")
    
    def generate_title_variations(self, topic: str) -> Dict[str, str]:
        """Generate SEO-friendly title variations"""
        
        prompt = f"""
Based on the topic "{topic}", generate 3 title variations:
1. A direct, descriptive title
2. A more engaging, question-based title  
3. A practical, actionable title

Format as:
Direct: [title]
Question: [title]
Practical: [title]

Keep titles under 60 characters for SEO.
"""
        
        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=200,
                temperature=0.8,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            # Parse response into variations
            lines = response.content[0].text.strip().split('\n')
            variations = {}
            
            for line in lines:
                if ':' in line:
                    key, title = line.split(':', 1)
                    variations[key.strip().lower()] = title.strip()
            
            return variations
            
        except Exception as e:
            print(f"Warning: Could not generate title variations: {e}")
            return {"direct": topic}


if __name__ == "__main__":
    # Test the content generator
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python content_generator.py 'Your blog post topic'")
        sys.exit(1)
    
    topic = sys.argv[1]
    
    try:
        generator = ContentGenerator()
        result = generator.generate_content(topic)
        
        print(f"Generated {result['word_count']} words for: {result['topic']}")
        print(f"Slug: {result['slug']}")
        print("\n" + "="*50)
        print(result['content'])
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)