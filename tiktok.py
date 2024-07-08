import json
import os
import requests
from common import get_full_caption
from utils import api_call


ACCESS_TOKEN = 'act.HciU22WO9PhQzUNvZ0sHKLZftbO2PSCx7ggivP1wx5VjTjD7Dgsnk5uT1Xzn!5204.va'


def upload_thread(video_path, title, caption, tags):
    text = get_full_caption(title, caption, tags)
    file_size = os.path.getsize(video_path)
    chunk_size = file_size
    total_chunk_count = int(file_size / chunk_size)
    data = {
            "source_info": {
                "source": "FILE_UPLOAD",
                "video_size": file_size,
                "chunk_size": chunk_size,
                "total_chunk_count": total_chunk_count,
            },
            "post_info": {
                "title": text,
                "privacy_level": "PUBLIC_TO_EVERYONE",
                "disable_duet": 'false',
                "disable_comment": 'true',
                "disable_stitch": 'false',
                "video_cover_timestamp_ms": 1000
            },
        }
    post_data = api_call(
        endpoint='https://open.tiktokapis.com/v2/post/publish/inbox/video/init/',
        data=json.dumps(data),
        headers={'Authorization': f'Bearer {ACCESS_TOKEN}', 'Content-Type': 'application/json; charset=UTF-8'},
        method='POST'
    )
    with open(video_path, 'rb') as f:
        upload_url = post_data.get('data').get('upload_url')
        publish_id = post_data.get('data').get('publish_id')
        upload_data = requests.put(
            url=upload_url,
            data=f,
            headers={
                'Content-Type': 'video/mp4',
                'Content-Length': str(chunk_size),
                'Content-Range': f'bytes 0-{file_size-1}/{file_size}',
                     }
        )
        print(f'{upload_data=}')
        check = requests.post(
            url='https://open.tiktokapis.com/v2/post/publish/status/fetch/',
            json={'publish_id': publish_id},
            headers={'Authorization': f'Bearer {ACCESS_TOKEN}', 'Content-Type': 'application/json; charset=UTF-8'},
        )
        print(check)

upload_thread('v100.mp4', 'title', 'caption', ['t1','t2'])

