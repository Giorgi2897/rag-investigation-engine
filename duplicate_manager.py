import hashlib


class DuplicateManager:

  @staticmethod
  def generate_document_hash(text: str) -> str:
    """ტექსტის მიხედვით უნიკალური MD5 ჰეშის გენერაცია დუბლიკატების ასაცილებლად"""
    return hashlib.md5(text.encode("utf-8")).hexdigest()

  @staticmethod
  def create_unique_id(text: str) -> str:
    doc_hash = DuplicateManager.generate_document_hash(text)
    return f"doc_{doc_hash}"