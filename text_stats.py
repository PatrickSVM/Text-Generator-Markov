import os
import sys
import errno
import re
import string
import numpy as np


def count_letters(a_string):  
    """ cout_letters
    Function that returns sorted list (from max to min) with letter counts in tuples.
    
    Inputs:
            a_string - String whose letters should be counted

    Output:
            letters_sorted  - Sorted list (from max to min) with letter counts in tuples
    """
    
    letter_count = {letter: a_string.count(letter) for letter in string.ascii_lowercase}
    letters_sorted = sorted(letter_count.items(), key=lambda x: x[1], reverse=True)
    return letters_sorted


def most_frequent_words(word_list, k, zipped=True): 
    """ most_frequent_words
    Function that returns sorted list of k most frequent words in a list of words
    
    Inputs:
            word_list - List of words
            k         - Number of most frequent words that should be considered
            zipped    - If set to True, a sorted list (max to min) with tuples of k most frequent words is returned,
                        If set to False, a list with unique words (list) and their count (list) (sorted from max to min) is 
                        retured

    Output:
            top_wrds  - K most frequent words with count
    """
    
    words, count = np.unique(word_list, return_counts=True)
    
    if k == np.inf: # If k equals inf, we want all words and their frequencies
        idx = np.arange(len(words)) # All elements chosen
    else: # If k is not inf, we only get the k-mist frequent words
        idx = np.argpartition(count, -k)[-k:]
    
    words, count = words[idx], count[idx]
    sort_idx = np.argsort(-count)
    top_wrds = [words[sort_idx], count[sort_idx]]
    
    if zipped: # Return zipped result
        top_wrds = list(zip(top_wrds[0], top_wrds[1]))
    
    return top_wrds


def get_word_list(word_string):
    """ get_word_list
    Function takes a string and seperates it into single words (after cleaning).
    
    Inputs:
            word_string - String with words to be extracted

    Output:
            clean_words  - List of individual words
    """
    
    clean_words = word_string.lower()
    clean_words = re.sub(r'\\n', '', clean_words)
    clean_words = re.sub(r',|\?|!|#|\.|:|\(|\)|\"','', clean_words)
    clean_words = re.sub(r'\s{2,}', ' ', clean_words)
    clean_words = re.findall(r'\b[_\w0-9\'’]+\b', clean_words)
    return clean_words


def get_string_from_txt(name_file):
    """ get_string_from_txt
    Function that extracts all lines of a txt-file into one string.
    
    Inputs:
            name_file - Name of a .txt-file

    Output:
            clean_words  - Lowercased string of all content of the file
    """
    
    file = open(name_file)
    clean_words = file.readlines()
    clean_words = list(filter(lambda x: True if x != '\n' else False, clean_words))
    clean_words = " ".join(clean_words)
    clean_words = clean_words.lower()
    file.close()
    return clean_words


class MissingArgError(Exception): # Define Error for missing file 
    pass



if __name__ == "__main__":   # Check whether script is executed from command line
    
    args = sys.argv
    write_output_to_file = False

    if len(args) == 1: # No file name provided
        raise MissingArgError("txt-file has to be provided")
    elif len(args) == 3: # Second file name provided
        write_output_to_file =  True
        out_file = args[2]
    elif len(args) > 3: # Too many arguments provided
        sys.exit("Too many arguments were provided. - Ending script.")

    if not os.path.isfile(args[1]):
        raise FileNotFoundError(os.strerror(errno.ENOENT), args[1])

    

    filename = args[1]   
    clean_words = get_string_from_txt(filename) 
    
    letters_sorted = count_letters(clean_words)

    clean_words = get_word_list(clean_words)

    top_5 = most_frequent_words(clean_words, 5)

    top_words = {tup[0]:{'max_count': tup[1], 'next_words': None} for tup in top_5}
    num_followers = 3
    
    clean_words = np.array(clean_words)
    for word in top_words:
        word_index = np.where(clean_words == word)[0]
        next_idx = word_index + 1
        if next_idx[-1] == len(clean_words): # Make sure its not out of bounds:
            next_idx[-1] = next_idx[:-1]
        
        next_words = clean_words[next_idx]
        top_next = most_frequent_words(next_words, 3)

        top_words[word]['next_words'] = top_next

    
    
    
    # Output generation:
    
    if write_output_to_file: # Check if output should be printed or written to a file
        original_stdout = sys.stdout # Remember standard output
        file = open(out_file, 'w')
        sys.stdout = file # Change output to file - print statements will be saved there now
    
    
    print(f"Analyzed document: {filename}")
    print("======================================\n\n")

    print(f"Letter information:")
    print("--------------------------------------\n")
    print("Let. |  Frequency")
    print("-----|---------")
    for letter in letters_sorted:
        print(f"  {letter[0]}  |  {letter[1]}")
    print("--------------------------------------\n")
    print("\n\n\n")


    print(f"Word information:")
    print("--------------------------------------\n")
    print(f"Count of words:         {len(clean_words)}")
    print(f"Number of unique words: {len(set(clean_words))}")
    print("--------------------------------------\n")
    print("\n\n\n")


    print("Most frequent words:")
    print("--------------------------------------\n")
    for word in top_words:
        print(f"Word: - '{word}' - (Freq: {top_words[word]['max_count']})\n")
        print("Most frequent next words:")
        for i, next_word in enumerate(top_words[word]["next_words"]):
            print(f"--> {i+1}. {next_word[0]}      (Freq: {next_word[1]})")
        print("--------------------------------------\n")
        
    
    
    if write_output_to_file:
        sys.stdout = original_stdout # Reset the standard output to its original value
        file.close() # Close file