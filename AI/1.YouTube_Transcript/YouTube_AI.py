from youtube_transcript_api import YouTubeTranscriptApi
import os
import google.generativeai as genai

# Set up Google AI API key

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("Please set the GOOGLE_API_KEY environment variable.")
# genai.configure(api_key=GOOGLE_API_KEY)
genai.configure(api_key="YourAPIKey")

# https://www.youtube.com/watch?v=ZQDL4EnvL8s

def extract_video_id(url):
    """Extracts the video ID from various YouTube URL formats."""
    if "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    elif "watch?v=" in url:
        return url.split("watch?v=")[1].split("&")[0]
    else:
        raise ValueError("Invalid YouTube URL format.")


def get_transcript(video_id):
    """Fetches the YouTube video transcript in the user's preferred language."""
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

    available_languages = [
        (transcript.language_code, transcript.language)
        for transcript in transcript_list
    ]

    print("\nAvailable transcript languages:")
    for i, (code, lang) in enumerate(available_languages):
        print(f"{i + 1}. {lang} ({code})")

    while True:
        try:
            choice = int(input("\nEnter the number of your desired language: "))
            selected_language_code = available_languages[choice - 1][0]
            break
        except (ValueError, IndexError):
            print("Invalid input. Please enter a valid number.")

    try:
        transcript = transcript_list.find_transcript([selected_language_code])
        transcript_text = transcript.fetch()

        # return "\n".join(item['text'] for item in transcript_text)
        return transcript_text

    except Exception as e:
        print(f"An error occurred fetching the transcript: {e}")
        return None


def chat_about_video(transcript):
    """Initiates a chat with the language model, providing the transcript as context."""
    model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")
    chat = model.start_chat(history=[])

    # You may want to improve how the transcript is fed to the model
    # For example, break it down into smaller chunks or summarize it


    # chat.send_message(f"Here's a transcript of a YouTube video:\n{transcript}")
    chat.send_message(f"I have access to the transcript of a YouTube video. Transcript: {transcript}")  # Provide context to the model


    while True:
        user_input = input(
            "\n\nEnter your question about the video (or type 'quit' to stop):\n"
        )
        if user_input.lower() == "quit":
            break

        response = chat.send_message(user_input)
        for message in response:
            for part in message.parts:
                print(part.text, end="", flush=True)


def main():
    video_url = input("Enter the YouTube video URL: ")
    try:
        video_id = extract_video_id(video_url)
        transcript = get_transcript(video_id)

        if transcript:
            chat_about_video(transcript)

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()