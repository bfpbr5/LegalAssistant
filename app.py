import streamlit as st
from ai_unit import CaseAnalyzer, EvidenceAnalyzer, SimilarCaseFinder, LitigationStrategist

case_analyzer = CaseAnalyzer()
evidence_analyzer = EvidenceAnalyzer()
similar_case_finder = SimilarCaseFinder()
litigation_strategist = LitigationStrategist()

# Initialize session state
st.session_state.setdefault("cases", [{"name": "Initial Case", "date": None, "steps": {}}])
st.session_state.setdefault("current_case", 0)

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

# Run the appropriate step based on the current state of the case
case = st.session_state["cases"][st.session_state["current_case"]]
case.setdefault("step", 1)

# Step 1: Case Analysis
if case["step"] >= 1:
    st.title("Case Analysis")
    case_text = st.text_area("Enter the details of your case:")
    if st.button("Analyze Case"):
        with st.spinner('🤔'):
            # result = case_analyzer.analyze(case_text)
            result = "1. 在这个案件中……\n\n2. 请求权基础主要是……\n\n3. 在这个案件中，原告的诉讼请求可能包括……\n\n4. 尽管提供的信息相对完整，但仍需要进一步澄清一些问题……"
            result_parts = case_analyzer.split_analysis(result)
            part_names = ["Case Context", "Claim Basis", "Plaintiff's Claims", "Additional Questions"]
            for i in range(4):
                st.subheader(part_names[i])
                st.write(result_parts[i])
            case["steps"][1] = {"input": case_text, "output": result_parts}
            case["step"] += 1

# Step 2: Evidence Analysis
if case["step"] >= 2:
    st.title("Evidence Analysis")
    evidence_input_method = st.radio("How would you like to provide your evidence?", ["Upload Image", "Upload PDF", "Enter Text"])
    if evidence_input_method == "Upload Image":
        evidence_image = st.file_uploader("Upload your evidence image:", type=["png", "jpg", "jpeg"])
        if st.button("Analyze Image Evidence"):
            # result = evidence_analyzer.analyze_image(evidence_image)
            result = "test"
            st.write(result)
            case["step"] += 1
    elif evidence_input_method == "Upload PDF":
        evidence_pdf = st.file_uploader("Upload your evidence PDF:", type=["pdf"])
        if st.button("Analyze PDF Evidence"):
            # result = evidence_analyzer.analyze_pdf(evidence_pdf)
            result = "test"
            st.write(result)
            case["step"] += 1
    else:
        evidence_text = st.text_area("Enter your evidence text:")
        if st.button("Analyze Text Evidence"):
            # result = evidence_analyzer.analyze_text(evidence_text)
            result = "test"
            st.write(result)
            case["step"] += 1

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
