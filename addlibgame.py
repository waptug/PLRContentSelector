import subprocess
import re

# Check if nltk is installed, if not, install it
try:
    import nltk
except ImportError:
    subprocess.run(["pip", "install", "nltk"])

from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

# Download necessary NLTK resources if not already downloaded
nltk.download('punkt', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)

# Function to tokenize the article and replace interesting parts with tokens
def tokenize_article(article, target_pos):
    tokens = word_tokenize(article)
    tagged_tokens = pos_tag(tokens)
    replacements = {}
    new_article_tokens = []
    token_count = 1

    for word, pos in tagged_tokens:
        if pos in target_pos:  # Targeting user-specified parts of speech
            token = f"{{TOKEN{token_count}}}"
            replacements[token] = (word, pos)
            new_article_tokens.append(token)
            token_count += 1
        else:
            new_article_tokens.append(word)

    return " ".join(new_article_tokens), replacements

# Function to collect user inputs for the tokens
def collect_user_inputs(replacements):
    user_inputs = {}
    pos_descriptions = {
        'NN': 'noun',
        'JJ': 'adjective',
        'VB': 'verb',
    }

    for token, (original_word, pos) in replacements.items():
        description = pos_descriptions.get(pos, "word")
        user_input = input(f"Please provide a replacement for the {description} '{original_word}' ({token}): ")
        user_inputs[token] = user_input

    return user_inputs

# Function to generate the new PLR article using user inputs
def generate_new_article(tokenized_article, user_inputs):
    new_article = tokenized_article
    for token, user_input in user_inputs.items():
        new_article = new_article.replace(token, user_input)

    return new_article

# Main code to execute the process
if __name__ == "__main__":
    file_path = input("Please enter the path to the PLR article file: ")
    with open(file_path, 'r') as file:
        plr_article = file.read()

    target_pos = input("Please enter the parts of speech to target (e.g., NN, JJ, VB): ").split(',')
    tokenized_article, replacements = tokenize_article(plr_article, target_pos)
    print("\nTokenized Article:")
    print(tokenized_article)

    user_inputs = collect_user_inputs(replacements)
    new_article = generate_new_article(tokenized_article, user_inputs)

    output_path = input("Please enter the path to save the new PLR article: ")
    with open(output_path, 'w') as file:
        file.write(new_article)

    print("\nGenerated New PLR Article:")
    print(new_article)
    print(f"\nThe new PLR article has been saved to {output_path}")
