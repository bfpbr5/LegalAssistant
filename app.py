import streamlit as st
from ai_unit import CaseAnalyzer, EvidenceAnalyzer, SimilarCaseFinder, LitigationStrategist, Chatbot
from aip import AipSpeech, AipOcr
# 设置百度API的参数
APP_ID = '37863384'
API_KEY = 'P7G5MoH6A8NuMgdWC2GU1aiN'
SECRET_KEY = 'EAByZyEt1Gp4HxiKGBgsG9ggKjr4I16F'

# 初始化百度API的客户端
client_speech = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
client_ocr = AipOcr(APP_ID, API_KEY, SECRET_KEY)

case_analyzer = CaseAnalyzer()
evidence_analyzer = EvidenceAnalyzer()
similar_case_finder = SimilarCaseFinder()
litigation_strategist = LitigationStrategist()

# Initialize session state
st.session_state.setdefault("cases", [{"name": "Initial Case", "date": None, "step": 1, "conversation":[]}])
st.session_state.setdefault("current_case", 0)
st.session_state.setdefault("analysis_results", {})

current_case_index = st.session_state.current_case
current_case = st.session_state.cases[current_case_index]
# Set default session state for evidence analysis clicked for the current case
st.session_state.setdefault(f"evidence_analysis_clicked_{current_case_index}", False)


def store_analysis_results(case_id, module_name, analysis_parts):
    if case_id not in st.session_state.analysis_results:
        st.session_state.analysis_results[case_id] = {}
    st.session_state.analysis_results[case_id][module_name] = analysis_parts

def retrieve_analysis_results(case_id, module_name=None):
    if module_name:
        return st.session_state.analysis_results.get(case_id, {}).get(module_name, {})
    return st.session_state.analysis_results.get(case_id, {})
    

# Option to switch between case navigation and chatbot
sidebar_option = st.sidebar.radio("Choose an option:", ("Case Navigation", "Chat with Bot"))

# Case Navigation
if sidebar_option == "Case Navigation":

    with st.sidebar.form("Add case form"):
        case_name = st.text_input("Enter case name:")
        case_date = st.date_input("Enter case date:")
        submitted = st.form_submit_button("Add a new case")

    if submitted:
        st.session_state["cases"].append({"name": case_name, "date": case_date, "steps": {}})
        st.session_state["current_case"] = len(st.session_state["cases"]) - 1

    # Allow user to select a case
    case_names = [case["name"] for case in st.session_state["cases"]] if st.session_state["cases"] else ["No cases"]
    case_index = st.sidebar.selectbox("Select a case", case_names, index=int(st.session_state["current_case"]) if st.session_state["current_case"] is not None else 0)
    if case_index != st.session_state["current_case"]:
        st.session_state["current_case"] = case_names.index(case_index)

# Chat with Bot
elif sidebar_option == "Chat with Bot":
    # Retrieve the current case ID
    current_case_id = st.session_state["cases"][st.session_state["current_case"]]["name"]

    # Initialize chatbot for the current case
    chatbot = Chatbot(current_case_id)

    # Option to load case details
    load_case_details = st.sidebar.checkbox("Load Case Details")
    user_input = st.sidebar.text_input("Chat with the bot:")
    if st.sidebar.button("Send"):
        analysis_data = None
        if load_case_details:
            analysis_data = retrieve_analysis_results(current_case_id)
        chatbot.add_user_message(user_input, analysis_data=analysis_data, load_case=load_case_details)
        bot_response = chatbot.get_bot_response()

        # Reset the "Load Case Details" checkbox
        load_case_details = False

    # Retrieve and display conversation for the current case
    for case in st.session_state["cases"]:
        if case["name"] == current_case_id:
            conversation = case["conversation"]
            for message in conversation:
                if message['role'] == 'user':
                    st.sidebar.write(f"You: {user_input}")
                elif message['role'] == 'assistant':
                    st.sidebar.write(f"Bot: {message['content']}")
            break

