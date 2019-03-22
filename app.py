from flask import Flask, render_template, request
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
    html = urlopen(provided_link).read().decode('utf-8')
    mp4_match = re.search('videoUri\": \"(.*.mp4)', html)
    if mp4_match != None:
        return json.dumps({ 'links': [mp4_match.group(1)] })
    else:
        feed_url_match = re.search("feedURL = '(.*)'", html)
        json_link = feed_url_match.group(1)
        if feed_url_match == None:
            response = json.dumps({ 'error': 'Could not find file list. Exiting' })
            response.status_code = 500
            return response
        else:
            video_id = re.search("contentId: '(.*)'", html).group(1)
            json_file_contents = json.loads(urlopen(json_link).read().decode('utf-8'))
            video_list = json_file_contents['videos']
            try:
                found_video = next(video for video in video_list if video['id'] == video_id)
            except StopIteration:
                print("No rows")
            result = map(lambda x: x['videoPath'], found_video['videoBitRates'])
            return json.dumps({ 'links': list(result) })
