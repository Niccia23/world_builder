import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

# Your EPUB file path
# Edit this path to point to your EPUB file
ebook_fp = r".\world_builder\file2txt\data\epub\East_of_Eden.epub"

# Read the EPUB file
book = epub.read_epub(ebook_fp)

# Get document items (chapters/content) - convert generator to list
document_items = list(book.get_items_of_type(ebooklib.ITEM_DOCUMENT))

print(f"Found {len(document_items)} document items in the EPUB:")
print("-" * 50)

# Display information about each document item
for i, item in enumerate(document_items, 1):
    print(f"\nDocument {i}:")
    print(f"  ID: {item.id}")
    print(f"  File name: {item.file_name}")
    print(f"  Media type: {item.media_type}")
    
    # Extract and display first 200 characters of text content
    try:
        html_content = item.get_content().decode('utf-8')
        soup = BeautifulSoup(html_content, 'html.parser')
        text = soup.get_text().strip()
        
        if text:
            preview = text[:200] + "..." if len(text) > 200 else text
            print(f"  Preview: {preview}")
        else:
            print(f"  Preview: [No readable text content]")
    except Exception as e:
        print(f"  Preview: [Error reading content: {e}]")
    
    print("-" * 30)

# Optional: Extract all text content
print("\n" + "="*50)
print("FULL TEXT EXTRACTION")
print("="*50)

all_text = []
for item in document_items:
    try:
        html_content = item.get_content().decode('utf-8')
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        text = soup.get_text()
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        clean_text = ' '.join(chunk for chunk in chunks if chunk)
        
        if clean_text.strip():
            all_text.append(clean_text)
            
    except Exception as e:
        print(f"Error processing {item.file_name}: {e}")

# Join all text and display stats
full_text = "\n\n".join(all_text)
print(f"\nExtracted text statistics:")
print(f"Total characters: {len(full_text):,}")
print(f"Total words: {len(full_text.split()):,}")
print(f"Total lines: {len(full_text.splitlines()):,}")

# Edit the output file path as needed
output_file = r".\world_builder\file2txt\data\txt\East_of_Eden.txt"
try:
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(full_text)
    print(f"\nText saved to: {output_file}")
except Exception as e:
    print(f"\nError saving file: {e}")

# Display first 1000 characters as preview
print(f"\nFirst 1000 characters of extracted text:")
print("-" * 50)
print(full_text[:1000] + "..." if len(full_text) > 1000 else full_text)