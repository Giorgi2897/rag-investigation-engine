from chunking_strategies import ChunkingHandler
from document_parser import DocumentParser
from duplicate_manager import DuplicateManager

class AddDocumentHandler:
    @staticmethod
    def execute(uploaded_file, db_manager):
        filename = uploaded_file.name
        
        # 1. ამოვტვირთავთ ტექსტსა და მეტამონაცემებს
        text, metadata = DocumentParser.extract_content(uploaded_file)
        
        if not text.strip():
            return False, f"ფაილი '{filename}' ცარიელია."

        # 2. ავტომატურად ვშლით ამავე სახელის (source) მქონე ძველ ჩანქერებს, 
        # რათა თავიდან ავიცილოთ დუბლიკატები და ძველი კოდის შენარჩუნება
        db_manager.delete_chunks_by_source(filename)

        # 3. ვქმნით უნიკალურ ID-ს, ვყოფთ ჩანქერებად და ვინახავთ ბაზაში
        doc_id = DuplicateManager.create_unique_id(text)
        chunks = ChunkingHandler.strategy_fixed_size(text)
        db_manager.add_chunks(chunks, metadata, doc_id)

        return True, f"დოკუმენტი '{filename}' წარმატებით დაემატა და განახლდა ბაზაში!"