import gensim
import numpy as np
from gensim import corpora
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial.distance import jensenshannon
from joblib import Parallel, delayed

class Lda:

    def create_model(self, corpus, dictionary, num_topics):
        return gensim.models.LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=10, alpha='symmetric')

    def generateTopic(self, data):
        np.random.seed(1)
        dictionary = corpora.Dictionary(data)
        corpus = [dictionary.doc2bow(doc) for doc in data]
        num_topics_range = range(2, 10)
        
        lda_models = Parallel(n_jobs=-1)(delayed(self.create_model)(corpus, dictionary, num_topics) for num_topics in num_topics_range)
        
        # Ambil topik-topik dari model-model tersebut
        all_topics = []
        for model in lda_models:
            topics = model.show_topics(formatted=False, num_words=10)
            all_topics.append([(topic_id, dict(words)) for topic_id, words in topics])
        
        # Lanjutkan dengan agregasi topik dan pemodelan akhir seperti sebelumnya
        agregated_topic = self.agregrat(all_topics, dictionary)
        num_topics = len(agregated_topic)

        lda_model = self.create_model(corpus, dictionary, num_topics)
        return lda_model

    def agregrat(self, all_topics, dictionary):
        aggregated_topics = []
        threshold = 0.5

        for topics in all_topics:
            for topic_id, topic_words in topics:
                merged = False
                for agg_id, agg_topic in enumerate(aggregated_topics):
                    cosine_sim = self.cosine_similarity_topic(topic_words, agg_topic, dictionary)
                    if cosine_sim > threshold:
                        aggregated_topics[agg_id] = {word: (agg_topic.get(word, 0) + weight) / 2 for word, weight in topic_words.items()}
                        merged = True
                        break
                if not merged:
                    aggregated_topics.append(topic_words)
                    
        return aggregated_topics

    # Fungsi untuk menghitung kesamaan antar topik menggunakan cosine similarity
    def cosine_similarity_topic(self, topic1, topic2, dictionary):
        vec1 = np.zeros(len(dictionary))
        vec2 = np.zeros(len(dictionary))
        for word, weight in topic1.items():
            vec1[dictionary.token2id[word]] = weight
        for word, weight in topic2.items():
            vec2[dictionary.token2id[word]] = weight
        return cosine_similarity([vec1], [vec2])[0][0]

    # Fungsi untuk menghitung kesamaan antar topik menggunakan Jensen-Shannon divergence
    def jensen_shannon_topic(self, topic1, topic2, dictionary):
        vec1 = np.zeros(len(dictionary))
        vec2 = np.zeros(len(dictionary))
        for word, weight in topic1.items():
            vec1[dictionary.token2id[word]] = weight
        for word, weight in topic2.items():
            vec2[dictionary.token2id[word]] = weight
        return 1 - jensenshannon(vec1, vec2)
    
    def document(self, data_tweet, data, lda_model):
        dictionary = corpora.Dictionary(data)
        documents_probability = []
        for i, doc in enumerate(data):
            bow = dictionary.doc2bow(doc)
            probs = lda_model.get_document_topics(bow)
            top_topic = max(probs, key=lambda x: x[1])
            data_tweet[i].update({
                "topic": str(top_topic[0]),
                "probability": str(top_topic[1])
            })
            documents_probability.append(data_tweet[i])
        
        return documents_probability

    def agregrat(self, all_topics, dictionary):
        aggregated_topics = []
        threshold = 0.5

        for topics in all_topics:
            for topic_id, topic_words in topics:
                merged = False
                for agg_id, agg_topic in enumerate(aggregated_topics):
                    cosine_sim = self.cosine_similarity_topic(topic_words, agg_topic, dictionary)
                    if cosine_sim > threshold:
                        aggregated_topics[agg_id] = {word: (agg_topic.get(word, 0) + weight) / 2 for word, weight in topic_words.items()}
                        merged = True
                        break
                if not merged:
                    aggregated_topics.append(topic_words)
                    
        return aggregated_topics
