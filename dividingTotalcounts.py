def count_unique_words(file_path):
    unique_word_count = 0

    with open(file_path, 'r', encoding='utf-8') as infile:
        for line in infile:
            unique_word_count += 1

    return unique_word_count

# Specify the path to the total word counts file
total_word_counts_file = "/home/ashagaire/Desktop/Python projects/Reddit_Scraping/data/total_word_counts.csv"

# Get the count of unique words
unique_words = count_unique_words(total_word_counts_file)

# Print to console
print(f"Total unique words: {unique_words}")

# Optionally, write to a file
with open("/home/ashagaire/Desktop/Python projects/Reddit_Scraping/data/unique_word_count.txt", 'w') as outfile:
    outfile.write(f"Total unique words: {unique_words}\n")