# This program concat IMDB dataset reviews into a single files
# and label it with 0 (positive) and 1 (negative) sentiment
#
# E.g:
#   __label__0, Bromwell High is a cartoon comedy...
#   __label__1, Story of a man who has unnatural feelings for a pig...
#

import os

# Variables config
#
# Data directory's structure:
#   pos/*.txt (positive reviews)
#   neg/*.txt (negative reviews)
#
train_dir = "/home/hiepph/Data/Text/IMDB/aclImdb/train/"
test_dir = "/home/hiepph/Data/Text/IMDB/aclImdb/test/"

# Positive
def pos_process(d, f):
    pos_dir = os.path.join(d, "pos")
    count = 0
    for filename in os.listdir(pos_dir):
        re = open(os.path.join(pos_dir, filename), "r").read()
        f.write('__label__0 , ' + re + '\n')

        count += 1

    print("Produced %d positive reviews" % count)


# Negative
def neg_process(d, f):
    neg_dir = os.path.join(d, "neg")
    count = 0
    for filename in os.listdir(neg_dir):
        re = open(os.path.join(neg_dir, filename), "r").read()
        f.write('__label__1 , ' + re + '\n')

        count += 1

    print("Produced %d negative reviews" % count)



# Make a train file for fastText
train_file = 'data/train.txt'
try:
    with open(train_file) as f:
        print("Overwrite train file!")
except FileNotFoundError:
    open(train_file, 'w').close()

# Process data and produce train files
train = open(train_file, 'w')
pos_process(train_dir, train)
neg_process(train_dir, train)
train.close

# Same for test file
test_file = 'data/test.txt'
try:
    with open(test_file) as f:
        print("Overwrite test file!")
except FileNotFoundError:
    open(test_file, 'w').close()

test = open(test_file, 'w')
pos_process(test_dir, test)
neg_process(test_dir, test)
test.close
