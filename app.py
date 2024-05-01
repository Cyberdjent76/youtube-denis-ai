import streamlit as st
import requests
import json
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
from pytube import YouTube


st.title("Denis the YouTube AI Assistant")

def get_video_title(youtube_url):
    try:
        # Create a YouTube object
        yt = YouTube(youtube_url)
        
        # Get the video title
        video_title = yt.title
        return video_title

    except Exception as e:
        return f"An error occurred: {e}"


with st.sidebar:
    youtube_url = st.text_input("Enter a YouTube URL")

# transcript = ""



# Parse the URL
if youtube_url:
    with st.sidebar:
        parsed_url = urlparse(youtube_url)

        video_title = get_video_title(youtube_url)

        st.video(youtube_url)
        st.markdown(f"# {video_title}")
        st.markdown("Wanna learn how to build this app yourself? [Click here](https://gamma.app/docs/Do-you-want-to-build-apps-and-make-money-with-AI-ChatGPT-in-8-wee-ru4joc3qr17h336)")

        # Parse the query parameters
        query_parameters = parse_qs(parsed_url.query)

        # Extract the video ID
        video_id = query_parameters.get("v")[0]
        
        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        # st.write(video_id)

        # Initialize an empty string to hold the concatenated text
        transcript_text = ""

        # Loop through each dictionary in the list
        for item in transcript:
            # Append the text to the concatenated_text string with a space in between
            transcript_text += item["text"] + " "

        # Remove the trailing space at the end
        transcript_text = transcript_text.rstrip()

    # st.write(transcript_text)

    # https://img.youtube.com/vi/UwiBxdT6_20/0.jpg

    def hit_relevance_ai(transcript, prompt):
        # spinner start
        # st.spinner(text="In progress...")
        with st.spinner(text="Denis is thinking..."):
            url = "https://api-d7b62b.stack.tryrelevance.com/latest/studios/891bd682-3f71-4f29-8536-d86c499cdf5b/trigger_limited"
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            payload = {
                "params": {
                    "transcript": transcript,
                    "prompt": prompt
                },
                "project": "25496be1b835-45f7-b24f-cf730e92ddba"
            }
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            # spinner end
            # st.success('Done!')
            if response.status_code == 200:
                return response.json()["output"]["answer"]
            else:
                return f"Error {response.status_code}: {response.text}"

    if 'messages' not in st.session_state:
        st.session_state.messages = []

  
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    

    if prompt := st.chat_input("What is up?"):
        user_message = {'role': 'user', 'content': prompt}
        st.session_state.messages.append(user_message)
        with st.chat_message("user"):
            st.markdown(prompt)

        ai_response = hit_relevance_ai(transcript_text, prompt)
        assistant_message = {'role': 'assistant', 'content': ai_response}
        
        st.session_state.messages.append(assistant_message)

        with st.chat_message("assistant"):
            st.markdown(ai_response)
        
        # for message in st.session_state.messages[-2:]:  # Show only the last two messages (user and assistant)
        #     with st.chat_message(message["role"]):
        #         st.markdown(message["content"])
