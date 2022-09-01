import json
import string
import nltk
import numpy as np
import random
from nltk.stem import WordNetLemmatizer
import tensorflow
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Dropout

nltk.download("punkt")  # required package for tokenization
nltk.download("wordnet")  # word database
nltk.download('omw-1.4')

date = json.load(open('test1.json'))

lm = WordNetLemmatizer()
# lists
ourClasses = []
newWords = []
documentX = []
documentY = []

for intent in date['intents']:
    for pattern in intent["patterns"]:
        ournewTkns = nltk.word_tokenize(pattern)  # tokenize the patterns
        newWords.extend(ournewTkns)  # extends the tokens
        documentX.append(pattern)
        documentY.append(intent["tag"])

    if intent["tag"] not in ourClasses:  # add unexisting tags to their respective classes
        ourClasses.append(intent["tag"])

newWords = [lm.lemmatize(word.lower()) for word in newWords if
            word not in string.punctuation]  # set words to lowercase if not in punctuation
newWords = sorted(set(newWords))  # sorting words
ourClasses = sorted(set(ourClasses))  # sorting classes

trainingData = []  # training list array
outEmpty = [0] * len(ourClasses)
# bow model
for idx, doc in enumerate(documentX):
    bagOfwords = []
    text = lm.lemmatize(doc.lower())
    for word in newWords:
        bagOfwords.append(1) if word in text else bagOfwords.append(0)

    outputRow = list(outEmpty)
    outputRow[ourClasses.index(documentY[idx])] = 1
    trainingData.append([bagOfwords, outputRow])

random.shuffle(trainingData)
trainingData = np.array(trainingData, dtype=object)  # coverting our data into an array afterv shuffling

x = np.array(list(trainingData[:, 0]))  # first trainig phase
y = np.array(list(trainingData[:, 1]))  # second training phase

iShape = (len(x[0]),)
oShape = len(y[0])
# parameter definition
ourNewModel = Sequential()
# In the case of a simple stack of layers, a Sequential model is appropriate

# Dense function adds an output layer
ourNewModel.add(Dense(128, input_shape=iShape, activation="relu"))
# The activation function in a neural network is in charge of converting the node's summed weighted input into activation of the node or output for the input in question
ourNewModel.add(Dropout(0.5))
# Dropout is used to enhance visual perception of input neurons
ourNewModel.add(Dense(64, activation="relu"))
ourNewModel.add(Dropout(0.3))
ourNewModel.add(Dense(oShape, activation="softmax"))
# below is a callable that returns the value to be used with no arguments
md = tensorflow.keras.optimizers.Adam(learning_rate=0.01, decay=1e-6)
# Below line improves the numerical stability and pushes the computation of the probability distribution into the categorical crossentropy loss function.
ourNewModel.compile(loss='categorical_crossentropy',
                    optimizer=md,
                    metrics=["accuracy"])
# Output the model in summary
print(ourNewModel.summary())
# Whilst training your Nural Network, you have the option of making the output verbose or simple.
ourNewModel.fit(x, y, epochs=200, verbose=1)
# By epochs, we mean the number of times you repeat a training set.
ourNewModel.save('model')

load_model = tensorflow.keras.models.load_model('model')


def clean(sentence):
    sentence = sentence.lower()
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lm.lemmatize(word) for word in sentence_words]
    return sentence_words


def bag_of_words(sentence):
    sentence_words = clean(sentence)
    bag = [0] * len(newWords)
    for w in sentence_words:
        for i, word in enumerate(newWords):
            if word == w:
                bag[i] = 1
    return np.array(bag)


def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = load_model.predict(np.array([bow]))[0]
    error_threshold = 0.10
    result = [[i, r] for i, r in enumerate(res) if r > error_threshold]
    result.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in result:
        return_list.append({'intent': ourClasses[r[0]], 'probability': str(r[1])})
    return return_list


def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            return result

# while True:
#     message = input()
#     ints = predict_class(message)
#     print(type(ints[0]['probability']))
#     if float(ints[0]['probability']) < 0.86:
#         print('я тебя не понял')
#     else:
#         res = get_response(ints, date)
#         print(res)
