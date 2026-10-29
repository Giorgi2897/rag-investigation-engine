from docx import Document
from pypdf import PdfReader


class DocumentParser:

  @staticmethod
  def extract_content(uploaded_file):
    filename = uploaded_file.name
    file_extension = filename.split(".")[-1].lower()
    text = ""
    metadata = {
        "source": filename,
        "format": file_extension,
        "size": uploaded_file.size,
    }

    if file_extension == "txt":
      text = uploaded_file.read().decode("utf-8", errors="ignore")
    elif file_extension == "pdf":
      reader = PdfReader(uploaded_file)
      for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
          text += extracted + "\n"
    elif file_extension == "docx":
      doc = Document(uploaded_file)
      for para in doc.paragraphs:
        text += para.text + "\n"
    else:
      raise ValueError("მხარდაუჭერელი ფაილის ფორმატი!")

    return text, metadata