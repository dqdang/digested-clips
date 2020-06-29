import os
import re
import requests
import sys
import urllib.request

basepath = './'
base_clip_path = 'https://clips-media-assets2.twitch.tv/'


def retrieve_mp4_data(slug):
    T_CID = os.environ['T_CID']
    T_TOKEN = os.environ['T_TOKEN']

    clip_info = requests.get(
        "https://api.twitch.tv/helix/clips?id=" + slug,
        headers={"Client-ID": T_CID, "Authorization": "Bearer {}".format(T_TOKEN)}).json()
    thumb_url = clip_info['data'][0]['thumbnail_url']
    title = clip_info['data'][0]['title']
    slice_point = thumb_url.index("-preview-")
    mp4_url = thumb_url[:slice_point] + '.mp4'
    return mp4_url, title


def dl_progress(count, block_size, total_size):
    percent = int(count * block_size * 100 / total_size)
    sys.stdout.write("\r...%d%%" % percent)
    sys.stdout.flush()


# https://clips.twitch.tv/VivaciousStylishGerbilKappa
def dl_clip(clip):
    slug = clip.split('/')[3].replace('\n', '')
    mp4_url, clip_title = retrieve_mp4_data(slug)
    regex = re.compile('[^a-zA-Z0-9_]')
    clip_title = clip_title.replace(' ', '_')
    out_filename = regex.sub('', clip_title) + '.mp4'
    output_path = (basepath + out_filename)

    print('\nDownloading clip slug: ' + slug)
    print('"' + clip_title + '" -> ' + out_filename)
    print(mp4_url)
    # with open(output_path, 'wb') as f:
    #     f.write(requests.get(mp4_url).content)
    urllib.request.urlretrieve(mp4_url, output_path, reporthook=dl_progress)

    # print('\nDone.')
    return clip_title, output_path


def main():
    clip_title, output_path = dl_clip(sys.argv[1])
    print(clip_title)
    print(output_path)


if __name__ == "__main__":
    main()
