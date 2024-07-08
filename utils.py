from datetime import datetime, timedelta
import os
import time
import requests

from common import get_full_caption
from twitter import upload_tweet

INTERVAL = 60
BASE_URL = 'https://graph.facebook.com/v20.0'
PERMANENT_USER_ACCESS_TOKEN = os.environ.get('USER_FB_TOKEN')


def api_call(endpoint, data=None, method='GET', headers=None, files=None):
    if endpoint.startswith('http'):
        url = endpoint
    else:
        url = f'{BASE_URL}/{endpoint}'
    if method == 'GET':
        response = requests.get(url, data=data, headers=headers)
    else:
        response = requests.post(url, data=data, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise RuntimeError(f'wrong result /n{response.text}')


def get_page_attributes(user_access_token):
    # get page ID
    accounts = api_call(
        endpoint=f'me?fields=accounts&access_token={user_access_token}',
        method='GET'
    )
    page_id = accounts['accounts']['data'][0]['id']
    print(f'get page {page_id=}')
    # get page_access_token
    page = api_call(endpoint=f'{page_id}?fields=access_token&access_token={user_access_token}')
    page_access_token = page['access_token']
    print(f'{page_access_token=}')
    return {'access_token': page_access_token, 'id': page_id}


def get_instagram_id(page):
    # get instagram_business_account ID
    instagram = api_call(f"{page.get('id')}?"
                         f"fields=instagram_business_account&"
                         f"access_token={page.get('access_token')}")
    instagram_business_account = instagram['instagram_business_account']['id']
    print(f'{instagram_business_account=}')
    return instagram_business_account


def upload_instagram_reel(
        user_access_token,
        file_path,
        title=None,
        caption=None,
        tags=None
):
    full_caption = get_full_caption(title, caption, tags)
    page = get_page_attributes(user_access_token)
    access_token = page.get('access_token')
    instagram_id = get_instagram_id(page)
    # upload video
    r = api_call(endpoint=f"{instagram_id}/media?access_token={access_token}",
                 data={
                     'video_url': file_path,
                     'media_type': "REELS",
                     'access-token': access_token,
                     'upload_type': "resumable",
                     'caption': full_caption,
                 },
                 method='POST'
                 )
    media_container_id = r['id']
    print(f'create container {media_container_id=}')
    print(f'upload start')
    with open(file_path, 'rb') as payload:
        upload_request = api_call(
            endpoint=f"https://rupload.facebook.com/ig-api-upload/v20.0/{media_container_id}?"
                     f"access_token={access_token}",
            headers={
                "Authorization": f'OAuth {access_token}',
                "offset": '0',
                "file_size": str(os.path.getsize(file_path)),
            },
            data=payload,
            method='POST'
        )
    print(f'upload done {upload_request=}')

    # publish video
    print(f'publish start')
    publish = api_call(
        endpoint=f'{instagram_id}/media_publish?'
                 f'creation_id={media_container_id}&'
                 f'access_token={access_token}',
        method='POST'
    )
    print(f'publish done {publish=}')


def upload_facebook_reel(
        user_access_token,
        file_path,
        title=None,
        caption=None,
        tags=None
):
    full_caption = get_full_caption(title, caption, tags)
    fb_page = get_page_attributes(user_access_token)
    access_token = fb_page.get('access_token')
    page_id = fb_page.get('id')
    # prepare upload (create container)
    start_upload = api_call(
        endpoint=f'{page_id}/video_reels?access_token={access_token}',
        method='POST',
        data={
            "upload_phase": "start",
            "access_token": f'{access_token}'
        }
    )
    video_id = start_upload['video_id']
    upload_url = start_upload.get('upload_url')

    # upload file
    with open(file_path, 'rb') as payload:
        api_call(
            endpoint=upload_url + "?access_token={access_token}",
            method='POST',
            data=payload,
            headers={
                "Authorization": f'OAuth {access_token}',
                "offset": '0',
                "file_size": str(os.path.getsize(file_path)),
            }
       )
    # publish reel
    api_call(
        endpoint=f'{page_id}/video_reels?access_token={access_token}',
        method='POST',
        data={
            'access_token': access_token,
            'video_id': video_id,
            'upload_phase': 'finish',
            'video_state': 'PUBLISHED',
            'description': full_caption
        },
    )
    limit = 100
    t = time.time()
    while True:
        limit -= 1
        response_status = api_call(endpoint=f"{video_id}?fields=status&access_token={access_token}")
        if limit <= 0:
            raise RuntimeError(response_status)
        stages = ['uploading_phase', 'processing_phase', 'publishing_phase', 'copyright_check_status']
        if response_status['status']['publishing_phase']['status'] == 'complete':
            print('published')
            break
        else:
            print(f'=============================={time.time()-t=}=============')
            if response_status['status']['processing_phase']['status'] == 'error':
                raise RuntimeError(response_status['status']['processing_phase']['errors'][0]['message'])
            for stage in stages:
                if response_status['status'][stage]['status'] == 'error':
                    raise RuntimeError(response_status['status'][stage])
                if response_status['status'][stage]['status'] not in ['complete', 'not_started']:
                    print(f"incomplete {stage}={response_status['status'][stage]=}")
        time.sleep(10)


def run_videos(videos, destination='facebook'):
    plain_info = []
    for lang in videos:
        for i in range(len(videos[lang])):
            plain_info.append(videos[lang][i])
            if plain_info[-1]['video_date'] is None:
                dt_value = datetime.now()
            else:
                dt_value = datetime.strptime(plain_info[-1]['video_date'], '%Y-%m-%dT%H:%M:%SZ')
            plain_info[-1]['video_date'] = dt_value
    sorted_plain_info = sorted(plain_info, key=lambda video: video['video_date'])

    t_start = time.time()
    errors_count = 0
    while len(sorted_plain_info) > 0:
        video = sorted_plain_info[0]
        if datetime.now() >= video['video_date']:
            try:
                print(f'upload {video=} START')
                if destination == 'facebook':
                    upload_facebook_reel(
                        PERMANENT_USER_ACCESS_TOKEN,
                        video.get('video_file_path'),
                        title=video.get('video_title'),
                        caption=video.get('video_description'),
                        tags=video.get('video_tags'),
                    )
                elif destination == 'instagram':
                    upload_instagram_reel(
                        PERMANENT_USER_ACCESS_TOKEN,
                        video.get('video_file_path'),
                        title=video.get('video_title'),
                        caption=video.get('video_description'),
                        tags=video.get('video_tags'),
                    )
                elif destination == 'twitter':
                    upload_tweet(
                        video_path=video.get('video_file_path'),
                        title=video.get('video_title'),
                        caption=video.get('video_description'),
                        tags=video.get('video_tags')
                    )

                print(f'upload succeed')
            except Exception as e:
                print(f'Error: {e} on {video=}')
                errors_count += 1
            sorted_plain_info.pop(0)
        else:
            print(f'waiting...{int(time.time()-t_start)=}')
            time.sleep(INTERVAL)

    print(f'video upload finished errors={errors_count} of total={len(videos)}')