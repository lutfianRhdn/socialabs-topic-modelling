import nltk
import re
from nltk.corpus import stopwords
from config.settings import openai_key, openai_endpoint, openai_deploy_name
import openai
import json

class Llm:
    def getContext(topics, keyword, best_num_topics_str):
        # Create a prompt using the keywords
        role = "AI Linguistik"
        action = "dapat menentukan kalimat dari beberapa topik hasil dari proses topic modeling yang berupa kumpulan kata-kata, "
        step = "dengan mempertimbangkan bobot setiap topik yang ada, dalam merangkai kata-kata kunci menjadi kalimat yang padu untuk sebuah topik yang diperbincangkan di Twitter dengan mengambil kata dari hasil topic modeling lalu menyusunnya menjadi sebuah kalimat yang padu yang mudah dipahami. "
        context = f"Topik ini membahas tentang keyword: {keyword} dengan berbagai pandangan masyarakat terhadap topik tersebut dengan hasil topic modeling dengan 1 topik terdiri dari beberapa kata kunci berikut: {topics}. "
        format_str = f"""dengan format JSON dengan 1 topik untuk 1 kalimat utama dengan jumlah sesuai jumlah topik yang diberikan yaitu: {best_num_topics_str}. Berikut ini adalah format JSON-nya:
        `[
            {{
                "kata_kunci": "..."
                "kalimat": "..."
            }}
            ...
        ]`
        ONLY answer in JSON FORMAT without opening words. 
        """

        # Combine components into the RASCEF prompt
        prompt = f"Anda adalah {role} yang {action} {step} {context}. Buatkan {format_str}"

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
        generated_sentence = response['choices'][0]['message']['content'].replace('```', '')
        
        pattern = re.compile(r'\[(?:\s*{[^{}]*}\s*,?)*\s*\]')
        match = pattern.search(generated_sentence)

        if match:
            json_text = match.group()
            print(json_text)
        else:
            print("Tidak ada JSON yang ditemukan dalam string.")
        # Print the generated sentence
        res_json = json.loads(json_text)
        print(type(res_json))
        res = {
            "context": "",
            "interpretation": []
        }
        for index, item in enumerate(res_json):
            res['context'] += str(index+1)+". "+item['kalimat']+"<br/>"
            res['interpretation'].append({
                "word_topic": item['kata_kunci'],
                "word_interpretation": item['kalimat']
            })
            
        return res  
                
    def getContextByTopics(words, keyword):
        # Data dengan bobot kata-kata tertinggi untuk setiap topik
        # Assuming 'words' is a list of (word, weight) tuples
        topic_keywords = words
        # Create a prompt using the keywords
        role = "AI Linguistik"
        action = "dapat menentukan kalimat dari beberapa topik hasil dari proses topic modeling yang berupa kumpulan kata-kata, "
        step = "dengan mempertimbangkan bobot setiap topik yang ada, dalam merangkai kata-kata kunci menjadi kalimat yang padu untuk sebuah topik yang diperbincangkan di Twitter dengan mengambil kata dari hasil topic modeling lalu menyusunnya menjadi sebuah kalimat yang padu yang mudah dipahami. "
        context = f"Topik ini membahas tentang keyword: {keyword} dengan berbagai pandangan masyarakat terhadap topik tersebut dengan hasil topic modeling dengan 1 topik terdiri dari beberapa kata kunci berikut: {topic_keywords}. "
        format_str = "dengan format kalimat singkat yang mudah dipahami oleh masyarakat"

        # Combine components into the RASCEF prompt
        prompt = f"Anda adalah {role} yang {action} {step} {context}. Buatkan {format_str}"

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
            generated_sentence = response['choices'][0]['message']['content'].replace('```', '')
            
            # Extract context from the generated sentence
            context_start = generated_sentence.find("membahas tentang keyword:")
            context_end = generated_sentence.find(". Buatkan", context_start)
            context_value = generated_sentence[context_start:context_end].strip() if context_start != -1 and context_end != -1 else generated_sentence

            return context_value

        except Exception as e:
            return f"An error occurred: {str(e)}"