from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io
import base64

def generate_wordcloud_base64(text):
    try:
        wc = WordCloud(width=800, height=400, background_color='white').generate(text)
        
        # Save to BytesIO stream without using plt
        img_stream = io.BytesIO()
        wc.to_image().save(img_stream, format='PNG')
        
        # Encode image to base64
        img_stream.seek(0)
        base64_img = base64.b64encode(img_stream.read()).decode('utf-8')
        
        return {"image": base64_img}
    except Exception as e:
        return {"error": str(e)}