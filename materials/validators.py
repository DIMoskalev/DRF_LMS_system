from rest_framework.serializers import ValidationError

access_video_urls = ['youtube.com', 'sky.pro']


def validate_video_url(value):
    for access_video_url in access_video_urls:
        if access_video_url in value:
            return value
    raise ValidationError('URL видео содержит запрещенный сайт')

# Вторая версия кода сверху
# def validate_video_url(value):
    # access_url = []
    # for access_video_url in access_video_urls:
    #     if access_video_url in value:
    #         access_url.append(access_video_url)
    # if len(access_url) == 0:
    #     raise ValidationError('URL видео содержит запрещенный сайт')
