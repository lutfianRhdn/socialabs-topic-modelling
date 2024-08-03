import nltk
import re
from nltk.corpus import stopwords
from config.settings import openai_key, openai_endpoint, openai_deploy_name
import openai

class Llm:
    def getContext(topics, keyword, best_num_topics_str, docs):
        # Data dengan bobot kata-kata tertinggi untuk setiap topik
        data = [topics]

        # Mengolah data untuk mengambil kata-kata terbobot tertinggi
        topic_keywords = []
        for topic_data in data:
            topic_data = topic_data[0][1]  # Ambil data topik pertama (bobot tertinggi)
            topic_data = sorted(topic_data, key=lambda x: x[1], reverse=True)  # Urutkan berdasarkan bobot terbesar ke terkecil
            keywords = [word[0] for word in topic_data[:10]]  # Ambil 10 kata dengan bobot tertinggi
            topic_keywords.extend(keywords)

        # Create a prompt using the keywords
        role = "AI Linguistik"
        action = "menentukan kalimat dari beberapa topik berdasarkan dari kumpulan kata-kata hasil dari proses LDA"
        step = "mempertimbangkan bobot setiap topik yang ada pada penomoran angka dalam merangkai kata-kata kunci menjadi kalimat yang padu untuk sebuah topik yang di perbincangkan di Twitter dengan menggunakan penomoran untuk setiap topic dengan mengambil kata inti dari hasil LDA lalu menyusunnya menjadi sebuah kalimat yang padu yang mudah dipahami"
        context = f"membahas tentang keyword: {keyword} dengan berbagai pandangan masyarakat terhadap topic tersebut dengan hasil LDA dengan kata-kata kunci berikut : \n\n" + " ".join(topic_keywords)
        example = "Misalnya, jika hasil analisis LDA mengidentifikasi kata utama pada setiap penomoran, Anda akan menciptakan kalimat yang masing-masing menggambarkan topik tersebut."
        format_str = f"dengan format numbering list dengan 1 topik untuk 1 kalimat utama dengan jumlah sesuai jumlah topik yang diberikan yaitu : {best_num_topics_str}"

        # Combine components into the RASCEF prompt
        prompt = f"# RASCEF = Role + ( Action + Step + Context + Example ) + Format\n\nAnda adalah {role} yang {action} {step} {context}. Buatkan {format_str}"
        # prompt = f"""I have a topic that results from the LDA model,
        #             The topic is described with the following keywords: {topic_keywords}
        #             Based on the above information, extract a short topic label in the following format:
        #             [
        #                 'context topik 1',
        #                 'context topik 2',
        #                 ...
        #             ]"""


        # Generate a completion using the ChatCompletion endpoint
        openai.api_key = openai_key
        openai.api_base = openai_endpoint
        openai.api_type = 'azure'
        openai.api_version = '2023-05-15' # this might change in the future

        deployment_name= openai_deploy_name 

        response = openai.ChatCompletion.create(
            engine=deployment_name,
            # prompt=start_phrase,
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        # Extract the generated sentence from the response
        generated_sentence = response['choices'][0]['message']['content'].replace('\n', '<br/>').replace(' .', '.').strip()
        # generated_sentence = response['choices'][0]['message']['content']
        # Print the generated sentence
        return generated_sentence
                
    def getContextByTopics(words, keyword):
        # Data dengan bobot kata-kata tertinggi untuk setiap topik
        # Assuming 'words' is a list of (word, weight) tuples
        topic_keywords = words
        # Create a prompt using the keywords
        role = "AI Linguistik"
        action = "menentukan kalimat dari beberapa topik berdasarkan dari kumpulan kata-kata hasil dari proses LDA"
        step = ("dengan menganalisis bobot setiap topik yang ada pada penomoran angka dalam merangkai kata-kata kunci "
                "menjadi kalimat yang padu untuk sebuah topik yang diperbincangkan di Twitter dengan menggunakan penomoran "
                "untuk setiap topik dengan mengambil kata inti dari hasil LDA lalu menyusunnya menjadi sebuah kalimat yang "
                "padu yang mudah dipahami")
        context = f"membahas tentang keyword: {keyword} dengan berbagai pandangan masyarakat terhadap topik tersebut dengan kata-kata kunci berikut:\n{', '.join(topic_keywords)}"
        format_str = "dengan format kalimat singkat yang mudah dipahami oleh masyarakat"

        # Combine components into the RASCEF prompt
        prompt = f"# RASCEF = Role + ( Action + Step + Context + Example ) + Format\n\nAnda adalah {role} yang {action} {step} {context}. Buatkan {format_str}"

        # Generate a completion using the ChatCompletion endpoint
        openai.api_key = openai_key
        openai.api_base = openai_endpoint
        openai.api_type = 'azure'
        openai.api_version = '2023-05-15'  # this might change in the future

        deployment_name = openai_deploy_name

        try:
            response = openai.ChatCompletion.create(
                engine=deployment_name,
                # prompt=start_phrase,
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )

            # Extract the generated sentence from the response
            generated_sentence = response['choices'][0]['message']['content'].replace('\n', '<br/>').replace(' .', '.').strip()

            # Extract context from the generated sentence
            context_start = generated_sentence.find("membahas tentang keyword:")
            context_end = generated_sentence.find(". Buatkan", context_start)
            context_value = generated_sentence[context_start:context_end].strip() if context_start != -1 and context_end != -1 else generated_sentence

            return context_value

        except Exception as e:
            return f"An error occurred: {str(e)}"