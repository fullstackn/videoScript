import json
import os
import requests
from common import get_full_caption
from utils import api_call


ACCESS_TOKEN = 'EAAMAgCJ3ZA9UBOwUsbkDdwzNNvn5ypv52vupBKuT5OE9JQwinZBXDGOKaWOT46jGRuVLMZA9bDV28m6ZCfWjP64RZCX2n2kGa7aGOZAPl6s7l7KtId9coXBbwrEUQtVRp0ybAhwMMWeir6zy0f9rOEqL9upZBTpoCqRr3GuCUTeyuXWIxrUo83pgs8C6Dv2ZA7BZBzsd8LzT9kGo4fOc0p7pGT8GmOj16QoCeAfXaeqbcfwZDZD'
WA_BUSINESS_ACCOUNT_ID = '363327930192230'


def upload_whatsapp(video_path, title, caption, tags):
    text = get_full_caption(title, caption, tags)
    media_type = 'video/mp4'
    whatsapp_info = api_call(
        endpoint=f'{WA_BUSINESS_ACCOUNT_ID}/phone_numbers?access_token={ACCESS_TOKEN}',
        method='GET',
        data={"access_token": f'{ACCESS_TOKEN}'}
    )
    phone_number_id = whatsapp_info['data'][0]['id']
    # prepare upload (create container)

    with open(video_path, 'rb') as payload:
        files = {
            "file": ('f', payload, media_type)
        }
        media = api_call(
            endpoint=f'{phone_number_id}/media?'
                     f'messaging_product=whatsapp&'
                     f'file={files}&'
                     f'type={media_type}&',
            method='POST',
            files=files,
            headers={'Authorization': f'Bearer {ACCESS_TOKEN}'}
        )
    media_id = media['id']

    # send message
    data = {
        "messaging_product": "whatsapp",
        "to": f"972506425534",
        "type": 'video',
        "recipient_type": "individual",
        "video": {
            "id": f"{media_id}",
            "caption": f"A succulent eclipse!",
        }
    }

    send = api_call(
            endpoint=f'{phone_number_id}/messages?access_token={ACCESS_TOKEN}',
            method='POST',
            data=data,
            headers={'Authorization': f'Bearer {ACCESS_TOKEN}', 'Content-Type': 'application/json'}
        )
    print(send)


upload_whatsapp('v100.mp4', 'title', 'caption', ['t1','t2'])

