import streamlit as st
from ai_unit import CaseAnalyzer, EvidenceAnalyzer, SimilarCaseFinder, LitigationStrategist

case_analyzer = CaseAnalyzer()
evidence_analyzer = EvidenceAnalyzer()
similar_case_finder = SimilarCaseFinder()
litigation_strategist = LitigationStrategist()

if "cases" not in st.session_state:
    st.session_state["cases"] = []

if "current_case" not in st.session_state:
    st.session_state["current_case"] = None

# Allow user to add a new case
if st.sidebar.button("Add a new case"):
    case_name = st.sidebar.text_input("Enter case name:")
    case_date = st.sidebar.date_input("Enter case date:")
    st.session_state["cases"].append({"name": case_name, "date": case_date, "steps": {}})
    st.session_state["current_case"] = len(st.session_state["cases"]) - 1

# Allow user to select a case
case_names = [case["name"] for case in st.session_state["cases"]]
case_index = st.sidebar.selectbox("Select a case", case_names, index=st.session_state["current_case"])
if case_index != st.session_state["current_case"]:
    st.session_state["current_case"] = case_index

# Run the appropriate step based on the current state of the case
case = st.session_state["cases"][st.session_state["current_case"]]
if "step" not in case:
    case["step"] = 1

if case["step"] == 1:
    st.title("Case Analysis")
    case_text = st.text_area("Enter the details of your case:")
    if st.button("Analyze Case"):
        with st.spinner('🤔'):
            result = case_analyzer.analyze(case_text)
            result_parts = result.split("\n\n")
            result_parts = [part.split('. ', 1)[-1] for part in result_parts]
            part_names = ["Case Context", "Claim Basis", "Plaintiff's Claims", "Additional Questions"]
            for i in range(4):
                st.subheader(part_names[i])
                st.write(result_parts[i])
            case["steps"][1] = {"input": case_text, "output": result_parts}
            case["step"] += 1

# Repeat for steps 2, 3, and 4



elif case["step"] == 2:
    st.title("Evidence Analysis")
    evidence_input_method = st.radio("How would you like to provide your evidence?", ["Upload Image", "Upload PDF", "Enter Text"])
    if evidence_input_method == "Upload Image":
        evidence_image = st.file_uploader("Upload your evidence image:", type=["png", "jpg", "jpeg"])
        if st.button("Analyze Image Evidence"):
            # result = evidence_analyzer.analyze_image(evidence_image)
            result = "test"
            st.write(result)
            st.session_state["step"] += 1
    elif evidence_input_method == "Upload PDF":
        evidence_pdf = st.file_uploader("Upload your evidence PDF:", type=["pdf"])
        if st.button("Analyze PDF Evidence"):
            # result = evidence_analyzer.analyze_pdf(evidence_pdf)
            result = "test"
            st.write(result)
            st.session_state["step"] += 1
    else:
        evidence_text = st.text_area("Enter your evidence text:")
        if st.button("Analyze Text Evidence"):
            # result = evidence_analyzer.analyze_text(evidence_text)
            result = "test"
            st.write(result)
            st.session_state["step"] += 1
    st.caption("请在分析结果满意后在侧边栏选择下一个模块继续分析.")


elif case["step"] == 3:
    st.title("Similar Case Analysis")
    keywords = st.text_input("Enter keywords for retrieval:")
    geog_pref = st.text_input("Enter geographical preference:")
    if st.button("Find Similar Cases"):
        # result = similar_case_finder.find(keywords, geog_pref)
        result = "test"
        st.write(result)
        st.session_state["step"] += 1


elif case["step"] == 4:
    st.title("Litigation Strategy")
    style = st.selectbox("Select a litigation style", ["Aggressive", "Defensive", "Balanced"])
    if st.button("Generate Strategy"):
        # result = litigation_strategist.generate(style)
        result = "test"
        st.write(result)
        st.session_state["step"] = 1

