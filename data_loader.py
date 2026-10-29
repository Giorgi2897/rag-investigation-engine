import chromadb
from datasets import load_dataset


def init_vector_db():
  # ვქმნით მუდმივ ვექტორულ ბაზას დისკზე
  client = chromadb.PersistentClient(path="./chroma_db")
  collection = client.get_or_create_collection(name="hotpot_investigation_1000")

  if collection.count() == 0:
    print("მონაცემთა ბაზის ჩამოტვირთვა და ინდექსაცია იწყება...")
    dataset = load_dataset(
        "hotpotqa/hotpot_qa", "distractor", split="train", streaming=True
    )

    documents = []
    metadatas = []
    ids = []

    count = 0
    for item in dataset:
      if count >= 1000:
        break

      context_data = item["context"]
      context_text = ""

      if isinstance(context_data, dict):
        titles = context_data.get("title", [])
        sent_lists = context_data.get("sentences", [])
        for title, sentences in zip(titles, sent_lists):
          joined_sentences = (
              "".join(sentences)
              if isinstance(sentences, list)
              else str(sentences)
          )
          context_text += f"სათაური: {title}\nტექსტი: {joined_sentences}\n\n"
      elif isinstance(context_data, list):
        for block in context_data:
          if len(block) >= 2:
            title = block[0]
            sentences = block[1]
            joined_sentences = (
                "".join(sentences)
                if isinstance(sentences, list)
                else str(sentences)
            )
            context_text += f"სათაური: {title}\nტექსტი: {joined_sentences}\n\n"

      documents.append(context_text)
      metadatas.append(
          {
              "question": str(item["question"]),
              "answer": str(item["answer"]),
          }
      )
      ids.append(str(item["id"]))
      count += 1

    collection.add(documents=documents, metadatas=metadatas, ids=ids)
    print(f"წარმატებით ჩაიტვირთვა და დაინდექსდა {count} ჩანაწერი ბაზაში!")
  else:
    print("მონაცემთა ბაზა უკვე არსებობს და მზადაა სამუშაოდ!")


if __name__ == "__main__":
  init_vector_db()