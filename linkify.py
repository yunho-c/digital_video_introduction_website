import re

file_path = 'index.html'

with open(file_path, 'r') as f:
    content = f.read()

# Regex to find URLs inside <li> tags that are not already links
# Looking for <li>http...</li> or <li>https...</li>
# We need to be careful not to double link if I run this multiple times, but currently they are plain text.

def replace_link(match):
    url = match.group(1)
    # Check if it's already an anchor tag (simple check)
    if '<a ' in url:
        return match.group(0)
    
    # Clean up trailing whitespace or <br> if any (though regex handles <li>...</li>)
    clean_url = url.strip()
    
    # Handle the case where there is text after the URL (e.g. "(was: ...)")
    # We'll just link the URL part.
    
    # Better approach: Find URLs within the text and linkify them.
    # URL regex pattern
    url_pattern = r'(https?://[^\s<]+)'
    
    linked_content = re.sub(url_pattern, r'<a href="\1">\1</a>', clean_url)
    
    return f'<li>{linked_content}</li>'

# Apply to all <li> items that contain http
# We limit this to the References section to be safe, but doing it globally might be okay if we are careful.
# Let's find the references section first.

ref_start = content.find('<section id="references"')
if ref_start != -1:
    pre_ref = content[:ref_start]
    ref_content = content[ref_start:]
    
    # Replace in ref_content
    # Find <li>...</li> blocks
    ref_content = re.sub(r'<li>(.*?)</li>', replace_link, ref_content, flags=re.DOTALL)
    
    new_content = pre_ref + ref_content
    
    with open(file_path, 'w') as f:
        f.write(new_content)
    print("Links updated in References section.")
else:
    print("References section not found.")
