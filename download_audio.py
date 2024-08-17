import requests
import os
import concurrent.futures

def fetch_chunk(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.content

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
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Map the fetch_chunk function to the chunk URLs
            results = list(executor.map(fetch_chunk, chunk_urls))

            for index, content in enumerate(results):
                chunks.append(content)
                print("Fetched chunk", index + 1, "/", len(chunk_urls))

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
