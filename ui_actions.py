from chunking_strategies import ChunkingHandler
from document_parser import DocumentParser


class UIActionsHandler:

  @staticmethod
  def process_file_preview(uploaded_file):
    """ატვირთული ფაილის წინასწარი დამუშავება, მეტამონაცემებისა და

    Chunking შედარების გენერაცია ინტერფეისისთვის
    """
    text_preview, meta = DocumentParser.extract_content(uploaded_file)
    comparison = ChunkingHandler.compare_strategies(text_preview)
    return meta, comparison