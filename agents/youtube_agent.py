# File: agents/youtube_agent.py

from langchain_core.runnables import RunnableLambda
from utils.youtube_utils import get_video_transcript, summarize_text


def youtube_handler(input_data: dict) -> dict:
    video_url = input_data.get("video_url")
    if not video_url:
        return {"response": "[YouTubeAgent] No video URL provided."}

    transcript = get_video_transcript(video_url)
    if not transcript:
        return {"response": "[YouTubeAgent] Could not retrieve transcript."}

    summary = summarize_text(transcript)
    return {"response": f"[YouTubeAgent] Summary: {summary}"}


YouTubeAgent = RunnableLambda(youtube_handler)