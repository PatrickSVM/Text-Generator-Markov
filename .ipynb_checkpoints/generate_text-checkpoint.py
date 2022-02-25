from text_stats import get_word_list, get_string_from_txt

import os
import sys
import errno
import numpy as np


def get_neighbour_matrix(word_list):
    """ get_neighbour_matrix
    Function that returns a matrix with the probabilities of each word following each other
    
    Inputs:
            word_list - List of words

    Output:
            idx_mapping  - Mapping of the unique words in the list to the row/col number
            unique_words - List of unique words
            neigh_prob   - NxN Matrix where each row represents a unique word and the value in this colum represents the
                           probability that this word is followed by the word associated with the respective column
    """
    
    unique_words = list(set(word_list))
    num_words_unique = len(unique_words)
    idx_mapping = {word: i for i, word in enumerate(unique_words)}
    neighbours = np.zeros((num_words_unique, num_words_unique), dtype=int)

    curr_word = word_list[0]
    for word in word_list[1:]:
        idx_row = idx_mapping[curr_word]
        idx_col = idx_mapping[word]
        neighbours[idx_row, idx_col] += 1
        curr_word = word
    
    # Convert into probabilities  
    neigh_prob = np.apply_along_axis(lambda row: row/np.sum(row) if np.sum(row)>0 else row, 1, neighbours)
    return idx_mapping, unique_words, neigh_prob


def get_random_sentence(all_words, start_word, max_words): # Create random sentence according to algorithm 
    """ most_frequent_words
    Function that creates a random sentence from a list of words according to the underlying word frequencies
    
    Inputs:
            all_words    - List of words
            start_word   - Word to start with
            max_words    - Number of words the sentence should maximally have (if the algorithm is not stopped by running out of  
                           neighbours)
                        
    Output:
            sent  - Created sentence
    """
    
    curr_word = start_word.lower()
    if curr_word not in all_words:
        sys.exit("Provided starting word not found in text. - Ending script.")
    
    idx_map, unique_words, next_matr = get_neighbour_matrix(all_words)
    
    idx_curr_word = idx_map[curr_word] # Index of current word
    rev_idx_map = {v:k for k, v in idx_map.items()} # Create a map from idx: word
    all_idx = np.arange(len(unique_words)) # Create array with all indexes
    chosen = [idx_curr_word] # List of chosen indexes, beginning with index of start word

    for i in range(max_words):
        probs = next_matr[idx_curr_word, ]

        if np.sum(probs) == 0: # Check if there are any next words, otherwise break
            print("No next words found. - Stop!")
            break

        choice = np.random.choice(all_idx, p=probs) 
        # Note: First tried it with unique words but this is approx. 8x slower than using a numeric array!

        chosen.append(choice) 
        idx_curr_word = choice

    sent = " ".join([rev_idx_map[wrd_id] for wrd_id in chosen]) # Now put evrything together to a string

    return sent



class MissingArgError(Exception): # Define Error for missing file 
    pass


if __name__ == "__main__":   # Check whether script is executed from command line
    
    args = sys.argv
    write_output_to_file = False

    if len(args) < 4: # Arguments are missing
        raise MissingArgError(f"Expected 3 arguments - {len(args)-1} were given.")
        
    elif len(args) == 4: # All arguments are provided
        # now check inputs
        filename = args[1]
        starting_word = args[2]
        max_words = args[3]
        
        if not os.path.isfile(filename): # Check whether file exists
            raise FileNotFoundError(os.strerror(errno.ENOENT), filename)
        
        if not isinstance(starting_word, str): # Check whether word is string
            sys.exit("Provided word is not a string. - Ending script.")
        
        try: # Check whether max_words is int
            max_words = int(max_words)
        except Exception as error:
            print('Provided word count is not an integer. - Ending script.\n' + repr(error))
            
    else: # Too many arguments provided
        sys.exit("Too many arguments were provided. - Ending script.")

        
        
    # If we are here, all inputs are provided and correct
    word_list = np.array(get_word_list(get_string_from_txt(filename)))
    
    sentence = get_random_sentence(word_list, starting_word, max_words)
    
    print(sentence)