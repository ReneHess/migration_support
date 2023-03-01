import os
import pandas as pd
import re
import datetime
import json
import openpyxl

from PyPDF2 import PdfReader

# Set folder ppip uninstall PyPDF2ath
folder_path = 'C:\\Users\\ReneHess\\OneDrive - LexiFi\\Documents\\test data'

# Set keywords to search for
keywords = [
    ['Review Dates', 400, "date", "valuation_dates"],
    ['Averaging Dates', 400, "date","averaging_dates"],
    ['Maturity Date', 55, "date","redemption_date"],
    ['Scheduled Redemption', 55, "date","redemption_date"],
    ['Pricing Date', 45, "date","initial_fixing_date"],
    ['Strike Date', 45, "date","initial_fixing_date"],
    ['Issue Date', 45, "date","issue_date"],
    ['Valuation Date', 55, "date", "final_fixing_date"],
    ['Valuation Date:', 55, "date", "final_fixing_date"],
    ['Final Valuation Date', 55, "date", "final_fixing_date"],
    ['Determination Date', 55, "date", "final_fixing_date"],
    ['Redemption Valuation Date', 55, "date", "final_fixing_date"],
    ['Redemption Valuation', 55, "date", "final_fixing_date"],
    ['Valuation Dates', 400, "date", "valuation_dates"],
    #['Barrier:', 100,"percentage"],
    #['Knock-In:', 100,"percentage"]
]


def extract_dates(text, keyword_reg, max_distance, reg_type):
    # Find the index of the keyword in the text
    indices = []
    start = 0
    while True:
        index = text.lower().find(keyword_reg.lower(),start)
        if index == -1:
            break
        indices.append(index)
        start = index + len(keyword_reg)

    keyword_index = text.lower().find(keyword_reg.lower())
    regex = ""
    # Find the substring of text within the specified distance from the keyword
    for keyword_index in indices:
        substring = text[max(0, keyword_index):min(len(text), keyword_index + max_distance)] #- max_distance
        if reg_type == "date":
            regex = r"\b(January|February|March|April|May|June|July|August|September|October|November|December)\s(\d{1," \
                    r"2})(?:st|nd|rd|th)?(?:\s|\.)?,?\s(\d{4})\b"
        elif reg_type == "percentage":
            regex = r"\b\d{1,3}\.\d{2}%\b(?=\s+(of\s+the\s+)?initial\s+(price|level|fixing))"
        # Use regular expressions to extract all dates in the substring
        dates = re.findall(regex, substring)
        dates = list(
            map(lambda match: datetime.datetime.strptime(f"{match[0]} {match[1]}, {match[2]}", "%B %d, %Y").strftime(
                "%Y-%m-%d"), dates))
        if dates != []:
            return dates
    return None


def extract_ids(s):
    # Find the index of the first and second opening brackets
    first_bracket_index = s.find("[")
    second_bracket_index = s.find("[", first_bracket_index + 1)

    # Find the index of the first and second closing brackets
    first_close_bracket_index = s.find("]")
    second_close_bracket_index = s.find("]", first_close_bracket_index + 1)

    # Extract the first and second values between the brackets
    first_value = s[first_bracket_index + 1: first_close_bracket_index]
    second_value = s[second_bracket_index + 1: second_close_bracket_index]

    return first_value


# Create an empty dictionary to store search results
search_results = {}
data_extraction = []

# Loop through all PDF files in the folder
for filename in os.listdir(folder_path):
    try:
        if filename.endswith('.pdf'):
            # Open the PDF file
            # Create a PDF viewer object
            sp_id = extract_ids(filename)
            reader = PdfReader(os.path.join(folder_path, filename))
            # Loop through all pages in the PDF
            rec = {'id': sp_id}
            for page in reader.pages:
                page_text = page.extract_text()
                for keyword_l in keywords:
                    keyword = keyword_l[0]
                    distance = keyword_l[1]
                    regex_t = keyword_l[2]
                    if keyword.lower() in page_text.lower():
                        # Add the filename to the search results dictionary
                       # if keyword in search_results:
                            # search_results[keyword].append(filename)
                        result_r = extract_dates(page_text, keyword, distance, regex_t)
                        if result_r:
                            rec[keyword_l[3]] = extract_dates(page_text, keyword, distance, regex_t)

                        #else:
                        #     search_results[keyword] = [filename]

            data_extraction.append(rec)
    except:
        print(filename)

files = []

with open(os.path.join(folder_path, 'test.json'), 'w') as f:
    json.dump(data_extraction, f)

for x in data_extraction:
 #  files = list(set(files))

 print(x)
# df = pd.DataFrame({'Averageing': files})

# df.to_excel('C:\\Users\\ReneHess\\OneDrive - LexiFi\\Documents\\test data\\Averagingd.xlsx')
