"""
Content generator using Claude API
Generates blog post content based on topic and cached writing style
"""
import os
from datetime import datetime
from typing import Dict, Any, Optional

import anthropic
from slugify import slugify

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
        
        # Create length guidance - more concise targets
        length_guide = {
            "short": "400-600 words, focused on a single concept with clear takeaways",
            "medium": "700-1000 words, thorough but concise exploration with examples", 
            "long": "1200-1600 words, comprehensive but structured deep-dive"
        }
        
        target_length = length_guide.get(length, length_guide["medium"])
        
        # Create the prompt
        prompt = f"""
{style_prompt}

TASK: Write a blog post about "{topic}"

REQUIREMENTS:
- Length: {target_length}
- Follow the writing style guide's voice and vocabulary
- Use markdown formatting
- Include practical examples where relevant
- Add image placeholders where they would enhance the content (use format: [IMAGE: Description of image needed])
- Structure with clear headings and sections
- Be concise and avoid repetition
- End with practical takeaways

IMPORTANT CONSTRAINTS:
1. Write ONLY the blog post content. Do not include YAML front matter or Jekyll-specific formatting - just the markdown content that will go inside the post.
2. Do NOT include an H1 title at the beginning - the title will be handled separately by Jekyll
3. Start directly with the content, not with a title
4. Do NOT mention children, kids, family, or parenting - focus on the technology and creative aspects
5. Keep each section focused and avoid repeating the same points
6. Use the British colloquialisms and self-deprecating tech language but keep it professional

LANGUAGE VARIETY CONSTRAINTS:
- DO NOT overuse signature phrases from the style guide - use them sparingly (max once per post)
- AVOID starting with "I've been mucking around with..." or "I was stumbling through..."
- DO NOT use "Mind blown" or "Right?" in every post
- Use different expressions for enthusiasm beyond just "genuinely amazing" and "brilliant"
- Mix up your self-deprecating language - don't always say "crappy hacks"

OPENING STYLE CONSTRAINTS:
- SKIP boring setup sentences like "The other day, I found myself..." or "I was futzing with..."
- START with the actual point - jump straight into the observation or argument
- BEGIN with bold statements, direct observations, or provocative questions
- AVOID "gotten" - use "got" (British usage)
- CUT the fluff - begin where it gets interesting, not with the backstory
- EXAMPLES of good openings: "We're thinking about AI all wrong." "Here's what everyone's missing about..." "Something odd is happening with..."

LANGUAGE TONE CONSTRAINTS:
- DO NOT use forced British swearing like "bloody hell" or "bloody brilliant" - it sounds artificial
- AVOID gratuitous profanity - the author's style is conversational but not sweary
- USE mild British expressions like "proper," "wicked," "brilliant" without overdoing it
- KEEP the tone professional but conversational - not artificially edgy

Begin writing:
"""

        try:
            # Call Claude API - adjusted for more focused and varied content
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=3500,
                temperature=0.75,
                messages=[{
                    "role": "user", 
                    "content": prompt
                }]
            )
            
            content = response.content[0].text
            
            return {
                "content": content,
                "topic": topic,
                "length": length,
                "generated_at": datetime.now().isoformat(),
                "word_count": len(content.split())
            }
            
        except Exception as e:
            raise RuntimeError(f"Failed to generate content: {e}")
    
    def generate_title_variations(self, topic: str) -> Dict[str, str]:
        """Generate title variations in the author's voice"""
        
        # Get style guide for context
        style_prompt = self.style_cache.get_style_prompt()
        
        prompt = f"""
{style_prompt}

Based on the topic "{topic}", write 3 short, natural titles in the author's voice.

Requirements:
- Maximum 8 words per title
- Use the author's vocabulary and tone
- Sound conversational, not corporate
- Match their British sensibilities and self-deprecating style

Generate exactly 3 titles in this format:

Straightforward: [short title here]
Provocative: [short title here]  
Personal: [short title here]

Do not include any commentary or explanation - just the three titles.
"""
        
        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=150,
                temperature=0.8,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            # Parse response into variations
            text = response.content[0].text.strip()
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            variations = {}
            
            for line in lines:
                if ':' in line and not line.startswith('['):
                    # Split on first colon only
                    parts = line.split(':', 1)
                    if len(parts) == 2:
                        key = parts[0].strip().lower()
                        title = parts[1].strip()
                        # Remove any extra formatting
                        title = title.replace('[', '').replace(']', '').strip()
                        if title and len(title) < 100:  # Sanity check for length
                            variations[key] = title
            
            # Fallback if parsing failed
            if not variations:
                variations = {"straightforward": topic}
            
            return variations
            
        except Exception as e:
            print(f"Warning: Could not generate title variations: {e}")
            return {"straightforward": topic}


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