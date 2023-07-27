import streamlit as st
from ai_unit import CaseAnalyzer, EvidenceAnalyzer, SimilarCaseFinder, LitigationStrategist

case_analyzer = CaseAnalyzer()
evidence_analyzer = EvidenceAnalyzer()
# similar_case_finder = SimilarCaseFinder()
# litigation_strategist = LitigationStrategist()

st.sidebar.title("AI Legal Assistant")
function = st.sidebar.selectbox("Select a function", ["Case analysis", "Evidence analysis", "Similar case analysis", "Litigation strategy"])

if function == "Case analysis":
    st.title("Case Analysis")
    case_text = st.text_area("Enter the details of your case:")
    if st.button("Analyze Case"):
        with st.spinner('🤔'):
            result = case_analyzer.analyze(case_text)
            # result = "1. 在这个案件中……\n\n2. 请求权基础主要是……\n\n3. 在这个案件中，原告的诉讼请求可能包括……\n\n4. 尽管提供的信息相对完整，但仍需要进一步澄清一些问题……"
            result_parts = result.split("\n\n")
            result_parts = [part.split('. ', 1)[-1] for part in result_parts]
            part_names = ["法律关系分析", "请求权基础", "诉讼请求", "待澄清问题"]
            for i in range(4):
                st.subheader(part_names[i])
                st.write(result_parts[i])
            st.caption("请在分析结果满意后在侧边栏选择下一个模块继续分析.")
        # if st.button("Next: Evidence Analysis"):
        #     function = "Evidence analysis"

elif function == "Evidence analysis":
    st.title("Evidence Analysis")
    evidence_input_method = st.radio("How would you like to provide your evidence?", ["Upload Image", "Upload PDF", "Enter Text"])
    if evidence_input_method == "Upload Image":
        evidence_image = st.file_uploader("Upload your evidence image:", type=["png", "jpg", "jpeg"])
        if st.button("Analyze Image Evidence"):
            # result = evidence_analyzer.analyze_image(evidence_image)
            result = "Analyzed Image Evidence"
            st.write(result)
    elif evidence_input_method == "Upload PDF":
        evidence_pdf = st.file_uploader("Upload your evidence PDF:", type=["pdf"])
        if st.button("Analyze PDF Evidence"):
            # result = evidence_analyzer.analyze_pdf(evidence_pdf)
            result = "Analyzed PDF Evidence"
            st.write(result)
    else:
        evidence_text = st.text_area("Enter your evidence text:")
        if st.button("Analyze Text Evidence"):
            # result = evidence_analyzer.analyze_text(evidence_text)
            result = "Analyzed Text Evidence"
            st.write(result)
    st.caption("请在分析结果满意后在侧边栏选择下一个模块继续分析.")
    # if st.button("Next: Similar Case Analysis"):
    #     function = "Similar case analysis"

elif function == "Similar case analysis":
    st.title("Similar Case Analysis")
    keywords = st.text_input("Enter keywords for retrieval:")
    geog_pref = st.text_input("Enter geographical preference:")
    if st.button("Find Similar Cases"):
        # result = similar_case_finder.find(keywords, geog_pref)
        result = "Found Similar Cases"
        st.write(result)
        # if st.button("Next: Litigation Strategy"):
        #     function = "Litigation strategy"

elif function == "Litigation strategy":
    st.title("Litigation Strategy")
    style = st.selectbox("Select a litigation style", ["Aggressive", "Defensive", "Balanced"])
    if st.button("Generate Strategy"):
        # result = litigation_strategist.generate(style)
        result = "Generated Strategy"
        st.write(result)
        # if st.button("Start Over"):
        #     function = "Case analysis"
