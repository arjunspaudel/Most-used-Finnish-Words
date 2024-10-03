import os
from collections import Counter
import csv

def combine_word_counts(input_folder, output_file):
    total_word_counter = Counter()

    for filename in os.listdir(input_folder):
        if filename.endswith('.csv'):
            file_path = os.path.join(input_folder, filename)
            with open(file_path, 'r', encoding='utf-8') as infile:
                reader = csv.reader(infile)
                for row in reader:
                    if len(row) == 2:
                        word, count = row
                        total_word_counter[word] += int(count)

    with open(output_file, 'w', encoding='utf-8') as outfile:
        for word, count in total_word_counter.most_common():
            outfile.write(f"{word},{count}\n")

# Specify the input directory and output file path
input_folder = "/home/ashagaire/Desktop/Python projects/Reddit_Scraping/data/words_count"
output_file = "/home/ashagaire/Desktop/Python projects/Reddit_Scraping/data/total_word_counts.csv"

combine_word_counts(input_folder, output_file)