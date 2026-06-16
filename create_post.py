#!/usr/bin/env python3
import sys
import subprocess
import os
import re
from datetime import datetime

def slugify(title):
    """Convert title to a URL-friendly slug."""
    # Convert to lowercase
    slug = title.lower()
    # Replace Polish characters and other special chars
    polish_chars = {
        'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l', 'ń': 'n',
        'ó': 'o', 'ś': 's', 'ź': 'z', 'ż': 'z'
    }
    for pl, en in polish_chars.items():
        slug = slug.replace(pl, en)
    # Replace spaces and special characters with hyphens
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    # Remove leading/trailing hyphens
    slug = slug.strip('-')
    return slug

def get_current_year():
    """Get current year."""
    return datetime.now().strftime('%Y')

def update_front_matter(file_path, title, pinned=False):
    """Update the front matter with the original title and optional pinning."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split the content by front matter delimiters (---)
    parts = content.split('---', 2)
    
    if len(parts) >= 3:
        # Front matter is in parts[1]
        front_matter = parts[1]
        
        # Update or add the title
        # Look for existing title: line
        title_pattern = r'^title:\s*["\']?.*["\']?\s*$'
        if re.search(title_pattern, front_matter, re.MULTILINE):
            # Replace existing title
            front_matter = re.sub(
                title_pattern,
                f'title: "{title}"',
                front_matter,
                flags=re.MULTILINE
            )
        else:
            # Add title if it doesn't exist
            front_matter = front_matter.rstrip() + f'\ntitle: "{title}"\n'
        
        # Add weight if pinned
        if pinned:
            if not re.search(r'^weight:', front_matter, re.MULTILINE):
                front_matter = front_matter.rstrip() + '\nweight: 1\n'
        
        # Reconstruct the file content
        new_content = f"---{front_matter}---{parts[2]}"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

def main():
    # Get title from stdin
    print("Enter post title: ", end='', flush=True)
    title = sys.stdin.readline().strip()
    
    if not title:
        print("Error: Title cannot be empty")
        sys.exit(1)
    
    # Generate filename from title
    slug = slugify(title)
    year = get_current_year()
    post_path = f"post/{year}/{slug}/index.md"
    
    # Create the post with Hugo
    try:
        cmd = ["hugo", "new", "content", post_path]
        print(f"Running: {' '.join(cmd)}")
        subprocess.run(cmd, check=True)
        print(f"Created: {post_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error creating post: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("Error: Hugo command not found. Is Hugo installed?")
        sys.exit(1)
    
    # Get the full path to the created file
    full_path = os.path.join("content", post_path)
    
    # Update the front matter with the original title
    try:
        update_front_matter(full_path, title)
        print(f"Updated title to: {title}")
    except Exception as e:
        print(f"Error updating title: {e}")
        sys.exit(1)
    
    # Open in default console editor (respects $EDITOR env var)
    editor = os.environ.get('EDITOR', 'nano')  # Default to nano if no EDITOR set
    
    try:
        print(f"Opening {full_path} in {editor}...")
        subprocess.run([editor, full_path])
    except FileNotFoundError:
        print(f"Warning: Editor '{editor}' not found. File created at: {full_path}")
    except KeyboardInterrupt:
        print("\nEditor closed.")
    except Exception as e:
        print(f"Error opening editor: {e}")

if __name__ == "__main__":
    main()
