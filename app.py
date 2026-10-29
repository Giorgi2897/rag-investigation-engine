from rag_engine import InvestigationEngine
import streamlit as st
from ui_components import render_main_search, render_sidebar

# გვერდის ძირითადი კონფიგურაცია
st.set_page_config(
    page_title="AI Investigation Engine", page_icon="🔍", layout="wide"
)


@st.cache_resource
def load_engine():
  return InvestigationEngine()


engine = load_engine()

st.title("🛡️ AI Investigation Engine (Modular RAG)")
st.write(
    "სისტემა უზრუნველყოფს მრავალსაფეხურიან ძიებას, დოკუმენტების მართვას (CRUD)"
    " და მეტამონაცემების ანალიზს."
)

# ვიზუალური ნაწილების რენდერი
render_sidebar(engine)
render_main_search(engine)