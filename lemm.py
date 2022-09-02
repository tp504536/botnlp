# import string
#
# import pymorphy2
# from model import date
# import nltk
# morph = pymorphy2.MorphAnalyzer()
# ourClasses = []
# newWords = []
# documentX = []
# documentY = []
# finalWords = []
# for intent in date['intents']:
#     for pattern in intent["patterns"]:
#         ournewTkns = nltk.word_tokenize(pattern)  # tokenize the patterns
#         newWords.extend(ournewTkns)  # extends the tokens
#         documentX.append(pattern)
#         documentY.append(intent["tag"])
#
#     if intent["tag"] not in ourClasses:  # add unexisting tags to their respective classes
#         ourClasses.append(intent["tag"])
# for word in newWords:
#     pars = morph.parse(word.lower())[0]
#     finalWords.append(pars.normal_form)
# print(finalWords)

# newWords = [morph.parse(word.lower()) for word in newWords if word not in string.punctuation]
# newWords = morph.parse(newWords)[0].normal_form
