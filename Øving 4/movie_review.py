from re import sub # needed for substituting illegal characters
import glob
import operator
from collections import Counter
# PART 1 - Reading a single file

# Problem:
# Create a method for reading a document of training set from a file,
# then representing it in a filtered order only containing unique words.


# Import a file and filter the output
def read_file(input_filename, stop_words):
    # Open file
    file_content = open(input_filename, encoding = 'utf-8')

    # read file
    review = file_content.read().lower()
    file_content.close()

    # removes illegal characters and splits into list
    review_words = sub('[^0-9a-zA-Z]+', ' ', review).split()

    # removes duplicates
    review_words = set(review_words)

    # Part 3 of assignment (see below)
    clean_review = remove_stop_words(review_words, stop_words)

    return clean_review

#PART 2 - Read all files

# Problem:
# Expand the code to read all files in the training set. Analyze the representation
# and find the 25 most frequent words for positive and negative reviews.


def read_all_files():
    # importing the stop words used for removing unusable words
    stop_words_file = open("data/stop_words.txt")
    stop_words = stop_words_file.read().split()
    stop_words_file.close()
    stop_words = set(stop_words)

    # importing the negative and positive reviews that was handed out in the assignment
    negative_review_list = glob.glob("data/alle/train/neg/*.txt")
    positive_review_list = glob.glob("data/alle/train/pos/*.txt")

    # removing stop words ( Part 3 )


    total_number_of_reviews = len(negative_review_list) + len(positive_review_list)


    # using helper(below) to create a dictionary with 25 most frequent words and their value
    most_frequent_positive_words = counting_number_of_words(positive_review_list,stop_words)
    most_frequent_negative_words = counting_number_of_words(negative_review_list,stop_words)

    # filter the most informative words
    most_informative_pos, most_informative_neg = most_informative_words(most_frequent_positive_words,most_frequent_negative_words)

    # return two list of the most frequent words
    return list(most_informative_pos), list(most_informative_neg)


# helper for part 2 - Analyzing most frequent words in review
def counting_number_of_words(list_of_reviews, stop_words):
    all_words = {}
    for review in list_of_reviews:
         #words_in_review is a list of unique words in a specific review
        words_in_review = read_file(review, stop_words)
        for word in words_in_review:
            # add the word to a dictionary or +1 the value of that word
            if word not in all_words and word is not None:
                all_words[word] = 1
            elif word is not None:
                all_words[word] += 1

    # sorting the dictionary and exctracting the 25 words with highest frequency
    # words = dict(sorted(all_words.items(), key=operator.itemgetter(1), reverse=True)[:25])
    # NB! Had to remove the filter when starting part 5.

    words = all_words
    return words


#PART 3 - Read all files

# Problem:
# Expand the system to remove all stop words (found in the data set under ./data/stop-words.txt)
# from the representation of the reviews. Find the most frequent words after the stop words are
# removed.

def remove_stop_words(review, stop_words):
    clean_review = set([word for word in review if word not in stop_words])
    return clean_review

#PART 4 -  Filter noninformative words

# Problem:
# Further expand the system to find the information value of a word.
# Print the 25 most informative words for both positive and negative reviews.
# NB! The information value is (Number of positive reviews with <word> / number of reviews total with the <word>).

def most_informative_words(pos_list_dict,neg_list_dict):
    # merging the 2 dictionaries and adding their value by casting them to a counter (subclass of dict)
    pos_counter = Counter(pos_list_dict)
    neg_counter = Counter(neg_list_dict)
    all_words = pos_counter + neg_counter
    most_informative_pos, most_informative_neg = {}, {}

    # prune limit (value of all words)
    sum_of_words = sum(all_words.values())
    print(sum_of_words)

    for word in pos_list_dict:
        # Updating the value of our all words

        # Part 5 - prune words
        if pos_list_dict[word] / sum_of_words> 0.05:
            all_words[word] = pos_list_dict[word] / all_words[word]
        else:
            all_words[word] = -1


    # save the most informative words to a list
    most_informative_pos = dict(sorted(all_words.items(), key=operator.itemgetter(1), reverse=True)[:25])

    # reset the dictionary
    all_words = pos_counter + neg_counter

    for word in neg_list_dict:
        # Updating the value of our all words

        # Part 5 - prune words
        if neg_list_dict[word] / sum_of_words > 0.05:
            all_words[word] = neg_list_dict[word] / all_words[word]
        else:
            all_words[word] = -1
        # save the most informative words to a list
    most_informative_neg = dict(sorted(all_words.items(), key=operator.itemgetter(1), reverse=True)[:25])

    return most_informative_pos , most_informative_neg

# PART 5 - Implement pruning

#Problem:
# Implement pruning at a given percentage and generate the reviews.

#Tip:
# Be ware that the share of total reviews defines if a word
# should be pruned away or not.

# soulution see line 120 and 136


# PART 6 - N-gram words


def main():
    print("lets go")
    pos_words, neg_words = read_all_files()
    print("POSITIVE WORDS:")
    print(pos_words)
    print("NEGATIVE WORDS:")
    print(neg_words)
main()