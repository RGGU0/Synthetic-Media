# -*- coding: utf-8 -*-
"""3 СинтМедиа Генерация текста в стиле Эзопа.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xHDM9eJhPseqyrt03yviEupytl9rAbDo
"""

from google.colab import drive
drive.mount('/content/drive')

#!pip install np_utils

import numpy as np
import re
from IPython.display import clear_output

from keras.layers import Dense, LSTM, Input, Embedding, Dropout
#from keras.utils import np_utils
from keras.utils import to_categorical
from keras.models import Model, load_model
from keras.optimizers import Adam, RMSprop
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer
from keras.callbacks import LambdaCallback

!pip install clearml

import pandas as pd
import numpy as np
from clearml import Task, Logger
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, ParameterSampler
#from catboost import CatBoostClassifier, Pool
from sklearn.metrics import roc_auc_score

# Commented out IPython magic to ensure Python compatibility.
# %env CLEARML_WEB_HOST=https://app.clear.ml
# %env CLEARML_API_HOST=https://api.clear.ml
# %env CLEARML_FILES_HOST=https://files.clear.ml
# %env CLEARML_API_ACCESS_KEY=OFCDKC4C1S6MO19CJU14
# %env CLEARML_API_SECRET_KEY=hBNiLBTbT60djVQXlGmQR6V3qSwjWNbRugtHspRS9xyPLJTFYW

task = Task.init(
    project_name='Aesop',
    task_name='TextGeneration',
    tags=['TextGeneration','keras','LSTM'])

import keras

load_saved_model = False
train_model = False

token_type = 'word'

"""

---

"""

import os

#os.system('TextDownloader.sh 21 aesop' )

sh = """
FILE=$1
NAME=$2
echo FILE
echo NAME
URL=http://www.gutenberg.org/cache/epub/$FILE/pg$FILE.txt
TARGET_DIR=./data/$NAME/
mkdir $TARGET_DIR
TXT_FILE=./data/$NAME/data.txt
wget -N $URL -O $TXT_FILE
"""
with open('script.sh', 'w') as file:
  file.write(sh)

!bash script.sh 21 aesop

"""

---

"""

#load in the text and perform some cleanup

seq_length = 20

filename = "./data/aesop/data.txt"

with open(filename, encoding='utf-8-sig') as f:
    text = f.read()

#removing text before and after the main stories
start = text.find("the wolf and the lamb")
end = text.find("footnotes")
text = text[start:end]

start_story = '| ' * seq_length

text = start_story + text
text = text.lower()
text = text.replace('\n\n\n\n\n', start_story)
text = text.replace('\n', ' ')
text = text.replace('"', ' ')
text = text.replace(' ,', '')
text = text.replace('“', '').replace('”', '')
text = re.sub('  +', '. ', text).strip()
text = text.replace('..', '.')

text = re.sub('([!"“”#$%&()*+,,-./:;<=>?@[\]^_`{|}~])', r' \1 ', text)
text = re.sub('\s{2,}', ' ', text)

text

if token_type == 'word':
    tokenizer = Tokenizer(char_level = False, filters = '')
else:
    tokenizer = Tokenizer(char_level = True, filters = '', lower = False)


tokenizer.fit_on_texts([text])

total_words = len(tokenizer.word_index) + 1

token_list = tokenizer.texts_to_sequences([text])[0]

total_words

print(tokenizer.word_index)
print(token_list)

import keras

def generate_sequences(token_list, step):

    X = []
    y = []

    for i in range(0, len(token_list) - seq_length, step):
        X.append(token_list[i: i + seq_length])
        y.append(token_list[i + seq_length])


    y = keras.utils.to_categorical(y, num_classes = total_words)


    num_seq = len(X)
    print('Number of sequences:', num_seq, "\n")

    return X, y, num_seq

step = 1
seq_length = 20

X, y, num_seq = generate_sequences(token_list, step)

X = np.array(X)
y = np.array(y)

