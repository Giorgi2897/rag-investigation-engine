from chunking_strategies import ChunkingHandler
from document_parser import DocumentParser
from duplicate_manager import DuplicateManager

class UpdateDocumentHandler:
    @staticmethod
    def execute(uploaded_file, db_manager):
        filename = uploaded_file.name

        # 1. ამოვტვირთავთ ახალ ტექსტსა და მეტამონაცემებს
        text, metadata = DocumentParser.extract_content(uploaded_file)
        
        if not text.strip():
            return False, f"ფაილი '{filename}' ცარიელია."

        # 2. ჯერ ვწაშლით ამ ფაილის ძველ ჩანქერებს სახელის (source) მიხედვით
        db_manager.delete_chunks_by_source(filename)

        # 3. ვამატებთ ახალი ტექსტით განახლებულ ვერსიას
        doc_id = DuplicateManager.create_unique_id(text)
        chunks = ChunkingHandler.strategy_fixed_size(text)
        db_manager.add_chunks(chunks, metadata, doc_id)

        return True, f"დოკუმენტი '{filename}' წარმატებით განახლდა!"