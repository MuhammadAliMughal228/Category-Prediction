import pandas as pd
from googletrans import Translator
from fuzzywuzzy import fuzz

# Load the CSV file
df = pd.read_csv('/content/file (1).csv')

# Initialize the Google Translator
translator = Translator()

# Function to translate the description into English
def translate_to_english(text):
    try:
        translated = translator.translate(text, src='auto', dest='en')
        return translated.text
    except Exception as e:
        print(f"Error translating {text}: {e}")
        return text  # In case of any error, return the original text

# Translate the 'Description' column into English
df['Description'] = df['Description'].apply(translate_to_english)

# Load the category dictionary from the mapp.txt file
with open('/content/expanded-category-dict.py', 'r') as f:
    file_content = f.read()
    exec(file_content)  # This will define category_dict from the file

# Convert both dictionary keys and the values to lowercase
category_dict_lower = {key.lower(): value.lower() for key, value in category_dict.items()}

# Define a function to categorize descriptions using fuzzy matching
def categorize(description, threshold=80):
    description_lower = description.lower()  # Convert description to lowercase
    best_match = 'Unknown'
    highest_ratio = 0

    for keyword, category in category_dict_lower.items():
        match_ratio = fuzz.partial_ratio(keyword, description_lower)

        if match_ratio > highest_ratio and match_ratio >= threshold:
            highest_ratio = match_ratio
            best_match = category

    return best_match

# Apply the fuzzy search function to create a new 'Category' column
df['Category'] = df['Description'].apply(categorize)
df['Category'] = df['Category'].str.upper()
# Save the updated dataframe if needed
df.to_csv('output_file.csv', index=False)

# Display the dataframe with the new column
df.head(50)
