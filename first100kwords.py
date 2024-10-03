def save_first_100000_words(input_file, output_file, limit=100000):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for i, line in enumerate(infile):
            if i < limit:
                outfile.write(line)
            else:
                break

# Specify the input and output file paths
total_word_counts_file = "/home/ashagaire/Desktop/Python projects/Reddit_Scraping/data/total_word_counts.csv"
output_file_path = "/home/ashagaire/Desktop/Python projects/Reddit_Scraping/data/first_100000_word_counts.csv"

save_first_100000_words(total_word_counts_file, output_file_path)