import os
import pandas as pd
import re
import datetime
import openpyxl

from PyPDF2 import PdfReader

# Set folder ppip uninstall PyPDF2ath
folder_path = 'C:\\Users\\ReneHess\\OneDrive - LexiFi\\Documents\\test data'

# Set keywords to search for
keywords = ['Averaging Dates:']
def extract_dates(text, keyword, max_distance):
    # Find the index of the keyword in the text
    keyword_index = text.find(keyword)

    # Find the substring of text within the specified distance from the keyword
    substring = text[max(0, keyword_index - max_distance):min(len(text), keyword_index + max_distance)]
    date_regex =  r"\b(January|February|March|April|May|June|July|August|September|October|November|December)\s(\d{1,2}),\s(\d{4})\b"
    # Use regular expressions to extract all dates in the substring
    dates = re.findall(date_regex, substring)
    dates = list(map(lambda match: datetime.datetime.strptime(f"{match[0]} {match[1]}, {match[2]}", "%B %d, %Y").strftime("%Y-%m-%d"), dates))

    return dates

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
            for page in reader.pages:
                page_text = page.extract_text()
                for keyword in keywords:
                    if keyword in page_text:
                    # Add the filename to the search results dictionary
                        if keyword in search_results:
                            #search_results[keyword].append(filename)
                            rec = {'id': sp_id, 'avg_dates': extract_dates(page_text, keyword, 400)}
                            data_extraction.append(rec)
                        else:
                            search_results[keyword] = [filename]
    except:
        print(filename)

files = []

for x in data_extraction:
 #   files = list(set(files))

    print(x)
#df = pd.DataFrame({'Averageing': files})

#df.to_excel('C:\\Users\\ReneHess\\OneDrive - LexiFi\\Documents\\test data\\Averagingd.xlsx')