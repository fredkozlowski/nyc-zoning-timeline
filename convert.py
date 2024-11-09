import re
from collections import defaultdict
from datetime import datetime
import json

def parse_input(input_text):
    sections = re.split(r'\n(?=\d{2,3}-\d{2,3})', input_text.strip())
    data = []
    
    for section in sections:
        lines = section.strip().split('\n')
        if not lines:
            continue
        
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
        if title and date:
            data.append({"title": title, "date": date})
    
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