# Run the appropriate step based on the current state of the case
case = st.session_state["cases"][st.session_state["current_case"]]
case_id = case["name"]
case.setdefault("step", 1)

# Step 1: Case Analysis
if case["step"] >= 1:

    st.title("Case Analysis")
    case_text = st.text_area("Enter the details of your case:")
    if st.button("Analyze Case"):
        with st.spinner('🤔'):
            result = case_analyzer.analyze(case_text)
            # result = "1. 在这个案件中……\n\n2. 请求权基础主要是……\n\n3. 在这个案件中，原告的诉讼请求可能包括……\n\n4. 尽管提供的信息相对完整，但仍需要进一步澄清一些问题……\n\n5."
            result_parts = case_analyzer.split_analysis(result)
            case_id = case["name"] # Assuming the case name or ID is used to identify the case
            store_analysis_results(case_id, "Case Analysis", {
                "Case Timeline": result_parts[0],
                "Case Context": result_parts[1],
                "Claim Basis": result_parts[2],
                "Plaintiff's Claims": result_parts[3],
                "Additional Questions": result_parts[4]
            })

    # Check if the analysis results already exist for this case
    case_analysis_results = retrieve_analysis_results(case_id, "Case Analysis")
    if case_analysis_results:
        part_names = ["Case Timeline", "Case Context", "Claim Basis", "Plaintiff's Claims", "Additional Questions"]
        for part_name, result_part in case_analysis_results.items():
            st.subheader(part_name)
            st.write(result_part)
        case["step"] += 1
    # case["steps"][1] = {"input": case_text, "output": result_parts}
    

if current_case["step"] >= 2:
    case_analysis_results = retrieve_analysis_results(case_id, "Case Analysis")
    if st.button("证据分析"):
        st.session_state[f"evidence_analysis_clicked_{current_case_index}"] = True

    if st.session_state[f"evidence_analysis_clicked_{current_case_index}"]:
        with st.spinner('🤔'):
            evidence_analysis_results = evidence_analyzer.analyze(case_analysis_results)
            evidence_analysis_results_list = evidence_analyzer.split_analysis(evidence_analysis_results)
            st.title("Evidence Analysis")
            descriptions = evidence_analysis_results_list
            evid_num = 0
            container = st.container()

            for desc in descriptions:
                cols = container.columns(3)
                cols[0].write(desc)
                
                # File uploader for each row in column 2
                uploaded_files = cols[1].file_uploader(label=f"上传证据文件:", key=evid_num, accept_multiple_files=True)
                result_content = ''
                for uploaded_file in uploaded_files:
                    if uploaded_file:
                        image_data = uploaded_file.read()
                        result_ocr = client_ocr.basicGeneral(image_data)
                        if result_ocr.get('words_result_num') > 0:
                            for line in result_ocr['words_result']:
                                result_content += line['words'] + '\n'
                qry = evidence_analyzer.evidence_query_prompt(desc)
                org_ocr = evidence_analyzer.organize_ocr(result_content)

                # cols[1].write(org_ocr)  # Display OCR results
                
                verify_result = evidence_analyzer.check_evidence_valid(desc, org_ocr)
                cols[2].write(verify_result)
                # evidence_analyzer.check_evidence(result_content)
                evid_num += 1

            # st.write(evidence_analysis_results)


# Step 3: Similar Case Analysis
if case["step"] >= 3:
    st.title("Similar Case Analysis")
    keywords = st.text_input("Enter keywords for retrieval:")
    geog_pref = st.text_input("Enter geographical preference:")
    if st.button("Find Similar Cases"):
        # result = similar_case_finder.find(keywords, geog_pref)
        result = "test"
        st.write(result)
        case["step"] += 1

# Step 4: Litigation Strategy
if case["step"] >= 4:
    st.title("Litigation Strategy")
    style = st.selectbox("Select a litigation style", ["Aggressive", "Defensive", "Balanced"])
    if st.button("Generate Strategy"):
        # result = litigation_strategist.generate(style)
        result = "test"
        st.write(result)
        case["step"] = 1
