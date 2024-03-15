import os
import requests
import util.config as config
import util.logger as logger

def download_font():
    font_url = config.value_of('font_url')
    font_path = font_url.split('/')[-1]
    if os.path.exists(f'fonts/{font_path}'):
        return

    try:
        r = requests.get(font_url, allow_redirects=True)
    except:
        logger.error(f'Failed to download font: {font_url}')
        return
    os.makedirs('fonts', exist_ok=True)
    open(f'fonts/{font_path}', 'wb').write(r.content)
    return