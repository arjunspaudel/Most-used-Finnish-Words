import csv
from collections import Counter
import re
import os

def count_words_in_csv(file_path, output_path):
    word_counter = Counter()

    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        text_column_index = 1  # Assuming the text is in the second column

        for row_number, row in enumerate(reader):
            if len(row) > text_column_index:
                text = row[text_column_index]
                words = re.findall(r'\b\w+\b', text, re.UNICODE)
                word_counter.update(words)

    with open(output_path, 'w', encoding='utf-8') as outfile:
        for word, count in word_counter.most_common():
            outfile.write(f"{word},{count}\n")

def process_all_csv_files(data_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(data_folder):
        if filename.endswith('.csv'):
            input_file_path = os.path.join(data_folder, filename)
            output_file_name = f"{os.path.splitext(filename)[0]}_word_counts.csv"
            output_file_path = os.path.join(output_folder, output_file_name)
            print(f"Processing {filename}...")
            count_words_in_csv(input_file_path, output_file_path)
            print(f"Word count for {filename} saved to {output_file_name}")

# Specify the input and output directories
data_folder = "/home/ashagaire/Desktop/Python projects/Reddit_Scraping/data"
output_folder = os.path.join(data_folder, "words_count")

process_all_csv_files(data_folder, output_folder)