import os
import re

FILLER_WORDS = set([
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during", "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves",
    "basically", "actually", "just", "really", "simply", "literally", "essentially", "practically", "virtually", "merely", "fairly", "quite", "somewhat", "somehow", "perhaps", "maybe", "probably", "certainly", "definitely", "absolutely", "obviously", "clearly", "apparently", "seemingly", "sort", "kind", "like", "well", "anyway", "anyhow"
])

def remove_fillers_from_text(text):
    # Dynamically build regex
    pattern_str = r'\b(?:' + '|'.join(sorted(list(FILLER_WORDS), key=len, reverse=True)) + r')\b[ \t]*'
    # Use re.IGNORECASE to match any case
    text = re.sub(pattern_str, '', text, flags=re.IGNORECASE)
    
    # Clean up double spaces that might have been created
    text = re.sub(r' {2,}', ' ', text)
    # Clean up spaces before punctuation
    text = re.sub(r' \.', '.', text)
    text = re.sub(r' \,', ',', text)
    
    return text

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Split by markdown blocks we want to keep intact
    # 1. Frontmatter \A---\n.*?\n---
    # 2. Code blocks ```.*?```
    # 3. Inline code `.*?`
    # 4. Markdown links \[.*?\]\(.*?\)
    # 5. HTML Tags <.*?> (to protect URLs or HTML like <br>)
    pattern = re.compile(r'(\A---\n.*?\n---|```.*?```|`.*?`|\[.*?\]\(.*?\)|<.*?>)', flags=re.MULTILINE | re.DOTALL)
    parts = pattern.split(content)
    
    for i in range(len(parts)):
        if i % 2 == 0: # text parts
            parts[i] = remove_fillers_from_text(parts[i])
            
    new_content = "".join(parts)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

if __name__ == "__main__":
    docs_dir = "/Users/studio/Documents/Sandbox/Unsloth-docs"
    for filename in os.listdir(docs_dir):
        if filename.endswith(".md"):
            print(f"Processing {filename}...")
            process_file(os.path.join(docs_dir, filename))
    print("Finished removing filler words.")
