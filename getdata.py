import datetime
from pytube import YouTube, Playlist

import re, os
import json
import requests
from bs4 import BeautifulSoup
from telegraph import upload_file

import pathlib

cur_dir = pathlib.Path(__file__).parent.resolve()

def getmoreinfo(url):
    headers = {
        "Accept-Language": "en-US,en;q=0.5"
    }
    soup = BeautifulSoup(requests.get(url, headers=headers, cookies={'CONSENT:': 'YES+1'}).text, "html.parser")
    prettified_soup =str(soup.prettify())
    
    with open("m.txt", "w", encoding="utf-8") as f:
        f.write(prettified_soup)
        
    data = re.search(r"var ytInitialData = ({.*});", prettified_soup).group(1)

    json_data = json.loads(data)
    data_yt = json_data['header']
    vid_info = {}
    try:
        vid_info["title"] = data_yt['pageHeaderRenderer']['pageTitle']
        vid_info["avatar"] = data_yt['pageHeaderRenderer']['content']['pageHeaderViewModel']['image']['decoratedAvatarViewModel']['avatar']['avatarViewModel']['image']['sources'][2]['url']
        vid_info["subscribers"] = data_yt['pageHeaderRenderer']['content']['pageHeaderViewModel']['metadata']['contentMetadataViewModel']['metadataRows'][1]['metadataParts'][0]['text']['content'].split()[0]
        vid_info["videos"] = data_yt['pageHeaderRenderer']['content']['pageHeaderViewModel']['metadata']['contentMetadataViewModel']['metadataRows'][1]['metadataParts'][1]['text']['content'].split()[0]
        print("1 worked")
    except KeyError as er:
        print("2 worked")
        vid_info["title"] = data_yt['c4TabbedHeaderRenderer']['title']
        vid_info["avatar"] = data_yt['c4TabbedHeaderRenderer']['avatar']['thumbnails'][2]['url']
        vid_info["subscribers"] = data_yt['c4TabbedHeaderRenderer']['subscriberCountText']['simpleText'].split()[0]
        vid_info["videos"] = data_yt['c4TabbedHeaderRenderer']['videosCountText']['runs'][0]['text'].split()[0]
        
    return vid_info


def seconds_to_hours_minutes(seconds):
    duration = datetime.timedelta(seconds=seconds)
    
    hours = duration.seconds // 3600
    minutes = (duration.seconds % 3600) // 60
    remaining_seconds = duration.seconds % 60
    
    return f"{hours}h {minutes}min {remaining_seconds}sec"

def num2text(num):
    if num > 1000000:
        res = f"{round(num/1000000, 2)}M avg.views"
    elif num > 1000:
        res = f"{round(num/1000, 2)}K avg.views"
    else:
        res = f"{round(num, 2)} avg.views"
        
    return res

def generate_data(url, content):
    data_list = []
    if content == "playlist":
        playlist = Playlist(url)

        for vid in playlist:
            video = YouTube(vid) 
            data_list.append(video.views)
        ytvid = YouTube(playlist[0])
    else:
        ytvid = YouTube(url)
    
    info = getmoreinfo(ytvid.channel_url)
    
    
    data = {
        "avatar": info['avatar'],
        "channel" : info['title'],
        "followers" : info['subscribers'],
        "videos" : info['videos'],
        "cover": ytvid.thumbnail_url,
        "views" : f"{ytvid.views} views",
        "length": seconds_to_hours_minutes(ytvid.length),
        "date": ytvid.publish_date.strftime("%d.%m.%Y")
    }
    if content == "playlist":
        data["all_views"] = data_list
        data["views"] = num2text(sum(data_list)/len(data_list))
        data["length"] = f"{len(data_list)} videos"
    
    return data 

file_name = os.path.join(cur_dir, "result.jpg")

if os.path.exists(file_name):
    os.remove(file_name)
    print(f"File '{file_name}' deleted successfully.")
else:
    print(f"File '{file_name}' does not exist.")

from image.getimage import getimage
def get_url(url, content):
    getimage(generate_data(url, content), content)

    link = upload_file(file_name)
    generated_Link = "https://telegra.ph" + "".join(link)

    print(generated_Link)

    return generated_Link


print(get_url("https://youtube.com/playlist?list=PLNVG-lhrskZr8mddtLriGu7fkFnX9SzVC&si=qBK83S4HSZ16rxRS", "playlist"))