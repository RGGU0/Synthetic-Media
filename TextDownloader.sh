FILE=$1
NAME=$2
echo FILE
echo NAME
URL=http://www.gutenberg.org/cache/epub/$FILE/pg$FILE.txt
TARGET_DIR=./data/$NAME/
mkdir $TARGET_DIR
TXT_FILE=./data/$NAME/data.txt
wget -N $URL -O $TXT_FILE