X.shape

y.shape

"""## Define the LSTM model"""

if load_saved_model:
    # model = load_model('./saved_models/lstm_aesop_1.h5')
    model = load_model('./saved_models/aesop_dropout_100.h5')

else:

    n_units = 256
    embedding_size = 100

    text_in = Input(shape = (None,))
    embedding = Embedding(total_words, embedding_size)
    x = embedding(text_in)
    x = LSTM(n_units)(x)
    x = Dropout(0.15)(x)
    text_out = Dense(total_words, activation = 'softmax')(x)

    model = Model(text_in, text_out)

    opti = RMSprop(lr = 0.001)
    model.compile(loss='categorical_crossentropy',
                  optimizer=opti,
                  metrics=['AUC','Precision','Recall']
                  )

model.summary()

def sample_with_temp(preds, temperature=1.0):
    # helper function to sample an index from a probability array
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)



def generate_text(seed_text, next_words, model, max_sequence_len, temp):
    output_text = seed_text

    seed_text = start_story + seed_text

    for _ in range(next_words):
        token_list = tokenizer.texts_to_sequences([seed_text])[0]
        token_list = token_list[-max_sequence_len:]
        token_list = np.reshape(token_list, (1, max_sequence_len))

        probs = model.predict(token_list, verbose=0)[0]
        y_class = sample_with_temp(probs, temperature = temp)

        if y_class == 0:
            output_word = ''
        else:
            output_word = tokenizer.index_word[y_class]

        if output_word == "|":
            break

        if token_type == 'word':
            output_text += output_word + ' '
            seed_text += output_word + ' '
        else:
            output_text += output_word + ' '
            seed_text += output_word + ' '


    return output_text

#log = Logger.current_logger()

train_model = True

def on_epoch_end(epoch, logs):
    seed_text = ""
    gen_words = 500

    print('Temp 0.2')
    print (generate_text(seed_text, gen_words, model, seq_length, temp = 0.2))
    print('Temp 0.33')
    print (generate_text(seed_text, gen_words, model, seq_length, temp = 0.33))
    print('Temp 0.5')
    print (generate_text(seed_text, gen_words, model, seq_length, temp = 0.5))
    print('Temp 1.0')
    print (generate_text(seed_text, gen_words, model, seq_length, temp = 1))



if train_model:
    epochs = 13
    batch_size = 32
    num_batches = int(len(X) / batch_size)
    callback = LambdaCallback(on_epoch_end=on_epoch_end)
    history = model.fit(X, y, epochs=epochs, validation_split=0.1, batch_size=batch_size, callbacks = [callback], shuffle = True,  verbose=2)

model.history.history.keys()

logger = task.get_logger()

for i in range(len(model.history.history['loss'])):
    logger.report_scalar("loss_d15", "train", iteration=i, value=model.history.history['loss'][i])
    logger.report_scalar("loss_d15", "test", iteration=i, value=model.history.history['val_loss'][i])
    logger.report_scalar("auc_d15", "train", iteration=i, value=model.history.history['auc'][i])
    logger.report_scalar("auc_d15", "test", iteration=i, value=model.history.history['val_auc'][i])
    logger.report_scalar("precision_d15", "train", iteration=i, value=model.history.history['precision'][i])
    logger.report_scalar("precision_d15", "test", iteration=i, value=model.history.history['val_precision'][i])
    logger.report_scalar("recall_d15", "train", iteration=i, value=model.history.history['recall'][i])
    logger.report_scalar("recall_d15", "test", iteration=i, value=model.history.history['val_recall'][i])
logger.flush()

model.save_weights('/content/drive/MyDrive/h5/my_model_weights_d15.h5')

model.summary()

def inferens(input_text, len):
  temp = 0.1
  print (generate_text(input_text, len, model, seq_length, temp))

inferens('One day the cat and ', 100)

#model.save('/content/drive/MyDrive/SyntheticMedia/TextGen/aesop_model.h5')