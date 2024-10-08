import requests
import urllib.parse
import json


def get_playlist(id: str, token: str, cookies: str) -> str:
    try:
        print('trying', id)

        base_url = "https://x.com/i/api/graphql/juwWgLbJVtGm3VpBm0GA3g/AudioSpaceById"

        # Query parameters
        variables = {
            "id": id,
            "isMetatagsQuery": False,  # Change "false" to False (boolean)
            "withReplays": True,  # Change "true" to True (boolean)
            "withListeners": True  # Change "true" to True (boolean)
        }

        features = {
            "spaces_2022_h2_spaces_communities":
            True,
            "spaces_2022_h2_clipping":
            True,
            "creator_subscriptions_tweet_preview_api_enabled":
            True,
            "rweb_tipjar_consumption_enabled":
            True,
            "responsive_web_graphql_exclude_directive_enabled":
            True,
            "verified_phone_label_enabled":
            False,
            "communities_web_enable_tweet_community_results_fetch":
            True,
            "c9s_tweet_anatomy_moderator_badge_enabled":
            True,
            "articles_preview_enabled":
            True,
            "responsive_web_graphql_skip_user_profile_image_extensions_enabled":
            False,
            "responsive_web_edit_tweet_api_enabled":
            True,
            "graphql_is_translatable_rweb_tweet_is_translatable_enabled":
            True,
            "view_counts_everywhere_api_enabled":
            True,
            "longform_notetweets_consumption_enabled":
            True,
            "responsive_web_twitter_article_tweet_consumption_enabled":
            True,
            "tweet_awards_web_tipping_enabled":
            False,
            "creator_subscriptions_quote_tweet_preview_enabled":
            False,
            "freedom_of_speech_not_reach_fetch_enabled":
            True,
            "standardized_nudges_misinfo":
            True,
            "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":
            True,
            "rweb_video_timestamps_enabled":
            True,
            "longform_notetweets_rich_text_read_enabled":
            True,
            "longform_notetweets_inline_media_enabled":
            True,
            "responsive_web_graphql_timeline_navigation_enabled":
            True,
            "responsive_web_enhance_cards_enabled":
            False
        }

        # Convert variables and features to JSON strings without encoding booleans as strings
        json_variables = json.dumps(variables).replace(" ", "")
        json_features = json.dumps(features).replace(" ", "")

        # Safely encode the JSON strings without unnecessary percent encoding
        encoded_variables = urllib.parse.quote(json_variables)
        encoded_features = urllib.parse.quote(json_features)

        # Construct the full URL
        request_url = f"{base_url}?variables={encoded_variables}&features={encoded_features}"

        # Headers
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/x-www-form-urlencoded",
            #"Content-Length": "242",
            "Cookie": cookies,
            #"Livepipeline-Session": "2ed324af-5d2c-44aa-96ef-4daace5d025c",
            "Origin": "https://x.com",
            "Priority": "u=1, i",
            "Referer": "https://x.com/",
            "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Linux"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent":
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "X-Client-Transaction-Id":
            "W8ocYdL19QXt+nLvJ2RJnVzK0g4qg8kevSFnW5FGYujJH/aYK4e7Z9wGetdLV41pNC52K1nMkKeKeswnRIayQr5CgOenWA",
            "X-Client-Uuid": "8acfbd1d-cfad-469b-a7a9-807d9cf016c9",
            "X-Csrf-Token":
            "32338dfd36dd5ac0127716824543ef9a66985edbe54d1a9c752b43399475c42d60040e445eae39b736dc441a6d82a9a9382811b2304dd93b940bddc61cc7ccc1605f95f4a73629753fb04e9b9e4338db",
            "X-Twitter-Active-User": "yes",
            "X-Twitter-Auth-Type": "OAuth2Session",
            "X-Twitter-Client-Language": "en",
        }

        # Make the request
        print('requesting')
        response = requests.get(request_url, headers=headers)
        print('got response', response.text)
        print('headers', response.headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        response_data = response.json()
        print("Server responded", response.status_code)
        print("Media key",
              response_data['data']['audioSpace']['metadata']['media_key'])
        media_key = response_data['data']['audioSpace']['metadata'][
            'media_key']

        # Fetch the playlist URL
        video_stream_response = requests.get(
            f"https://x.com/i/api/1.1/live_video_stream/status/{media_key}?client=web&use_syndication_guest_id=false&cookie_set_host=x.com",
            headers=headers)
        video_stream_data = video_stream_response.json()

        return video_stream_data['source']['location']

    except requests.RequestException as e:
        print('Error fetching playlist:', e)
        return None
