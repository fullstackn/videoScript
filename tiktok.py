import json
import os
import requests
from common import get_full_caption
from utils import api_call

ACCESS_TOKEN = 'act.UVnSLWjrFNfeV7IwSoykYQKKdzm7bt9jBE6WmfZ0yKR1PDL8StoXBWKBbDaC!5249.va'


def upload_ticktock(video_path, title, caption, tags):
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
                "disable_duet": False,
                "disable_comment": True,
                "disable_stitch": False,
                "video_cover_timestamp_ms": 1000
            },
        }
    post_data = api_call(
        endpoint=f'https://open.tiktokapis.com/v2/post/publish/video/init/',
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

        while check.json()['data']['status'] not in ['FAILED', 'PUBLISH_COMPLETE']:
            check = requests.post(
                url='https://open.tiktokapis.com/v2/post/publish/status/fetch/',
                json={'publish_id': publish_id},
                headers={'Authorization': f'Bearer {ACCESS_TOKEN}', 'Content-Type': 'application/json; charset=UTF-8'},
            )
            print(check.json())
        if check.json()['data']['status'] == 'FAILED':
            raise RuntimeError(check.json())


#upload_ticktock('v100.mp4', 'title', 'caption', ['t1','t2'])

