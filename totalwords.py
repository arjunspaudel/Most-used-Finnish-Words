import os
import csv
import re

def count_words_and_estimate_pages(file_path, words_per_page=500):
    word_count = 0
    with open(file_path, 'r', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        next(reader, None)  # Skip the header row
        for row in reader:
            if len(row) > 1:
                text = row[1]  # Assuming the comment text is in the second column
                words = text.split()
                word_count += len(words)
    estimated_pages = round(word_count / words_per_page)
    return word_count, estimated_pages

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split('(\d+)', s)]

def count_words_in_directory(directory, output_file, words_per_page=500):
    total_word_count = 0
    total_estimated_pages = 0
    file_word_counts = []

    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            file_path = os.path.join(directory, filename)
            print(f"Processing file: {filename}")  # Debugging output
            word_count, estimated_pages = count_words_and_estimate_pages(file_path, words_per_page)
            file_word_counts.append((filename, word_count, estimated_pages))
            total_word_count += word_count
            total_estimated_pages += estimated_pages

    # Sort the list of file word counts by filename using natural sort
    file_word_counts = sorted(file_word_counts, key=lambda x: natural_sort_key(x[0]))

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Write the results to a CSV file
    with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(["Filename", "Word Count", "Estimated Pages"])
        for filename, word_count, estimated_pages in file_word_counts:
            writer.writerow([filename, word_count, estimated_pages])
        writer.writerow(["Total", total_word_count, round(total_estimated_pages)])

    print(f"Results written to {output_file}")  # Debugging output

# Specify the directory containing the CSV files and the output file path
directory_path = "/home/ashagaire/Desktop/Python projects/Reddit_Scraping/data/CSV"
output_file_path = "/home/ashagaire/Desktop/Python projects/Reddit_Scraping/data/word_count_summary.csv"

count_words_in_directory(directory_path, output_file_path)