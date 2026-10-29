class DeleteDocumentHandler:

  @staticmethod
  def execute(filename: str, db_manager):
    success = db_manager.delete_chunks_by_source(filename)
    if success:
      return True, f"ფაილი '{filename}' წარმატებით წაიშალა ბაზიდან."
    return False, "ფაილი ამ სახელით ვერ მოიძებნა ბაზაში."