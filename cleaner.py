# Need to install unidecode: pip install unidecode

import csv
import re
from unidecode import unidecode

def clean(x):
    # Convert to a lowercase string and normalize characters.
    # https://stackoverflow.com/questions/517923/what-is-the-best-way-to-remove-accents-normalize-in-a-python-unicode-string
    result = unidecode(str(x).lower())

    # Remove single quotes, double quotes, periods, commas, question marks
    # exclamation points, apostrophe.
    result = re.sub(r"[\'\"\.\,\-\?\!\`]", "", result)

    # Remove string surrounded by parenthesis, brackets, or braces.
    result = re.sub(r"\([^)]*\)", " ", result)
    result = re.sub(r"\[[^]]*\]", " ", result)
    result = re.sub(r"\{[^}]*\}", " ", result)

    # Replace any whitespace characters with a single space.
    result = re.sub(r"(\s)+", " ", result)

    return result

with open("combined_output_Nov22.csv", encoding="utf-8") as file:
    # Our input CSV file to clean.
    reader = csv.DictReader(file)

    # Our output CSV file to write to.
    OutputFile = open("new_output.csv", "w+")
    fields = ["title", "artist", "lyrics", "genre"]
    writer = csv.DictWriter(OutputFile, fieldnames=fields)

    # First write the column names to file.
    writer.writeheader()

    # Loop through each row.
    for row in reader:
        NewRow = {
            "title":        clean(row["song"]),
            "artist":       clean(row["artist"]),
            "lyrics":       clean(row["lyrics"]),
            "genre":        clean(row["majority_genre"])
        }

        # Send to output file.
        writer.writerow(NewRow)

    # Close output stream.
    OutputFile.close()