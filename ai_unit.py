import openai
import promptlayer
import streamlit as st
# import langchain

promptlayer.api_key = "pl_6693b063dd1e5bc294f4fb3e18820039"
openai = promptlayer.openai
openai.api_key = st.secrets["openai"]["api_key"]

class CaseAnalyzer:
    def __init__(self):
        # Initialize the OpenAI API
        pass

    def analyze(self, case_text):
        # Send the case details to the API and get the response
        response = openai.ChatCompletion.create(
          model="gpt-4",
          messages=[
                {"role": "system", "content": """Suppose you're a seasoned Chinese attorney well-versed in the civil law system. A user will share a case with you for review. Structure your response following below: 
1) Analyzing the case to discern the involved legal relations,
2) Establishing the cause of action(案由),
3) Identifying the litigation request presented in the case, and 
4) Evaluating if the given information is comprehensive and seeking further clarification if necessary.
Please structure your response using a format similar to '1.' to clearly distinguish and separate each part of the content. Additionally, kindly refrain from including the original request and any extra text in your response.
Finally, always answer in Chinese."""},
                {"role": "user", "content": case_text}
            ],
        temperature=0.1
        )
        # Return the assistant's reply
        return response['choices'][0]['message']['content']
    
    # def chat(self, history, )


class EvidenceAnalyzer:
    def __init__(self):
        # Initialize the OpenAI API
        pass

    def analyze(self, evidence_file):
        # Since GPT-3 doesn't support image analysis, we'll return a placeholder
        return "GPT-3 does not support image or document analysis."


class SimilarCaseFinder:
    def __init__(self):
        # Initialize the OpenAI API
        pass

    def find(self, keywords, geog_pref):
        # Send the keywords and geographical preference to the API and get the response
        query = f"Find similar cases related to {keywords} in {geog_pref}."
        response = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": query}
            ]
        )
        # Return the assistant's reply
        return response['choices'][0]['message']['content']


class LitigationStrategist:
    def __init__(self):
        # Initialize the OpenAI API
        pass

    def generate(self, style):
        # Send the litigation style to the API and get the response
        response = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Generate a {style} litigation strategy."}
            ]
        )
        # Return the assistant's reply
        return response['choices'][0]['message']['content']