from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled
from urllib.parse import urlparse, parse_qs

def extract_video_id(url):
    try:
        parsed = urlparse(url)
        if parsed.hostname == 'youtu.be':
            return parsed.path[1:]
        if parsed.hostname in ['www.youtube.com', 'youtube.com']:
            return parse_qs(parsed.query)['v'][0]
        return None
    except Exception:
        return None

def get_youtube_transcript(url):
    try:
        video_id = extract_video_id(url)
        if not video_id:
            return {"error": "Invalid YouTube URL"}

        transcripts = YouTubeTranscriptApi.list_transcripts(video_id)

        # Try manual English
        try:
            transcript = transcripts.find_transcript(['en'])
        except:
            # Try auto English
            try:
                transcript = transcripts.find_generated_transcript(['en'])
            except:
                # Fallback: use any first transcript (e.g., Hindi)
                try:
                    transcript = list(transcripts)[0]  # pick first available
                except:
                    return {"error": "No usable transcript found"}

        text = " ".join([entry.text for entry in transcript.fetch()])
        return {"text": text.strip()}

    except (NoTranscriptFound, TranscriptsDisabled):
        return {"error": "Transcript not available for this video."}
    except Exception as e:
        return {"error": str(e)}
