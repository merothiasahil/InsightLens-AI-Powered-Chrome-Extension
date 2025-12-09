from flask import Blueprint, request, jsonify
from services import summarizer, sentiment, ocr, webscraper, transcript, wordcloud_gen, translator
import time

routes = Blueprint("routes", __name__)

@routes.route("/")
def home():
    return "InsightLens Backend Running!"


@routes.route("/summarize", methods=["POST"])
def summarize_route():
    start_time = time.time()

    data = request.json
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"error": "No text provided"}), 400

    summary = summarizer.generate_summary(text)
    elapsed_time = round(time.time() - start_time, 3)

    return jsonify({
        "summary": summary,
        "response_time_sec": elapsed_time
    })


@routes.route("/sentiment", methods=["POST"])
def sentiment_route():
    start_time = time.time()

    data = request.json
    text = data.get("text", "").strip()
    detailed = request.args.get("detailed", "false").lower() == "true"

    if not text:
        return jsonify({"error": "No text provided"}), 400

    result = sentiment.analyze_sentiment(text)

    if not detailed:
        result.pop("sentence_level", None)
        result.pop("distribution", None)

    result["response_time_sec"] = round(time.time() - start_time, 3)
    return jsonify(result)


@routes.route("/ocr", methods=["POST"])
def ocr_route():
    start_time = time.time()

    data = request.json
    base64_img = data.get("image", "").strip()

    if base64_img.startswith("data:image"):
        base64_img = base64_img.split(",")[1]

    result = ocr.extract_text_from_image_base64(base64_img)
    result["response_time_sec"] = round(time.time() - start_time, 3)
    return jsonify(result)


@routes.route("/analyze-image", methods=["POST"])
def analyze_image():
    start_time = time.time()

    data = request.json
    base64_img = data.get("image", "").strip()

    if base64_img.startswith("data:image"):
        base64_img = base64_img.split(",")[1]

    ocr_result = ocr.extract_text_from_image_base64(base64_img)
    if "error" in ocr_result:
        return jsonify({"error": "OCR failed"}), 400

    text = ocr_result["text"]
    summary = summarizer.generate_summary(text)
    sentiment_result = sentiment.analyze_sentiment(text)

    elapsed_time = round(time.time() - start_time, 3)

    return jsonify({
        "ocr_text": text,
        "summary": summary,
        "sentiment": sentiment_result,
        "response_time_sec": elapsed_time
    })


@routes.route("/wordcloud", methods=["POST"])
def wordcloud_route():
    start_time = time.time()

    data = request.json
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"error": "No text provided"}), 400

    result = wordcloud_gen.generate_wordcloud_base64(text)
    result["response_time_sec"] = round(time.time() - start_time, 3)
    return jsonify(result)


@routes.route("/analyze-url", methods=["POST"])
def analyze_url():
    start_time = time.time()

    data = request.json
    url = data.get("url", "").strip()

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    scraped = webscraper.scrape_article_text(url)
    if "error" in scraped:
        return jsonify(scraped), 400

    text = scraped["text"]
    summary = summarizer.generate_chunked_summary(text)
    sentiment_result = sentiment.analyze_sentiment(text)
    wordcloud_result = wordcloud_gen.generate_wordcloud_base64(text)

    elapsed_time = round(time.time() - start_time, 3)

    return jsonify({
        "url": url,
        "content": text,
        "summary": summary,
        "sentiment": sentiment_result,
        "wordcloud": wordcloud_result.get("image"),
        "response_time_sec": elapsed_time
    })


@routes.route("/analyze-youtube", methods=["POST"])
def analyze_youtube():
    start_time = time.time()

    data = request.json
    url = data.get("url", "").strip()

    transcript_data = transcript.get_youtube_transcript(url)
    if "error" in transcript_data:
        return jsonify(transcript_data), 400

    text = transcript_data["text"]

    if "।" in text or "है" in text:
        print("Hindi detected – translating...")
        text = translator.translate_hi_to_en(text)

    summary = summarizer.generate_summary(text)
    sentiment_result = sentiment.analyze_sentiment(text)
    wordcloud_result = wordcloud_gen.generate_wordcloud_base64(text)

    elapsed_time = round(time.time() - start_time, 3)

    return jsonify({
        "url": url,
        "transcript": text,
        "summary": summary,
        "sentiment": sentiment_result,
        "wordcloud": wordcloud_result.get("image"),
        "response_time_sec": elapsed_time
    })
