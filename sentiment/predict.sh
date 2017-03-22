echo `cat $1`

if [ `fasttext predict imdb.bin $1` == '__label__0' ]; then
    echo "-> Positive"
else
    echo "-> Negative"
fi
