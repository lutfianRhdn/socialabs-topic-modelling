import re
import pandas as pd
import nltk
import string
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords')
indonesian_stopwords = set(stopwords.words('indonesian'))
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
            res.append(tweet)
        
        return res

    def tokenizing(self, tweets):
        return [str(tweet).split() for tweet in tweets]

    def normalization(self, tweets):
        res = []
        with open('./static/kbba.txt', 'r', encoding='utf-8') as file:
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
            words = [w for w in tweet if w not in indonesian_stopwords]  

            hapus = ['id','amp','deh','tanyakanrl','sih','na','si','rj','lc','ar','oe','al','sm','ri','en','ar','mc','vt','rob','ny','dc','az','va','mkmk','nya','do','ye','adalah']

            # Memfilter kata-kata yang tidak ada dalam array yang akan dihapus
            word = [kata for kata in tweet if kata not in hapus]

            res.append(word)

        return res