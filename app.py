import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Affiliate marketing tags
AFFILIATE_TAGS = {
    "google_cloud": "<affiliate-link>",
    "ai_tools": "<affiliate-link>"
}

# SEO and content generation prompt
prompt = """
आप एक कुशल लेखक हैं जिन्हें यूट्यूब वीडियो ट्रांसक्रिप्ट्स के आधार पर ब्लॉग सामग्री तैयार करने का कार्य सौंपा गया है। 
आपका लक्ष्य वीडियो में दी गई मुख्य जानकारी को आकर्षक और सूचनात्मक ब्लॉग पोस्ट में परिवर्तित करना है।

विशेष रूप से:

1. **प्रदान किए गए ट्रांसक्रिप्ट टेक्स्ट के आधार पर एक विस्तृत ब्लॉग पोस्ट तैयार करें।**
2. **ब्लॉग पोस्ट को पैराग्राफ में लिखें**, और सुनिश्चित करें कि यह पढ़ने में आसान और आकर्षक हो।
3. **ब्लॉग पोस्ट को 500 शब्दों तक सीमित रखें।**
4. **पाठकों के लिए वीडियो की सामग्री की संभावित प्रासंगिकता पर विचार करें।**
5. **प्रदान किए गए Google क्लाउड कंसोल क्रेडेंशियल्स छवि के संदर्भ में, यदि वीडियो क्लाउड कंप्यूटिंग, एआई या प्रौद्योगिकी से संबंधित किसी भी विषय पर चर्चा करता है, तो कृपया इन पहलुओं को ब्लॉग पोस्ट में उजागर करें।**
6. **यदि वीडियो में किसी भी उपकरण, सेवाओं या प्लेटफार्मों (जैसे Google क्लाउड) का उल्लेख किया गया है, तो कृपया उन्हें ब्लॉग पोस्ट में शामिल करें और उनका संक्षिप्त विवरण दें।**
7. **ब्लॉग पोस्ट को हिंदी भाषा में लिखें, और सुनिश्चित करें कि यह हिंदी भाषी पाठकों के लिए सांस्कृतिक रूप से प्रासंगिक हो।**
8. **ब्लॉग पोस्ट में एक आकर्षक शीर्षक और उपशीर्षक भी शामिल करें।**
9. **SEO के लिए -3 कीवर्ड शामिल करें और उन्हें प्राकृतिक रूप से पोस्ट में एम्बेड करें।**
10. **संबंधित तकनीकों के लिए एफिलिएट लिंक जोड़ें: {affiliate_tags}**
11. **AdSense के लिए प्लेसहोल्डर DIVs जोड़ें: <!-- ADSENSE_HEADER -->, <!-- ADSENSE_CONTENT -->, <!-- ADSENSE_FOOTER -->**
"""

# Function to extract YouTube transcript
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id, languages=["hi"])
        transcript = " ".join([item["text"] for item in transcript_text])
        return transcript
    except Exception as e:
        st.error(f"Error extracting transcript: {e}")
        return None

# Function to generate blog content using Gemini
def generate_blog_content(transcript_text):
    try:
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        full_prompt = prompt.format(affiliate_tags=AFFILIATE_TAGS)
        response = model.generate_content(full_prompt + transcript_text)
        return response.text
    except Exception as e:
        st.error(f"Error generating blog content: {e}")
        return None

# Streamlit UI
st.title("YouTube to Blog Automation 🚀")
youtube_link = st.text_input("Enter YouTube Video Link:")

if youtube_link:
    try:
        video_id = youtube_link.split("=")[1]
        st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)
    except Exception as e:
        st.error(f"Error displaying video thumbnail: {e}")

if st.button("Generate & Publish Blog"):
    if not youtube_link:
        st.warning("Please enter a YouTube link.")
    else:
        with st.spinner("Extracting transcript..."):
            transcript = extract_transcript_details(youtube_link)
        
        if transcript:
            with st.spinner("Generating blog content..."):
                blog_content = generate_blog_content(transcript)
            
            if blog_content:
                st.success("Blog generated successfully!")
                st.markdown("### Blog Preview:")
                st.write(blog_content)
            else:
                st.error("Failed to generate blog content.")
        else:
            st.error("Failed to extract transcript.")