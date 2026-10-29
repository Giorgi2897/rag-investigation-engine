from chunking_strategies import ChunkingHandler
from document_parser import DocumentParser
from duplicate_manager import DuplicateManager


class UpdateDocumentHandler:

  @staticmethod
  def execute(uploaded_file, db_manager):
    filename = uploaded_file.name

    # განახლება ნიშნავს: ჯერ ვწაშლით ამ ფაილის ძველ ჩანქერებს
    db_manager.delete_chunks_by_source(filename)

    # შემდეგ ვამატებთ ახალი ტექსტით განახლებულ ვერსიას
    text, metadata = DocumentParser.extract_content(uploaded_file)
    doc_id = DuplicateManager.create_unique_id(text)
    chunks = ChunkingHandler.strategy_fixed_size(text)
    db_manager.add_chunks(chunks, metadata, doc_id)

    return True, f"დოკუმენტი '{filename}' წარმატებით განახლდა!"