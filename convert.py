import re
from collections import defaultdict
from datetime import datetime
import json

def convert_to_roman(number):
    """Convert Arabic number to lowercase Roman numeral."""
    if not isinstance(number, int):
        return number
    
    roman_nums = [
        (1000, "m"), (900, "cm"), (500, "d"), (400, "cd"),
        (100, "c"), (90, "xc"), (50, "l"), (40, "xl"),
        (10, "x"), (9, "ix"), (5, "v"), (4, "iv"), (1, "i")
    ]
    
    result = ""
    for value, numeral in roman_nums:
        while number >= value:
            result += numeral
            number -= value
    return result

def generate_url(section_id):
    """Generate URL from section ID (e.g., '22-341' -> article-ii/chapter-2/22-341)"""
    try:
        # Extract article and chapter numbers
        if len(section_id.split('-')[0]) == 3:  # For cases like 124-00
            article_num = int(section_id[:2])  # First two digits for article
            chapter_num = int(section_id[2])   # Third digit for chapter
        else:  # For cases like 22-341
            article_num = int(section_id[0])   # First digit for article
            chapter_num = int(section_id[1])   # Second digit for chapter
        
        # Convert article number to roman numeral
        article_roman = convert_to_roman(article_num)
        
        # Construct the URL
        base_url = "https://zoningresolution.planning.nyc.gov"
        url = f"{base_url}/article-{article_roman}/chapter-{chapter_num}/{section_id}"
        
        return url
    except:
        return None

def parse_input(input_text):
    sections = re.split(r'\n(?=\d{2,3}-\d{2,3})', input_text.strip())
    data = []
    
    for section in sections:
        lines = section.strip().split('\n')
        if not lines:
            continue
        
        # Extract section ID and title
        first_line = lines[0]
        section_match = re.match(r'(\d{2,3}-\d{2,3})', first_line)
        
        if not section_match:
            continue
            
        section_id = section_match.group(1)
        title_parts = []
        date = None
        
        for line in lines:
            if line.startswith('LAST AMENDED'):
                date_match = re.search(r'LAST AMENDED (\d{1,2}/\d{1,2}/\d{4})', line)
                if date_match:
                    date_str = date_match.group(1)
                    date = datetime.strptime(date_str, '%m/%d/%Y').strftime('%Y-%m-%d')
                break
            else:
                title_parts.append(line)
        
        title = '\n'.join(title_parts).split(' - ', 1)[-1].strip()
        url = generate_url(section_id)
        
        if title and date and url:
            data.append({
                "title": title,
                "date": date,
                "url": url,
                "section_id": section_id
            })
    
    return data

def group_by_month(data):
    grouped = defaultdict(lambda: {"items": [], "count": 0})
    for item in data:
        year_month = item['date'][:7]  # Extract YYYY-MM
        grouped[year_month]["items"].append(item)
        grouped[year_month]["count"] += 1
    return dict(grouped)

def main():
    # Read input from all_outputs.txt
    with open('all_outputs.txt', 'r') as file:
        input_text = file.read()
        
    parsed_data = parse_input(input_text)
    grouped_data = group_by_month(parsed_data)
    
    # Write output to amendments.json
    with open('amendments.json', 'w') as file:
        json.dump(grouped_data, file, indent=2)

if __name__ == "__main__":
    main()
