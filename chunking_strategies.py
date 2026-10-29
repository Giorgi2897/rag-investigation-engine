class ChunkingHandler:

  @staticmethod
  def strategy_fixed_size(text, chunk_size=500, overlap=50):
    """სტრატეგია A: ფიქსირებული სიმბოლოების ზომაზე დაფუძნებული ჩანქინგი"""
    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
      chunks.append(text[i : i + chunk_size])
    return chunks

  @staticmethod
  def strategy_extended_size(text, chunk_size=800, overlap=100):
    """სტრატეგია B: გაფართოებული ზომის/აბზაცებზე დაფუძნებული ჩანქინგი"""
    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
      chunks.append(text[i : i + chunk_size])
    return chunks

  @classmethod
  def compare_strategies(cls, text):
    """ორივე სტრატეგიის შედარება და მეტრიკების დაბრუნება"""
    chunks_a = cls.strategy_fixed_size(text)
    chunks_b = cls.strategy_extended_size(text)
    return {
        "strategy_a_count": len(chunks_a),
        "strategy_b_count": len(chunks_b),
        "sample_a": chunks_a[0] if chunks_a else "",
        "sample_b": chunks_b[0] if chunks_b else "",
    }