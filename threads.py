import time
import urllib
from common import get_full_caption
from utils import api_call

CLIENT_ID = '13827354524027541'
CLIENT_SECRET = '157bb4df0428aa4b32e2e7f1a30f88621'
ACCESS_TOKEN = 'THQWJYWV9qZAi1US0lqTHdLVnRHczBYR3NkLXdRUnlBemZAOX0xaekVNYTZAIQVRRRmZAxVlZA6MmhPa1Y5RWY4ZAnJOR0VyTVRleWtqT1p5YW1aZAUdGOGJKdHJGd2llR2ZAibVVhaWtSb2NNVzUyV19ZASlpTMkdTVUlVOEI0ZA1EZD1'
USER_ID = '73063350828044971'


def upload_thread(video_path, title, caption, tags):
    if not video_path.startswith('http'):
        error_message = ("Meta Threads API supports only uploading video from public URL, "
                         "as https://file-examples.com/storage/fe0e5e78596682d89b36118/2017/04"
                         "/file_example_MP4_480_1_5MG.mp4")
        raise RuntimeError(error_message)
    text = get_full_caption(title, caption, tags)
    # upload message
    post_data = api_call(
        endpoint=f"https://graph.threads.net/v1.0/{USER_ID}/threads?"
                 f"media_type=VIDEO&"
                 f"video_url={video_path}&"
                 f"text={text}&"
                 f"access_token={ACCESS_TOKEN}",
        method='POST'
    )
    media_id = post_data.get('id')
    # would better check status
    while True:
        check_status = api_call(
            endpoint=f"https://graph.threads.net/v1.0/{media_id}?"
                     f"fields=status,error_message&"
                     f"access_token={ACCESS_TOKEN}")
        if check_status['status'] == 'IN_PROGRESS':
            time.sleep(1)
        elif check_status['status'] != 'FINISHED':
            raise RuntimeError(check_status)
        else:
            break
    # publish
    publish_data = api_call(
        endpoint=f"https://graph.threads.net/v1.0/{USER_ID}/"
                 f"threads_publish?creation_id={media_id}&"
                 f"access_token={ACCESS_TOKEN}",
        method='POST'
    )

    print(publish_data)

