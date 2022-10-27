import nltk
import numpy as np
import string
import sys
import regex as re
import os

from collections import Counter
from nltk.tokenize import word_tokenize

FILE_MATCHES = 5
SENTENCE_MATCHES = 1

nltk.download('punkt')
nltk.download('stopwords')

def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    files = dict()

    curr_path = os.path.dirname(os.path.realpath(__file__))
    for document in os.listdir(os.path.join(curr_path,directory)):
        full_path = os.path.join(directory, document)
        with open(full_path, encoding="utf-8") as f:
            files[document] = f.read()

    return files


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    lower_cased = [
        word.lower() for word in word_tokenize(document)
        if re.search('[a-zA-Z]', word) != None
    ]

    non_trivial = filter(lambda word: word not in nltk.corpus.stopwords.words("english"), lower_cased)

    return list(non_trivial)


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """

    total_doc = len(documents)
    idfs, words = dict(), set()

    for document in documents:
        for word in documents[document]:
            words.add(word)
    
    for word in words:
        counter = 0
        for document in documents:
            if word in documents[document]:
                counter += 1
        idfs[word] = np.log(total_doc/counter)

    return idfs
            


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    def rank_files(file):
        sum = 0
        for word in query:
            if word not in files[file]:
                continue
            sum += (files[file].count(word) * idfs[word])
        return sum
    
    return sorted(list(files), key=rank_files, reverse=True)[0:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    def idf(sentence):
        sum = 0
        for word in query:
            if word in sentence:
                sum += idfs[word]
        return sum

    def query_term_density(sentence):
        counter = 0
        for word in sentence:
            if word in query:
                counter += 1
        return counter / len(sentence)

    ranked_sentences = [key for key,item in sorted(
        sentences.items(),
        key=lambda x: (idf(x[1]),query_term_density(x[1])),
        reverse=True
    )]
    
    return ranked_sentences[0:n]
    
    

if __name__ == "__main__":
    main()
