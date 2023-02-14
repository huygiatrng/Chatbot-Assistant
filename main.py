# import necessary libraries
import nltk
from nltk.stem import WordNetLemmatizer
import json
import pickle
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD
import random

# initialize lemmatizer
lemmatizer = WordNetLemmatizer()

# initialize empty lists
words = []
classes = []
documents = []
ignore_words = ['?', '!']

# load data from JSON file
data_file = open('intents.json').read()
intents = json.loads(data_file)

# tokenize each pattern and add to words list, add to documents list as tuple (pattern, tag), and add unique tag to classes list
for intent in intents['intents']:
    for pattern in intent['patterns']:
        w = nltk.word_tokenize(pattern)
        words.extend(w)
        documents.append((w, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# lemmatize and remove duplicates from words list, and sort classes and words lists
words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]
words = sorted(list(set(words)))
classes = sorted(list(set(classes)))

# print length of documents, classes, and words lists
print(len(documents), "documents")
print(len(classes), "classes", classes)
print(len(words), "unique lemmatized words", words)

# save words and classes lists to pickle files
pickle.dump(words,open('words.pkl','wb'))
pickle.dump(classes,open('classes.pkl','wb'))

# create an empty array for our output and training set
output_empty = [0] * len(classes)
training = []

# create bag of words for each pattern and add to training set
for doc in documents:
    bag = [0] * len(words)
    pattern_words = doc[0]
    pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]
    for w in pattern_words:
        if w in words:
            bag[words.index(w)] = 1
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1
    training.append([bag, output_row])

# pad all bag arrays with zeros to make them the same length
max_len = max([len(x[0]) for x in training])
for i in range(len(training)):
    bag = training[i][0]
    padding = [0] * (max_len - len(bag))
    training[i][0] = bag + padding

# convert training list to a NumPy array and shuffle the rows
np.random.shuffle(training)
training = np.array(training, dtype=object)

# split train_x and train_y from training set
train_x = list(training[:,0])
train_y = list(training[:,1])

# create a Sequential model with 3 layers, compile it with stochastic gradient descent and Nesterov accelerated gradient, and fit the model to the training data
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))
sgd = SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
model.save('chatbot_model.h5', hist)
print("model created")