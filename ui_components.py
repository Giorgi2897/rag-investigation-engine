from chunking_strategies import ChunkingHandler
from document_parser import DocumentParser
import streamlit as st


def render_sidebar(engine):
  """მთლიანი Sidebar ლოგიკა (დოკუმენტების დამატება, განახლება, წაშლა)"""
  st.sidebar.header("📁 დოკუმენტების მართვა")

  action_type = st.sidebar.selectbox(
      "აირჩიეთ ოპერაცია", ["დოკუმენტის დამატება", "დოკუმენტის განახლება"]
  )

  uploaded_file = st.sidebar.file_uploader(
      "ატვირთეთ ფაილი (.txt, .pdf, .docx)", type=["txt", "pdf", "docx"]
  )

  if uploaded_file is not None:
    text_preview, meta = DocumentParser.extract_content(uploaded_file)
    comparison = ChunkingHandler.compare_strategies(text_preview)

    if action_type == "დოკუმენტის დამატება":
      if st.sidebar.button("ბაზაში დამატება"):
        with st.spinner("მიმდინარეობს დოკუმენტის ინდექსაცია..."):
          success, msg = engine.add_document(uploaded_file)
          if success:
            st.sidebar.success(msg)
            st.sidebar.info(
                f"📊 **მეტამონაცემები:**\n- სახელი: {meta['source']}\n- ფორმატი:"
                f" {meta['format'].upper()}\n- ზომა: {meta['size']} bytes"
            )
            st.sidebar.write("---")
            st.sidebar.write("⚙️ **Chunking შედარება:**")
            st.sidebar.write(
                f"სტრატეგია A (ჩანქების რაოდენობა):"
                f" {comparison['strategy_a_count']}"
            )
            st.sidebar.write(
                f"სტრატეგია B (ჩანქების რაოდენობა):"
                f" {comparison['strategy_b_count']}"
            )
          else:
            st.sidebar.warning(msg)

    elif action_type == "დოკუმენტის განახლება":
      if st.sidebar.button("დოკუმენტის განახლება"):
        with st.spinner("მიმდინარეობს დოკუმენტის განახლება..."):
          success, msg = engine.update_document(uploaded_file)
          if success:
            st.sidebar.success(msg)
            st.sidebar.info(
                f"📊 **ახალი მეტამონაცემები:**\n- სახელი: {meta['source']}\n-"
                f" ფორმატი: {meta['format'].upper()}\n- ზომა: {meta['size']}"
                " bytes"
            )
          else:
            st.sidebar.error(msg)

  # დოკუმენტის წაშლის სექცია
  st.sidebar.write("---")
  st.sidebar.subheader("🗑️ დოკუმენტის წაშლა")
  file_to_delete = st.sidebar.text_input(
      "ჩაწერეთ წასაშლელი ფაილის სახელი (მაგ: report.pdf):"
  )
  if st.sidebar.button("ბაზიდან წაშლა"):
    if file_to_delete:
      success, msg = engine.delete_document(file_to_delete)
      if success:
        st.sidebar.success(msg)
      else:
        st.sidebar.error(msg)
    else:
      st.sidebar.warning("გთხოვთ, ჩაწეროთ ფაილის ზუსტი სახელი.")


def render_main_search(engine):
  """მთავარი ფანჯრის ლოგიკა (ძიება და გენერაცია)"""
  st.write("---")
  user_query = st.text_input(
      "🔍 დასვი კითხვა ატვირთული დოკუმენტებიდან:",
      placeholder="Enter your question here...",
  )

  if user_query:
    with st.spinner("მიმდინარეობს სემანტიკური ძიება და გენერაცია..."):
      ai_answer, retrieved_docs, sources = engine.search_and_generate(user_query)

      st.subheader("💡 Gemini-ს გენერირებული პასუხი:")
      st.success(ai_answer)

      st.subheader("📌 გამოყენებული მტკიცებულებები და წყაროები:")
      if retrieved_docs:
        for i, (doc, src) in enumerate(zip(retrieved_docs, sources), 1):
          source_name = (
              src.get("source", "Unknown") if isinstance(src, dict) else "Unknown"
          )
          file_fmt = (
              src.get("format", "txt").upper()
              if isinstance(src, dict)
              else "TXT"
          )
          st.info(
              f"**წყარო #{i} | ფაილი: {source_name} (ფორმ.: {file_fmt}):**\n\n{doc}"
          )
      else:
        st.warning("რელევანტური წყაროები ვერ მოიძებნა.")