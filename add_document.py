from chunking_strategies import ChunkingHandler
from document_parser import DocumentParser
from duplicate_manager import DuplicateManager


class AddDocumentHandler:

  @staticmethod
  def execute(uploaded_file, db_manager):
    text, metadata = DocumentParser.extract_content(uploaded_file)
    doc_id = DuplicateManager.create_unique_id(text)

    # დუბლიკატების შემოწმება
    if db_manager.check_document_exists(doc_id):
      return False, "ეს დოკუმენტი უკვე არსებობს ბაზაში (დუბლიკატი)."

    # ტექსტის დაყოფა ჩანქებად და ბაზაში შენახვა
    chunks = ChunkingHandler.strategy_fixed_size(text)
    db_manager.add_chunks(chunks, metadata, doc_id)

    return True, "დოკუმენტი წარმატებით დაემატა და დაინდექსდა!"