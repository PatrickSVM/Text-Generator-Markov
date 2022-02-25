# Text_Generator_Markov

Implementation of a simple Markov Chain Text Generator as part of a project for one of my courses at LiU.

## Usage
Both scripts can either be imported as modules to access their functions (as shown in the Jupyter Notebook file) or can be run directly from the command line. If run from the command line, the following instructions can be followed:

 ```console
foo@bar:~$ text_stats.py <txt_file> <output_file>
```
where the last argument is just optional. If provided the output is not printed but rather stored in the provided file.

 ```console
 foo@bar:~$ generate_text.py <txt_file> <starting_word> <max_words>
 ```
 where the first argument specifies the word to start with and the second argument the number of words to be generated.
