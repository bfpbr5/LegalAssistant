import streamlit as st
from ai_unit import CaseAnalyzer, EvidenceAnalyzer, SimilarCaseFinder, LitigationStrategist, Chatbot

case_analyzer = CaseAnalyzer()
evidence_analyzer = EvidenceAnalyzer()
similar_case_finder = SimilarCaseFinder()
litigation_strategist = LitigationStrategist()

# Initialize session state
st.session_state.setdefault("cases", [{"name": "Initial Case", "date": None, "step": 1, "conversation":[]}])
st.session_state.setdefault("current_case", 0)
st.session_state.setdefault("analysis_results", {})

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
    

# Step 2: Evidence Analysis
if case["step"] >= 2:
    case_analysis_results = retrieve_analysis_results(case_id, "Case Analysis")
    if st.button("证据分析"):
        with st.spinner('🤔'):
            evidence_analysis_results = evidence_analyzer.analyze(case_analysis_results)
            evidence_analysis_results_list = evidence_analyzer.split_analysis(evidence_analysis_results)
            st.title("Evidence Analysis")
            # Text descriptions for the first column
            descriptions = evidence_analysis_results_list
            evid_num = 0
            # Create a container to hold the rows
            container = st.container()

            # Iterate through the descriptions and create rows with 3 columns
            for desc in descriptions:
                # Create a row using beta_columns
                cols = container.columns(3)
                
                # First column: text description
                cols[0].write(desc)
                
                # Second column: text input box
                input_value = cols[1].text_input(label=f"请输入证据:", value="", key=evid_num)
                
                # Third column: You can add additional content here, such as an image or button
                cols[2].write("Additional content")  # Example content
                if input_value:
                    evidence_analyzer.check_evidence(input_value)
                evid_num += 1

            st.write(evidence_analysis_results)


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
