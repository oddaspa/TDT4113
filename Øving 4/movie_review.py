from re import sub # needed for substituting illegal characters
import glob
from operator import itemgetter
from collections import Counter
from math import log
# PART 1 - Reading a single file

# Problem:
# Create a method for reading a document of training set from a file,
# then representing it in a filtered order only containing unique words.

counter = 0
class Review():

    def __init__(self, n_gram):
        print("Importing stop words...")
        # importing the stop words used for removing unusable words
        stop_file = open("data/stop_words.txt", "r", encoding="utf-8")
        stop_str = stop_file.read().lower()
        stop_file.close()
        self.stop_words = stop_str
        self.n_gram = n_gram

    # Import a file and filter the output
    def read_file(self, input_filename):
        # Open file
        file_content = open(input_filename, encoding = 'utf-8')

        # read file
        review = file_content.read().lower()
        file_content.close()

        # removes illegal characters and splits into list
        review_words = sub('[^0-9a-zA-Z]+', ' ', review).split()

        # removes duplicates
        review_words = set(review_words)

        # Part 6 of assignment (N-gram)
        # NB! Taken out in part 7
        #n_grams = n_gram(review_words, 2)

        # Part 3 of assignment (see below)
        clean_review = self.remove_stop_words(review_words, self.stop_words)

        return clean_review

    #PART 2 - Read all files

    # Problem:
    # Expand the code to read all files in the training set. Analyze the representation
    # and find the 25 most frequent words for positive and negative reviews.


    def read_all_files(self):
        # importing the negative and positive reviews that was handed out in the assignment
        print("Importing training data...")
        negative_review_list = glob.glob("data/subset/train/neg/*.txt")
        positive_review_list = glob.glob("data/subset/train/pos/*.txt")
        # removing stop words ( Part 3 )

        length_of_reviews = (len(positive_review_list),(len(negative_review_list)))

        # using helper(below) to create a dictionary with 25 most frequent words and their value
        all_positive_words = self.counting_number_of_words(positive_review_list)
        all_negative_words = self.counting_number_of_words(negative_review_list)

        # filter the most informative words
        most_informative_pos, most_informative_neg, pos_vocabulary, neg_vocabulary = self.most_informative_words(all_positive_words,all_negative_words, length_of_reviews )

        # Vocabulary for testing data
        self.pos_vocabulary = pos_vocabulary
        self.neg_vocabulary = neg_vocabulary

        # return two list of the most frequent words
        return list(most_informative_pos), list(most_informative_neg)


    # helper for part 2 - Analyzing most frequent words in review
    def counting_number_of_words(self,list_of_reviews):
        all_words = {}
        for review in list_of_reviews:
            # words_in_review is a list of unique words in a specific review
            words_in_review = self.read_file(review)
            for word in words_in_review:
                # add the word to a dictionary or +1 the value of that word
                if word not in all_words and word is not None:
                    all_words[word] = 1
                elif word is not None:
                    all_words[word] += 1

        # sorting the dictionary and exctracting the 25 words with highest frequency
        # words = dict(sorted(all_words.items(), key=operator.itemgetter(1), reverse=True)[:25])
        # NB! Had to remove the filter when starting part 5.

        # we create a dictionary for all the words to test the test files
        words = all_words
        return words


    #PART 3 - Clean review

    # Problem:
    # Expand the system to remove all stop words (found in the data set under ./data/stop-words.txt)
    # from the representation of the reviews. Find the most frequent words after the stop words are
    # removed.

    def remove_stop_words(self,review, stop_words):
        clean_review = set([word for word in review if word not in stop_words])
        return clean_review

    #PART 4 -  Filter noninformative words

    # Problem:
    # Further expand the system to find the information value of a word.
    # Print the 25 most informative words for both positive and negative reviews.
    # NB! The information value is (Number of positive reviews with <word> / number of reviews total with the <word>).

    def most_informative_words(self,pos_list_dict,neg_list_dict, length_of_reviews):
        # merging the 2 dictionaries and adding their value by casting them to a counter (subclass of dict)
        pos_counter = Counter(pos_list_dict)
        neg_counter = Counter(neg_list_dict)
        all_words = pos_counter + neg_counter

        pos_length, neg_length = length_of_reviews
        total_number_of_reviews = pos_length + neg_length

        pos_inf_dict, neg_inf_dict, pos_pop_dict, neg_pop_dict  = {}, {}, {}, {}

        for word in all_words:
            # Updating the value of our all words

            # Part 5 - prune words
            if all_words[word] / total_number_of_reviews < 0.01: # Pruning increases correctness?
                pos_list_dict.pop(word,None)
                neg_list_dict.pop(word,None)

        for word in pos_list_dict:
            pos_inf_dict[word] = pos_list_dict[word] / all_words[word]
            pos_pop_dict[word] = pos_list_dict[word] / pos_length
        for word in neg_list_dict:
            neg_inf_dict[word] = neg_list_dict[word] / all_words[word]
            neg_pop_dict[word] = neg_list_dict[word] / neg_length

        # save the most informative words to a list
        most_informative_pos = dict(sorted(pos_inf_dict.items(), key=itemgetter(1), reverse=True)[:25])
        #print("POS: " + str(most_informative_pos))

        most_informative_neg = dict(sorted(neg_inf_dict.items(), key=itemgetter(1), reverse=True)[:25])
        #print("NEG: " + str(most_informative_neg))

        # returns the 25 most informative words and a dictionary the informative value of all words
        return most_informative_pos , most_informative_neg, pos_inf_dict, neg_inf_dict

    # PART 5 - Implement pruning

    #Problem:
    # Implement pruning at a given percentage and generate the reviews.

    #Tip:
    # Be ware that the share of total reviews defines if a word
    # should be pruned away or not.
        ################################ UPDATE LATER ##########################
    # soulution see line 120 and 136


    # PART 6 - N-gram words
    def n_gram(self, review,n):
        review_list = list(review)
        for i in range(0,len(review_list)-1,n-1):
            review_list.append("_".join(review_list[i : i+n]))
        return review_list

    # Part 7 - Classification

    # Problem:
    # Implement the classification system. System must first be train by the training data
    # and compute the frequency of the words. Then create a method to import testing data
    # and classify them as either positive or negative. In this part only use words that
    # are at least in 2% of the documents and remove stop words. PS! It is not necessary to
    # create n-grams.

    # test_data uses the file_list to attempt to see if the review are positive or negative
    # depending on the words in the review

    def test_data(self, file_list):
        if "pos" in file_list[0]:
            list_type = "Type Positive"
        else:
            list_type = "Type Negative"

        guess_pos_review, guess_neg_review = 0, 0
        print("Reading testfile: " + str(list_type))

        for file in file_list:
            current_review = self.read_file(file)
            pos_value, neg_value = 0, 0

            for word in current_review:
                # increasing the score of positive and negative value
                pos_value += self.get_score(self.pos_vocabulary, word)
                neg_value += self.get_score(self.neg_vocabulary, word)

            # appending guess to variable
            if pos_value > neg_value:
                guess_pos_review += 1
            else:
                guess_neg_review += 1

        # Error test
        if list_type == "Type Positive" and pos_value < neg_value:
            print("This is the probability value of the pos_value: " + str(pos_value))
            print("This is the probability value of the neg_value: " + str(neg_value))

        if list_type == "Type Negative" and pos_value > neg_value:
            print("This is the probability value of the pos_value: " + str(pos_value))
            print("This is the probability value of the neg_value: " + str(neg_value))

        # see how many we got right depending on the test type
        if list_type == "Type Positive":
            return guess_pos_review / len(file_list)
        else:
            return guess_neg_review / len(file_list)

    # Helper to create a logarithmic value of the frequency of the word
    # NB! If word is not in vocabulary the corresponding value gets "punished"
    # by adding log(0.01) to the value
    def get_score(self, vocab,word):
        try:
            return log(vocab[word])
        except KeyError:
            return log(0.01)




    # helper progressbar
    def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
        """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
        """
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
        # Print New Line on Complete
        if iteration == total:
            print()

# Testing system
print("Starting Movie Review system")

# Constructor
review = Review(2)

# Importing training files and creating vocabulary
pos_words, neg_words = review.read_all_files()

# Tracking test files
pos_test_list = glob.glob("data/subset/test/pos/*.txt")
neg_test_list = glob.glob("data/subset/test/neg/*.txt")

# testing test data
pos = review.test_data(pos_test_list)
print("Percentage correct: " + str(pos) + "%")
neg = review.test_data(neg_test_list)
print("Percentage correct: " + str(neg) + "%")

# printing result
print("Total: " + str((pos + neg) / 2) + "%")

