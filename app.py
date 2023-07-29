import streamlit as st
from ai_unit import CaseAnalyzer, EvidenceAnalyzer, SimilarCaseFinder, LitigationStrategist

case_analyzer = CaseAnalyzer()
evidence_analyzer = EvidenceAnalyzer()
similar_case_finder = SimilarCaseFinder()
litigation_strategist = LitigationStrategist()

# Initialize session state
st.session_state.setdefault("cases", [{"name": "Initial Case", "date": st.date_input('Please select a date', value=None), "steps": {}}])
st.session_state.setdefault("current_case", 0)

def add_new_case():
    case_name = st.sidebar.text_input("Enter case name:")
    case_date = st.sidebar.date_input("Enter case date:")
    st.session_state["cases"].append({"name": case_name, "date": case_date, "steps": {}})
    st.session_state["current_case"] = int(len(st.session_state["cases"]) - 1)

# Allow user to add a new case
if st.sidebar.button("Add a new case"):
    add_new_case()

# Allow user to select a case
case_names = [case["name"] for case in st.session_state["cases"]] if st.session_state["cases"] else ["No cases"]
case_index = st.sidebar.selectbox("Select a case", case_names, index=int(st.session_state["current_case"]) if st.session_state["current_case"] is not None else 0)
if case_index != st.session_state["current_case"]:
    st.session_state["current_case"] = case_index

# Run the appropriate step based on the current state of the case
case = st.session_state["cases"][int(st.session_state["current_case"])]
case.setdefault("step", 1)

# Rest of your code
