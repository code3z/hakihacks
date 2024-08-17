from download_audio import download_audio_from_playlist
from get_playlist import get_playlist
import whisper
import os
from dotenv import load_dotenv

load_dotenv()

# Example usage
audio_space_id = "1rmxPolzXaDJN"
bearer_token = os.getenv("BEARER_TOKEN")

print(os.getenv('AUTH_TOKEN'))

# Separate cookies
cookies = [
    f"auth_token={os.getenv('AUTH_TOKEN')}",
    f"ct0={os.getenv('CT0')}",
]

cookies_string = "; ".join(cookies)


def main():
    try:
        # Fetch playlist URL
        playlist_url = get_playlist(audio_space_id, bearer_token,
                                    cookies_string)

        print(f"Got playlist URL: {playlist_url}")

        if playlist_url == None:
            raise ValueError("Playlist URL is None")

        # Download audio from playlist
        download_audio_from_playlist(playlist_url)
        
        model = whisper.load_model("base")
        result = model.transcribe("combined_audio.aac")
        
        print(result["text"])


    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
