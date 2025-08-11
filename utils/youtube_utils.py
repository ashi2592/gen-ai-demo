# File: utils/youtube_utils.py

from youtube_transcript_api import YouTubeTranscriptApi
from langchain_core.runnables import RunnableLambda
from langchain.chains.summarize import load_summarize_chain
from langchain_groq import ChatGroq
from langchain.docstore.document import Document


def get_video_transcript(video_id: str) -> str:
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        full_text = " ".join([entry["text"] for entry in transcript])
        return full_text
    except Exception as e:
        return f"Error fetching transcript: {e}"


def summarize_text(text: str) -> str:
    try:
        docs = [Document(page_content=text)]
        llm = ChatGroq(temperature=0.3, model_name="llama3-8b-8192")
        chain = load_summarize_chain(llm, chain_type="stuff")
        summary = chain.run(docs)
        return summary
    except Exception as e:
        return f"Error summarizing text: {e}"


# Example usage with Runnable
summarize_transcript_runnable = RunnableLambda(lambda x: summarize_text(get_video_transcript(x["video_id"])))
