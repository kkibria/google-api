# Google's Request

from lib import get_tokens, YOUTUBE_UPLOAD_SCOPE

if __name__ == '__main__':
    c = get_tokens(fetch=True, scope=YOUTUBE_UPLOAD_SCOPE)
    # print(c.to_json())