import requests
import os


def download_audio_from_playlist(playlist_url):
    try:
        # Fetch the playlist content
        response = requests.get(playlist_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        playlist_text = response.text

        print('got playlist file')

        # Extract base URL from the playlist URL
        base_url = playlist_url.rsplit('/', 1)[0] + '/'

        # Parse playlist and extract chunk URLs
        lines = playlist_text.split('\n')
        chunk_urls = [
            base_url + line for line in lines if line.endswith('.aac')
        ]

        # Fetch all chunks
        chunks = []
        print("fetching chunks")
        for index, url in enumerate(chunk_urls):
            chunk_response = requests.get(url)
            chunk_response.raise_for_status()
            chunks.append(chunk_response.content)
            print(chunk_response, index, "/", len(chunk_urls))

        # Combine chunks into a single byte array
        combined_chunks = b''.join(chunks)

        print("fetched all chunks")

        # Write the combined audio data to a file
        output_path = os.path.join(os.path.dirname(__file__),
                                   'combined_audio.aac')
        with open(output_path, 'wb') as file:
            file.write(combined_chunks)

        print('Download complete! File saved as', output_path)
    except requests.RequestException as e:
        print('Error downloading audio:', e)
