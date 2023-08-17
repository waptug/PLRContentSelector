import subprocess
import os
import random

# Check if nltk and chardet are installed, if not, install them
try:
    import nltk
except ImportError:
    subprocess.run(["pip", "install", "nltk"])

try:
    import chardet
except ImportError:
    subprocess.run(["pip", "install", "chardet"])

from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

# Download necessary NLTK resources if not already downloaded
nltk.download('punkt', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('wordnet', quiet=True)

# Function to read the file with proper encoding
def read_file_with_encoding(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
        content = raw_data.decode(encoding)
        
        # Convert to UTF-8 if not already
        if encoding.lower() != 'utf-8':
            content = content.encode('utf-8').decode('utf-8')

    return content

# Function to randomly pick a file from the source directory
def pick_random_file(source_directory):
    all_files = []
    for root, _, files in os.walk(source_directory):
        for file_name in files:
            all_files.append(os.path.join(root, file_name))
    return random.choice(all_files)

# Function to get a random synonym for a word
def get_random_synonym(word):
    synonyms = wordnet.synsets(word)
    if synonyms:
        words = synonyms[0].lemmas()
        if words:
            return words[0].name()
    return word  # Return the original word if no synonym is found

# Function to tokenize the article and replace interesting parts with tokens
def tokenize_article(article, target_pos):
    tokens = word_tokenize(article)
    tagged_tokens = pos_tag(tokens)
    new_article_tokens = []

    for word, pos in tagged_tokens:
        if pos in target_pos:  # Targeting user-specified parts of speech
            replacement_word = get_random_synonym(word)
            new_article_tokens.append(replacement_word)
        else:
            new_article_tokens.append(word)

    return " ".join(new_article_tokens)

# Main code to execute the process
if __name__ == "__main__":
    source_directory = input("Please enter the path to the source directory: ")
    file_path = pick_random_file(source_directory)
    print(f"Selected file: {file_path}")

    plr_article = read_file_with_encoding(file_path)

    target_pos = input("Please enter the parts of speech to target (e.g., NN, JJ, VB): ").split(',')
    new_article = tokenize_article(plr_article, target_pos)
    print("\nSpun Article:")
    print(new_article)

    output_path = input("Please enter the path to save the spun PLR article: ")
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(new_article)

    print(f"\nThe spun PLR article has been saved to {output_path}")
