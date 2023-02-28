import re

text = "The date is January 9, 2023."
date_regex = r"\b(January|February|March|April|May|June|July|August|September|October|November|December)\s(\d{1,2}),\s(\d{4})\b"
matches = re.findall(date_regex, text)

print(matches)  # Output: ['January 9, 2023']