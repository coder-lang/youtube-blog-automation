import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

def generate_blog(youtube_link):
    try:
        # Extract transcript
        video_id = youtube_link.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id, languages=["hi"])
        transcript = " ".join([item["text"] for item in transcript_text])

        # Generate blog
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        prompt = """
        आप एक कुशल लेखक हैं जिन्हें यूट्यूब वीडियो ट्रांसक्रिप्ट्स के आधार पर ब्लॉग सामग्री तैयार करने का कार्य सौंपा गया है। 
        आपका लक्ष्य वीडियो में दी गई मुख्य जानकारी को आकर्षक और सूचनात्मक ब्लॉग पोस्ट में परिवर्तित करना है।
        """
        response = model.generate_content(prompt + transcript)
        return {"blogContent": response.text}
    except Exception as e:
        return {"error": str(e)}