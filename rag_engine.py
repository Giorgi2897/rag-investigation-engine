from add_document import AddDocumentHandler
from delete_document import DeleteDocumentHandler
from llm_service import LLMService
from update_document import UpdateDocumentHandler
from vector_database import VectorDatabaseManager


class InvestigationEngine:

  def __init__(self):
    self.db_manager = VectorDatabaseManager()
    self.llm_service = LLMService(db_manager=self.db_manager)

  def add_document(self, uploaded_file):
    return AddDocumentHandler.execute(uploaded_file, self.db_manager)

  def update_document(self, uploaded_file):
    return UpdateDocumentHandler.execute(uploaded_file, self.db_manager)

  def delete_document(self, filename: str):
    return DeleteDocumentHandler.execute(filename, self.db_manager)

  def search_and_generate(self, user_query: str):
    try:
      safe_query = (
          str(user_query).encode("utf-8", errors="ignore").decode("utf-8")
      )
      retrieved_docs, sources = self.db_manager.similarity_search(
          safe_query, n_results=5
      )

      context_text = "\n\n".join(retrieved_docs)
      ai_answer = self.llm_service.generate_investigation_answer(
          safe_query, context_text
      )

      return ai_answer, retrieved_docs, sources
    except Exception as e:
      return f"შეცდომა: {str(e)}", [], []