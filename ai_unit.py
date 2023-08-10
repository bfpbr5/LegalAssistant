import openai
import promptlayer
import streamlit as st
# import langchain

promptlayer.api_key = "pl_6693b063dd1e5bc294f4fb3e18820039"
openai = promptlayer.openai
openai.api_key = st.secrets["openai"]["api_key"]
# color_prefix_by_role = {
# "system": "\033[0m",  # gray
# "user": "\033[0m",  # gray
# "assistant": "\033[92m",  # green
# }

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
1) Analyzing the case to discern all involved legal relations,
2) Establishing the cause of action(案由),
3) Identifying the litigation request presented in the case, make sure your identification is comprehensive enought to cover all possible requests, then analyze how to maximize profits for the client, 
4) Evaluating if the given information is comprehensive and seeking further clarification if necessary.
Here are guidelines to give a better response:
1. **Embrace Comprehensive Fact-Checking**: Before starting your analysis, make sure you have all the necessary facts. Check for regulatory compliance, contract validity, and other foundational elements of the case. Never make assumptions about these facts; ensure everything is verified. Remember, a strong legal analysis is built on the bedrock of accurate, comprehensive information.

2. **Flexibility in Legal Framework Application**: Do not limit yourself to your area of expertise or previous experiences. Each case is unique and may require a different legal framework. Continually review your understanding of various legal principles and their applicability. Be adaptable and versatile in your approach, tailoring your analysis to the specifics of the case.

3. **Specific Tailoring of Analytical Approach**: While generic models and checklists can be helpful, don't forget to adapt your analysis to the specifics of the case. There is no one-size-fits-all in legal analysis. Each case has its peculiarities that must be addressed. Tailoring your analysis to the case not only provides a more accurate assessment but also highlights your critical thinking skills.

4. **Patient, Step-by-Step Reasoning**: Don't rush to conclusions. Before formulating your legal strategies, ensure that you understand all the facts and have considered all possible angles. Proceed with your analysis methodically, building your case step by step. This patient, systematic approach reduces the chance of oversight and enhances the quality of your legal analysis.

5. **Anticipate Counterarguments**: Try to anticipate the other party's arguments and be ready with counterarguments. This will make your case more robust and gives you a better understanding of the potential strengths and weaknesses of your case.
Please structure your response using a format similar to '1.' to clearly distinguish and separate each part of the content. Additionally, kindly refrain from including the original request and any extra text in your response.
Finally, always answer in Chinese."""},
                {"role": "user", "content": case_text}
            ],
        temperature=0.1
        )
        # Return the assistant's reply
        self.full_analysis = response['choices'][0]['message']['content']
        return self.full_analysis
    
    def split_analysis(self, response):
        result_parts = response.split("\n\n")
        result_parts = [part.split('. ', 1)[-1] for part in result_parts]
        self.context = result_parts[0]
        self.cause = result_parts[1]
        self.claim = result_parts[2]
        self.questions = result_parts[3]
        return result_parts

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
    
class Chatbot:
    def __init__(self, case_id, model="gpt-4"):
        self.model = model
        self.case_id = case_id
        self.initialize_conversation()

    def initialize_conversation(self):
        # Check if a conversation history exists for the given case
        for case in st.session_state["cases"]:
            if case["name"] == self.case_id:
                if "conversation" not in case or not case["conversation"]:
                    # If not, initialize the conversation
                    case["conversation"] = [
                        {
                        "role": "system",
                        "content": """
You're a seasoned Chinese attorney well-versed in the civil law system. A user has shared a case with you for review. 
Your task is:
1. to clarify the case for the user and provide an accurate analysis based on their thoughts.
2. When user asks for calculation, always provide detailed and accurate calculation steps before giving the answer.
3. Ask for clarification if a user request is ambiguous.
4. not to answer any off-topic questions.
"""
                    }
                ])
                break

    def add_user_message(self, thoughts, analysis_data):
        content_parts = [f"My thoughts: {thoughts}"]

        for module_name, module_data in analysis_data.items():
            for key, value in module_data.items():
                content_parts.append(f"The {key}: {value}")

        content = ". ".join(content_parts)

        # Find the case by name and append the user message to the conversation
        for case in st.session_state["cases"]:
            if case["name"] == self.case_id:
                case["conversation"].append({
                    "role": "user",
                    "content": content
                })
                break

    def get_bot_response(self):
        # Retrieve the current conversation for the given case
        conversation = []
        for case in st.session_state["cases"]:
            if case["name"] == self.case_id:
                conversation = case["conversation"]
                break

        # Create a response with stream=True
        response_stream = openai.ChatCompletion.create(
            model=self.model,
            messages=conversation,
            stream=True
        )
        bot_message = ""
        for chunk in response_stream:
            delta = chunk["choices"][0]["delta"]
            if "content" in delta:
                bot_message += delta["content"]

        # Find the case by name and append the bot message to the conversation
        for case in st.session_state["cases"]:
            if case["name"] == self.case_id:
                case["conversation"].append({
                    "role": "assistant",
                    "content": bot_message
                })
                break
        return bot_message

    def reset_conversation(self):
        # Find the case by name and reset the conversation
        for case in st.session_state["cases"]:
            if case["name"] == self.case_id:
                case["conversation"] = [
                    {
                        "role": "system",
                        "content": "You are a helpful assistant."
                    }
                ]
                break
