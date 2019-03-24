from flask import Flask, render_template, request, jsonify
from urllib.request import urlopen
import json
import re
import pdb
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('form.html')

@app.route('/handle_data', methods=['POST'])
def handle_data():
    provided_link = json.loads(request.data)['linkField']
    if not url_is_valid(provided_link):
        return error_response('URL not a valid nfl.com link')

    html = get_source_code(provided_link)
    mp4_link, feed_url, video_id = get_important_values(html)

    # if mp4_link:
    #     return jsonify({ 'links': [mp4_link] })
    if not feed_url:
        return error_response('Could not find file list.')
    if not video_id:
        return error_response('Could not find video ID.')

    json_file_contents = json.loads(get_source_code(feed_url))
    video_list = json_file_contents['videos']
    video_link_list = get_second_page_mp4_links(video_list, video_id)
    if(mp4_link and (not mp4_link in video_link_list)):
        video_link_list.append(mp4_link)
    video_link_list = video_link_list + get_embeddable_video_links(video_id)
    video_link_list = list(dict.fromkeys(video_link_list))
    return jsonify({ 'links': video_link_list })

def get_source_code(url):
    return urlopen(url).read().decode('utf-8')

def get_important_values(text):
    mp4_link = get_first_page_mp4_link(text)
    feed_url = get_feed_url_link(text)
    content_id = get_content_id(text)
    return (mp4_link, feed_url, content_id)

def url_is_valid(url):
    match = re.search("https?://www.nfl.com/videos.*", url)
    if match:
        return True
    else:
        return False

def get_first_page_mp4_link(text):
    match = re.search('videoUri\": \"(.*.mp4)', text)
    if match:
        return match.group(1)
    else:
        return None

def get_second_page_mp4_links(video_list, video_id):
    found_video = None
    try:
        found_video = next(video for video in video_list if video['id'] == video_id)
    except StopIteration:
        print("No rows")
    if not found_video:
        return []
    links = map(lambda x: x['videoPath'], found_video['videoBitRates'])
    return list(links)

def get_embeddable_video_links(video_id):
    path = 'http://www.nfl.com/static/embeddablevideo/' + video_id + '.json'
    json_source = json.loads(get_source_code(path))
    mp4_link_objects = json_source['cdnData']['bitrateInfo']
    links = []
    if(len(mp4_link_objects) > 0):
        paths = map(lambda x: x['path'], mp4_link_objects)
        links = map(lambda x: "http://a.video.nfl.com/" + x, paths)
        links = list(links)
    else:
        links = [json_source['cdnData']['videoPlayBackUrl']]
    return links

def get_feed_url_link(text):
    match = re.search("feedURL = '(.*)'", text)
    if match:
        return match.group(1)
    else:
        return None

def get_content_id(text):
    match = re.search("contentId: '(.*)'", text)
    if match:
        return match.group(1)
    else:
        return None

def error_response(text):
    response = jsonify({ 'error': text })
    response.status_code = 500
    return response
