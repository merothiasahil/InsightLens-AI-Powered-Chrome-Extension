from transformers import pipeline, AutoTokenizer


summarizer_pipeline = pipeline("summarization", model="facebook/bart-large-cnn")
tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")

def generate_summary(text):
    if not text or len(text.strip()) < 30:
        return "Not enough content to summarize."

 
    tokens = tokenizer(text, return_tensors="pt", truncation=True)
    token_count = len(tokens["input_ids"][0])
    print(f"Token count: {token_count}")

    if token_count < 80:
        max_len, min_len = 50, 15
    elif token_count < 200:
        max_len, min_len = 100, 25
    elif token_count < 400:
        max_len, min_len = 160, 40
    else:
        max_len, min_len = 200, 60

    #Run summarization
    summary = summarizer_pipeline(
        text,
        max_length=max_len,
        min_length=min_len,
        do_sample=False
    )

    return summary[0]["summary_text"]

def split_text(text, max_tokens=450):
    sentences = text.split(". ")
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len((current_chunk + sentence).split()) <= max_tokens:
            current_chunk += sentence + ". "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + ". "

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def generate_chunked_summary(text):
    chunks = split_text(text)
    summaries = []

    for chunk in chunks:
        try:
            summary = summarizer_pipeline(
                chunk,
                max_length=130,
                min_length=30,
                do_sample=False
            )
            summaries.append(summary[0]['summary_text'])
        except Exception as e:
            summaries.append(f"[Chunk failed] {str(e)}")

    return " ".join(summaries)


