from utils import run_videos

# it's possible to pass video_date=None, in that case video will be uploaded immediately
videos = {
    "en": [
        {
            "video_file_path": "path/to/english/video1.mp4",
            "video_title": "English Video Title 1",
            "video_description": "This is the English description for the first video.",
            "video_tags": ["tag1", "tag2", "tag3"],
            "video_date": "2024-06-22T14:52:00Z"
        },
        {
            "video_file_path": "path/to/english/video2.mp4",
            "video_title": "English Video Title 2",
            "video_description": "This is the English description for the second video.",
            "video_tags": ["tag4", "tag5", "tag6"],
            "video_date": "2024-06-22T15:52:00Z"
        }
        ],

    "fr": [
        {
            "video_file_path": "path/to/french/video1.mp4",
            "video_title": "Titre de la Vidéo Française 1",
            "video_description": "Ceci est la description en français pour la première vidéo.",
            "video_tags": ["étiquette1", "étiquette2", "étiquette3"],
            "video_date": "2024-06-22T14:54:00Z"
        }
    ]
    }

# ant the moment support only 'facebook' and 'instagram' destination
run_videos(videos=videos, destination='facebook')
