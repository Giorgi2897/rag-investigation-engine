import os
from dotenv import load_dotenv
import google.generativeai as genai
import streamlit as st  # დავამატეთ streamlit-ის მხარდაჭერა

load_dotenv()

# ვცდილობთ ამოვიღოთ გასაღები ან Streamlit Cloud-ის Secrets-იდან, ან ლოკალური .env ფაილიდან
api_key = None
try:
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass

if not api_key:
    api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)


class LLMService:

    def __init__(self, model_name="gemini-3.8-flash", db_manager=None):
        self.model_name = model_name
        self.db_manager = db_manager
        
        # Tool Calling: ვუწესებთ მოდელს ინსტრუმენტს (ფუნქციას), რომლის გამოძახებაც შეუძლია
        tools = [self.get_database_stats_tool] if db_manager else None
        
        self.model = genai.GenerativeModel(
            model_name=model_name,
            tools=tools
        )

    def get_database_stats_tool(self):
        """Tool Calling ფუნქცია: აბრუნებს ვექტორულ ბაზაში არსებული ჩანქერების რაოდენობას."""
        if self.db_manager:
            count = self.db_manager.get_total_documents_count()
            return {"status": "success", "total_indexed_chunks": count}
        return {"status": "error", "message": "Database manager not connected."}

    def generate_investigation_answer(self, query: str, context_text: str) -> str:
        prompt = f"""
        შენ ხარ პროფესიონალური AI Investigation Assistant (საგამოძიებო ასისტენტი RAG სისტემაში).
        გთხოვ, მკაცრად დაიცვა შემდეგი ინსტრუქციები:
        1. პასუხი დააფუძნე **მხოლოდ** ქვემოთ მოცემულ კონტექსტზე.
        2. თუ კონტექსტში არ არის საკმარისი ინფორმაცია კითხვაზე პასუხის გასაცემად, სიტყვასიტყვით მიწერე: „მოცემულ დოკუმენტებში არ არის საკმარისი ინფორმაცია ამ კითხვაზე პასუხისთვის.“ და თავი შეიკავე ვარაუდებისგან.
        3. აუცილებლად მიუთითე წყაროები და მტკიცებულებები.
        4. თუ დოკუმენტებში შეამჩნევ ურთიერთგამომრიცხავ ინფორმაციას, აუცილებლად გამოკვეთე და მიუთითე კონფლიქტის შესახებ.
        
        კონტექსტი:
        {context_text}
        
        კითხვა:
        {query}
        
        პასუხი:
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"შეცდომა LLM სერვისთან კომუნიკაციისას: {str(e)}"