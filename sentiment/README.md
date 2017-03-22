## IMDB datasets

http://ai.stanford.edu/~amaas/data/sentiment/

## Guidelines

```
# Generate data/train.txt + data/test.txt
$ python imdb_preprocess.py

# Train text classification model (with FastText + data/train.txt)
# Generate an imdb.bin model
$ ./train.sh

# Evaluate above model
$ ./evaluate.sh

# Sentiment testing
$ ./predict.sh test_review.txt
```
