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
        return response['choices'][0]['message']['content']
    
    def split_analysis(self, response):
        result_parts = response.split("\n\n")
        result_parts = [part.split('. ', 1)[-1] for part in result_parts]
        self.context = result_parts[0]
        self.cause = result_parts[1]
        self.claim = result_parts[2]
        self.questions = result_parts[3]
        return result_parts
    
    # def chat(self, history, para):
    #     # Extracting history and parameters from the input
    #     history_need_input, paras_need_input = history, para

    #     # Call the API
    #     with st.spinner("🤔"):
    #         try:
    #             r = openai.ChatCompletion.create(model=st.session_state["select_model"], messages=history_need_input,
    #                                             stream=True,
    #                                             **paras_need_input)
    #         except (FileNotFoundError, KeyError):
    #             st.error("OpenAI API Key is missing. Please configure it in Secrets after copying the project, or configure it temporarily in the model options.")
    #         except openai.error.AuthenticationError:
    #             st.error("Invalid OpenAI API Key.")
    #         except openai.error.APIConnectionError as e:
    #             st.error("Connection timed out, please try again. Error: \n" + str(e.args[0]))
    #         except openai.error.InvalidRequestError as e:   
    #             st.error("Invalid request, please try again. Error: \n" + str(e.args[0]))
    #         except openai.error.RateLimitError as e:
    #             st.error("Request limit exceeded. Error: \n" + str(e.args[0]))
    #         else:
    #             st.session_state["chat_of_r"] = function
    #             st.session_state["r"] = r
    #             st.experimental_rerun()

    #     if ("r" in st.session_state) and (function == st.session_state["chat_of_r"]):
    #         try:
    #             for e in st.session_state["r"]:
    #                 if "content" in e["choices"][0]["delta"]:
    #                     st.session_state[function + 'report'] += e["choices"][0]["delta"]["content"]
    #                     st.write(st.session_state['pre_user_input_content'])
    #                     st.write(st.session_state[function + 'report'])
    #         except ChunkedEncodingError:
    #             st.error("Poor network condition, please refresh the page and try again.")
    #         # Handle 'stop' situation
    #         except Exception:
    #             pass
    #         else:
    #             # Save content
    #             st.session_state["history"].append(
    #                 {"role": "user", "content": st.session_state['pre_user_input_content']})
    #             st.session_state["history"].append(
    #                 {"role": "assistant", "content": st.session_state[function + 'report']})
    #         # Handle when user clicks 'stop' on the webpage, ss may be temporarily empty under certain circumstances
    #         if function + 'report' in st.session_state:
    #             st.session_state.pop(function + 'report')
    #         if 'r' in st.session_state:
    #             st.session_state.pop("r")
    #             st.experimental_rerun()



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