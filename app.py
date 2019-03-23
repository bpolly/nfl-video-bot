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

    if mp4_link:
        return jsonify({ 'links': [mp4_link] })
    if not feed_url:
        return error_response('Could not find file list.')
    if not video_id:
        return error_response('Could not find video ID.')

    json_file_contents = json.loads(get_source_code(feed_url))
    video_list = json_file_contents['videos']
    video_link_list = get_second_page_mp4_links(video_list, video_id)
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
    try:
        found_video = next(video for video in video_list if video['id'] == video_id)
    except StopIteration:
        print("No rows")
    links = map(lambda x: x['videoPath'], found_video['videoBitRates'])
    return list(links)

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
