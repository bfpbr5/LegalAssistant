import streamlit as st
from ai_unit import CaseAnalyzer, EvidenceAnalyzer, SimilarCaseFinder, LitigationStrategist

case_analyzer = CaseAnalyzer()
# evidence_analyzer = EvidenceAnalyzer()
# similar_case_finder = SimilarCaseFinder()
# litigation_strategist = LitigationStrategist()

st.sidebar.title("AI Legal Assistant")
function = st.sidebar.selectbox("Select a function", ["Case analysis", "Evidence analysis", "Similar case analysis", "Litigation strategy"])

if function == "Case analysis":
    st.title("Case Analysis")
    case_text = st.text_area("Enter the details of your case:")
    if st.button("Analyze Case"):
        # result = case_analyzer.analyze(case_text)
        result = case_analyzer.analyze(case_text)
        result_parts = result.split("\n\n")
        part_names = ["法律关系分析", "请求权基础", "诉讼请求", "待澄清问题"]
        for i in range(4):
            st.subheader(part_names[i])
            st.write(result_parts[i])

elif function == "Evidence analysis":
    st.title("Evidence Analysis")
    evidence_file = st.file_uploader("Upload your evidence:")
    if st.button("Analyze Evidence"):
        # result = evidence_analyzer.analyze(evidence_file)
        result = "Analyzed Evidence"
        st.write(result)

elif function == "Similar case analysis":
    st.title("Similar Case Analysis")
    keywords = st.text_input("Enter keywords for retrieval:")
    geog_pref = st.text_input("Enter geographical preference:")
    if st.button("Find Similar Cases"):
        # result = similar_case_finder.find(keywords, geog_pref)
        result = "Found Similar Cases"
        st.write(result)

elif function == "Litigation strategy":
    st.title("Litigation Strategy")
    style = st.selectbox("Select a litigation style", ["Aggressive", "Defensive", "Balanced"])
    if st.button("Generate Strategy"):
        # result = litigation_strategist.generate(style)
        result = "Generated Strategy"
        st.write(result)
