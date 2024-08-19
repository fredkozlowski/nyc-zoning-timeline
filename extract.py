import re
import pdfplumber

def extract_titles_and_dates(pdf_path, output_path):
    with pdfplumber.open(pdf_path) as pdf:
        # Pattern to match title, with optional "LAST AMENDED" and date
        title_pattern = r'(?s)(\d{2,3}-\d{2,3}.-..*?(?=LAST AMENDED))(?:\s*LAST\s*AMENDED\s*(\d{1,2}/\d{1,2}/\d{4})?)?'
        
        results = []
        debug_info = []
        
        # Process each page separately
        for page_num, page in enumerate(pdf.pages, start=1):
            page_text = page.extract_text()
            
            # Find all potential titles on this page
            # print(page_text)
            matches = re.finditer(title_pattern, page_text, re.IGNORECASE )
            
            for match in matches:
                # print('match group 1 strip')
                # print(match.group(1).strip())
                # print('match group 1')
                # print(match.group(1))
                # print('match group 2')
                # print(match.group(2))
                title = match.group(1).strip()
                date = match.group(2)
                
                # Extract words with their positions and fonts
                words_with_fonts = page.extract_words(keep_blank_chars=True, use_text_flow=True, extra_attrs=['fontname'])
                
                # Find the word(s) that match the beginning of the title
                # title_words = title.split('-')
                matching_words = [word for word in words_with_fonts if title[:2] in word['text']]  # Check first two words
                # print('title')
                # print(title)
                # print('matching words')
                # print(matching_words)
                # for word in matching_words:
                #     print(word['fontname'])
                #
                # print('-------')

                
                is_stone_sans_bold = any('StoneSansBold' in word['fontname'] for word in matching_words)
                
                # If date is not found, look ahead for "LAST AMENDED" and date
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
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(results))
    
    with open('debug_output.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(debug_info))

# Usage
pdf_path = 'Article01.pdf'
output_path = 'output.txt'
extract_titles_and_dates(pdf_path, output_path)
print(f"Processing complete. Check {output_path} for results and debug_output.txt for debugging information.")
