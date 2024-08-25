import re
import pdfplumber
import os

def extract_titles_and_dates(pdf_path, output_path):
    with pdfplumber.open(pdf_path) as pdf:
        title_pattern = r'(?s)(\d{2,3}-\d{2,3}.-..*?(?=LAST AMENDED))(?:\s*LAST\s*AMENDED\s*(\d{1,2}/\d{1,2}/\d{4})?)?'
        
        results = []
        debug_info = []
        
        for page_num, page in enumerate(pdf.pages, start=1):
            page_text = page.extract_text()
            matches = re.finditer(title_pattern, page_text, re.IGNORECASE)
            
            for match in matches:
                title = match.group(1).strip()
                date = match.group(2)
                
                words_with_fonts = page.extract_words(keep_blank_chars=True, use_text_flow=True, extra_attrs=['fontname'])
                matching_words = [word for word in words_with_fonts if title[:2] in word['text']]
                
                is_stone_sans_bold = any('StoneSansBold' in word['fontname'] for word in matching_words)
                
                if not date:
                    last_amended_match = re.search(r'LAST\s*AMENDED\s*(\d{1,2}/\d{1,2}/\d{4})', 
                                                   page_text[match.end():match.end()+200], 
                                                   re.IGNORECASE | re.DOTALL)
                    if last_amended_match:
                        date = last_amended_match.group(1)
                
                font_info = "StoneSansBold" if is_stone_sans_bold else "Not StoneSansBold"
                
                if date:
                    results.append(f"{title}\nLAST AMENDED {date}\nFound on page {page_num}\nFont: {font_info}\n")
                    debug_info.append(f"Found: {title} - {date} - Page {page_num} - Font: {font_info}")
                else:
                    results.append(f"{title}\nFound on page {page_num}\nFont: {font_info}\n")
                    debug_info.append(f"Title found without date: {title} - Page {page_num} - Font: {font_info}")
    
    return results, debug_info

def process_multiple_pdfs(start_num, end_num):
    all_results = []
    all_debug_info = []
    
    for i in range(start_num, end_num + 1):
        pdf_path = f'Article{i:02d}.pdf'
        if os.path.exists(pdf_path):
            print(f"Processing {pdf_path}...")
            results, debug_info = extract_titles_and_dates(pdf_path, '')
            all_results.extend([f"Results for {pdf_path}:"] + results + ["\n"])
            all_debug_info.extend([f"Debug info for {pdf_path}:"] + debug_info + ["\n"])
        else:
            print(f"File {pdf_path} not found. Skipping...")
    
    with open('all_outputs.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(all_results))
    
    with open('all_debug_outputs.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(all_debug_info))

# Usage
start_num = 1
end_num = 14
process_multiple_pdfs(start_num, end_num)
print(f"Processing complete. Check all_outputs.txt for results and all_debug_outputs.txt for debugging information.")
