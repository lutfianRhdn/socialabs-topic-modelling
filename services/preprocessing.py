import re
import pandas as pd
import nltk
import string
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords')
english_stopwords = set(stopwords.words('english'))

class Preprocessing:
    def __init__(self, tweet):
        self.data = tweet
        self.data = self.case_folding(self.data)
        self.data = self.cleaning(self.data)
        self.data = self.tokenizing(self.data)
        self.data = self.normalization(self.data)
        # self.data = self.steaming(self.data)
        self.data = self.stopword_removal(self.data)

    def get_data(self):
        return self.data

    def case_folding(self, tweets):
        return [str(tweet).lower() for tweet in tweets]

    def cleaning(self, tweets):
        res = []
        sequencePattern   = r'([A-Za-z])\1{2,}'
        seqReplacePattern = r'\1'
        for tweet in tweets:
            tweet = re.compile('https?://\S+|www\.\S+').sub(r'', tweet) # Remove hyperlinks

            if tweet.startswith("rt"): # Remove retweets (repetitions)
                i = tweet.find(':')
                if i != -1:  
                    tweet = tweet[i+2:]
            
            tweet = re.compile('@[^\s]+').sub(r'', tweet) # Mentions 
            tweet = re.compile(r'#([^\s]+)').sub(r'\1', tweet) # Remove hashtags
            tweet = re.sub('@', 'at', tweet)
            tweet  = ''.join([char for char in tweet if char not in string.punctuation]) #Remove punctuation characters
            tweet = re.compile('[^A-Za-z]').sub(r' ', tweet) # Remove any other non-alphabet characterss
            tweet = re.sub(sequencePattern, seqReplacePattern, tweet)
            tweet = re.sub(r'\\[nt]', ' ', tweet)
            tweet = re.sub(r"\s+", " ", tweet)
            tweet = re.sub(r"^\s+|\s+$", "", tweet)
            
            
            res.append(tweet)
        
        return res

    def tokenizing(self, tweets):
        return [str(tweet).split() for tweet in tweets]

    def normalization(self, tweets):
        res = []
        with open('./../static/slang-word.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()

            data = [line.strip().split('\t') for line in lines]
            data_singkatan = pd.DataFrame(data, columns=['Kata', 'Asli'])

            kontraksi_dict = dict(zip(data_singkatan['Kata'], data_singkatan['Asli']))

            for tweet in tweets:
                expanded_text = [kontraksi_dict[word] if word in kontraksi_dict else word for word in tweet]
                
                res.append(expanded_text)

            return res

    # def steaming(word):
    #     res = []
    #     for tweet in tweets:
    #         factory = StemmerFactory()
    #         stemmer = factory.create_stemmer()
    #         text = stemmer.stem(text)

    def stopword_removal(self, tweets):
        res = []
        for tweet in tweets:
            words = [w for w in tweet if w not in english_stopwords]  

            hapus = ["a", "about", "above", "after", "again", "against", "all", "am", "an",
            "and", "any", "are", "aren't", "as", "at", "be", "because", "been",
            "before", "being", "below", "between", "both", "but", "by", "can't",
            "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't",
            "doing", "don't", "down", "during", "each", "few", "for", "from",
            "further", "had", "hadn't", "has", "hasn't", "have", "haven't", "having",
            "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers",
            "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll",
            "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its",
            "itself", "let's", "me", "more", "most", "mustn't", "my", "myself",
            "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other",
            "ought", "our", "ours", "ourselves", "out", "over", "own", "same",
            "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't",
            "so", "some", "such", "than", "that", "that's", "the", "their", "theirs",
            "them", "themselves", "then", "there", "there's", "these", "they",
            "they'd", "they'll", "they're", "they've", "this", "those", "through",
            "to", "too", "under", "until", "up", "very", "was", "wasn't", "we",
            "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's",
            "when", "when's", "where", "where's", "which", "while", "who", "who's",
            "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you",
            "you'd", "you'll", "you're", "you've", "your", "yours", "yourself",
            "yourselves","f","d","c","b","e","g","h","i","j","k","l","m","n","o","p","q","r",
            "s","t","u","v","w","x","y","z","hey","hi","hello","helo","hii","hiii","hiiii","hiiiii",
            "hiiiiii","hiiiiiii","hiiiiiiii","hiiiiiiiii","hiiiiiiiiii","hiiiiiiiiiii","hiiiiiiiiiiii",
            "hiiiiiiiiiiiii","hiiiiiiiiiiiiii","hiiiiiiiiiiiiiii","hiiiiiiiiiiiiiiii","hiiiiiiiiiiiiiiiii",
            "hiiiiiiiiiiiiiiiiii","hiiiiiiiiiiiiiiiiiii","ve"]

            # Memfilter kata-kata yang tidak ada dalam array yang akan dihapus
            word = [kata for kata in tweet if kata not in hapus]

            res.append(word)

        return res