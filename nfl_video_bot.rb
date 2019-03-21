require 'open-uri'
require 'json'

url = ARGV[0]
url ||= 'http://www.nfl.com/videos/cleveland-browns/0ap3000001023215/Joe-Thomas-Andrew-Siciliano-Marc-Sessler-discuss-expectations-for-revamped-Browns'
fh = open(url)
html = fh.read

video_url_match = /"videoUri": "(.*.mp4)"/.match html
if video_url_match
  puts 'Found MP4 in source code'
  puts '------'
  puts video_url_match[1]
  puts '------'
else
  puts 'Could not find MP4 in source code, checking file list'
  match = /feedURL = '(.*)'/.match html
  json_link =  match[1]
  if !json_link
    puts 'Could not find file list. Exiting'
  else
    puts json_link
    video_id = /contentId: '(.*)'/.match html
    json_file_contents = JSON.parse(open(json_link).read, object_class: OpenStruct)
    video_link = json_file_contents
                    .videos
                    .select { |v| v.id == video_id }
                    .first
                    .videoBitRates
                    .sort_by { |v| v.bitate }
                    .first
                    .videoPath
    if video_link
      puts 'Found MP4 in JSON list'
      puts '------'
      puts video_link
      puts '------'
    end
  end
end


