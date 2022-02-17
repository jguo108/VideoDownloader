from enum import unique
import sys
import os
from datetime import date
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import WebVTTFormatter
from vtt_to_srt.vtt_to_srt import vtt_to_srt

if len(sys.argv) != 2:
    print("Usage: python caption_downloader.py video_id")
    exit(1)
    
video_id = sys.argv[1]

todays_date = date.today()
unique_folder = str(todays_date.year) + '-' + str(todays_date.month) + '-' + str(todays_date.day) + '_' + video_id

# Create folder for subtitle files
path = './videos/' + unique_folder + '/' 
os.makedirs(os.path.dirname(path), exist_ok=True)

# Create metadata file
filename = path + 'metadata.txt'
with open(filename, 'w', encoding='utf-8') as metadata_file:
    metadata_file.write('https://www.youtube.com/watch?v=' + video_id)

# Download subtitle
transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
transcript = transcript_list.find_transcript(['en'])
translated_transcript = transcript.translate('zh-Hans')
print(translated_transcript.fetch())

formatter = WebVTTFormatter()
vtt_formatted = formatter.format_transcript(translated_transcript.fetch())

# Convert subtitle from vtt to srt
filename = path + 'subtitles.vtt'
with open(filename, 'w', encoding='utf-8') as vtt_file:
    vtt_file.write(vtt_formatted)
    
vtt_to_srt(filename)

# Download video
os.system("youtube-dl -o '" + path + "%(title)s.%(ext)s' -f 'bestvideo[height<=1080]+bestaudio/best[height<=1080]' --write-thumbnail https://www.youtube.com/watch?v=" + video_id)