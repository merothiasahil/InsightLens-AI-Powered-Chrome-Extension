from transformers import MarianMTModel, MarianTokenizer

# Load Hindi to English model
model_name = "Helsinki-NLP/opus-mt-hi-en"
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

def translate_hi_to_en(text):
    try:
        inputs = tokenizer([text], return_tensors="pt", truncation=True, padding=True)
        translated = model.generate(**inputs)
        result = tokenizer.batch_decode(translated, skip_special_tokens=True)
        return result[0]
    except Exception as e:
        return f"Translation error: {str(e)}"
