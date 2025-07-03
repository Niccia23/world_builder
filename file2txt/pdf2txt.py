import pymupdf
import tiktoken

# Don't forget to change file paths
# pdf_fp = r"what_happened_to_janet_uzor.pdf"
# output_fp = r"example_what_happened_to_janet_uzor.txt"

# Tiktoken Encoder 
enc = tiktoken.get_encoding("o200k_base")

# Open PDF
doc = pymupdf.open(pdf_fp)

# Data to collect
pg_count = doc.page_count
all_text = []
total_tokens = 0

# If you want to extract all pages
# for pg in range(pg_count):
for pg in range(30, 50):
    page = doc.load_page(pg)
    text = page.get_text()
    page_tokens = len(enc.encode(text))
    total_tokens += page_tokens

    all_text.append(text)

combined_text = "".join(all_text)

with open(output_fp, "w", encoding="utf-8") as f:
    f.write(combined_text)



print(f"\nTotal tokens: {total_tokens}")
print(f"Total pages processed: {min(20, doc.page_count - 30)}")
print(f"Text saved to: {output_fp}")
print(f"Total characters: {len(combined_text)}")

doc.close()