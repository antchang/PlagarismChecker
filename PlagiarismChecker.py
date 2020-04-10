import math


def clean_text(txt):
    """returns a list containing words in txt after punctuation has been
    removed"""

    txt = txt.lower()
    txt = txt.replace(',', '').replace('.', '').replace('!', '').replace('\n', '').replace('?', '')
    return txt.split()


def sample_file_write(filename):
    """A function that demonstrates how to write a
       Python dictionary to an easily-readable file.
    """
    d = {'test': 1, 'foo': 42}   # Create a sample dictionary.
    f = open(filename, 'w')      # Open file for writing.
    f.write(str(d))              # Writes the dictionary to the file.
    f.close()                    # Close the file.


def sample_file_read(filename):
    """A function that demonstrates how to read a
       Python dictionary from a file.
    """
    f = open(filename, 'r')    # Open for reading.
    d_str = f.read()           # Read in a string that represents a dict.
    f.close()

    d = dict(eval(d_str))      # Convert the string to a dictionary.

    print("Inside the newly-read dictionary, d, we have:")
    print(d)


def stem(s):
    """ that accepts a string as a parameter. The function
        should then return the stem of s. The stem of a word
        is the root part of the word, which excludes any
        prefixes and suffixes
    """
    if len(s) == 1:
        return s
    if s[-1] == 's' and s[-2] not in 'aeious':
        s = s[:-1]
    if s[-3:] == 'ing':
        if s[-5:-3] not in ['bb' 'dd' 'ff' 'gg' 'mm' 'nn' 'pp' 'rr' 'tt']:
            s = s[:-3]
        else:
            s = s[:-4]
    if s[-2:] == 'ed' and s[-3] not in 'aeiou':
        s = s[:-2]
    if s[-2:] == 'er' and len(s) > 5:
        s = s[:-2]
    if s[-2:] == 'es' and len(s) > 5:
        s = s[:-2]
    if s[-4:] == 'ness':
        s = s[:-4]
    if s[-3:] == 'ful':
        s = s[:-3]
    if s[-4:] == 'able':
        s = s[:-4]
    if s[-2:]== 'al':
        s = s[:-2]
    if s[-3:] == 'ize':
        s = s[:-3]
    return s


def compare_dictionaries(d1, d2):
    """computes and returns log-similarity score of two dictionaries"""

    score = 0
    total = 0

    for key in d1:
        total += d1[key]

    for item in d2:
        if item in d1:
            score += d2[item] * math.log(d1[item]/total)
        else:
            score += d2[item] * math.log(.5/total)
    return score



class TextModel:

    def __init__(self, model_name):
        """constructs new TextModel object"""

        self.name = model_name
        self.words = {}
        self.word_lengths = {}
        self.stems = {}
        self.sentence_lengths = {}
        self.punctuation = {}

    def __repr__(self):
        """returns string that includes name, model, and dictionary sizes"""

        s = 'text model name: ' + self.name + '\n'
        s += '  number of words: ' + str(len(self.words)) + '\n'
        s += "  number of word lengths: " + str(len(self.word_lengths)) + '\n'
        s += "  number of stems: " + str(len(self.stems)) + '\n'
        s += "  number of sentence lengths: " + str(len(self.sentence_lengths)) + '\n'
        s += "  number of different punctuation: " + str(len(self.punctuation))
        return s

    def add_string(self, s):
        """ Analyzes the string txt and adds its pieces
            to all of the dictionaries in this text model."""

        sen_length = 0
        for x in s:
            if x == ' ':
                sen_length += 1
            else:
                if x in '.?!':
                    sen_length += 1
                    if sen_length not in self.sentence_lengths:
                        self.sentence_lengths[sen_length] = 1
                    else:
                        self.sentence_lengths[sen_length] += 1
                    sen_length = 0

        for punct in s:
            if punct in '.?!':
                if punct not in self.punctuation:
                    self.punctuation[punct] = 1
                else:
                    self.punctuation[punct] += 1

        word_list = clean_text(s)

        for word in word_list:
            if word not in self.words:
                self.words[word] = 1
            else:
                self.words[word] += 1

        for word in word_list:
            if len(word) not in self.word_lengths:
                self.word_lengths[len(word)] = 1
            else:
                self.word_lengths[len(word)] += 1

        for word in word_list:
            word = stem(word)
            if word not in self.stems:
                self.stems[word] = 1
            else:
                self.stems[word] += 1

    def add_file(self, filename):
        """ that adds all of the text in the file identified by
            filename to the model. It should not explicitly return a value."""

        file = open(filename, 'r', encoding='utf8', errors='ignore')
        text = file.read()
        file.close()

        self.add_string(text)

    def save_model(self):
        """ that saves the TextModel object self by writing its
            various feature dictionaries to files.
            There will be one file written for each feature dictionary."""

        words_dict = open(self.name + '_' + 'words', 'w')
        words_dict.write(str(self.words))
        
        word_lengths_dict = open(self.name + "_" + "word_lengths", 'w')
        word_lengths_dict.write(str(self.word_lengths))
        
        words_dict.close()
        word_lengths_dict.close()

    def read_model(self):
        """ reads the stored dictionaries for the called TextModel
            objects from their files and assigns them to the attributes
            of the called TextModel"""

        read_words = open(self.name + '_' + 'words', 'r')
        dict_words = read_words.read()
        read_words.close()

        self.words = dict(eval(dict_words))

        read_word_lengths = open(self.name + '_' + 'word_lengths', 'r')
        dict_word_lengths = read_word_lengths.read()
        read_word_lengths.close()

        self.word_lengths = dict(eval(dict_word_lengths))

    def similarity_scores(self, other):
        """return list of log similarity scores """

        word_score = compare_dictionaries(other.words, self.words)
        word_length = compare_dictionaries(other.word_lengths, self.word_lengths)
        stems = compare_dictionaries(other.stems, self.stems)
        sentence_length = compare_dictionaries(other.sentence_lengths, self.sentence_lengths)
        punctuation = compare_dictionaries(other.punctuation, self.punctuation)

        return [word_score, word_length, stems, sentence_length, punctuation]

    def classify(self, source1, source2):
        """compares the called TextModel object to two other source TextModel objects """

        scores1 = self.similarity_scores(source1)
        scores2 = self.similarity_scores(source2)

        print("score for " + source1.name + ': ' + str(scores1))
        print("score for " + source2.name + ': ' + str(scores2))

        weighted_sum1 = 10 * scores1[0] + 5 * scores1[1] + 7 * scores1[2] + 3 * scores1[3] + scores1[4]
        weighted_sum2 = 10 * scores2[0] + 5 * scores2[1] + 7 * scores2[2] + 3 * scores2[3] + scores2[4]

        if weighted_sum1 > weighted_sum2:
            print(self.name + " is more likely to have come from " + source1.name)
        else:
            print(self.name + " is more likely to have come from " + source2.name)

