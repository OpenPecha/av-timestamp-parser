from os import link
import re

from pathlib import Path

def get_link_mapping():
    link_mapping = {}
    video_infos = Path('./data/otr/link_detail.txt').read_text(encoding='utf-8').splitlines()
    for video_info in video_infos:
        _,link,title = video_info.split(",")
        v_num = re.search("\d+", title)[0]
        link_mapping[v_num] = link
    return link_mapping


def update_link(line, link_mapping):
    video_num = re.search("\d+ ", line)[0].strip()
    v_num = f"{int(video_num):03}"
    yt_link = link_mapping[v_num]
    line = re.sub("htt.+</p>", f"{yt_link}</p>", line)
    return line

def change_drive_link_to_youtube(xml):
    new_xml = ""
    link_mapping = get_link_mapping()
    lines = xml.splitlines()
    for line in lines:
        if "https" in line:
            new_xml += f"{update_link(line, link_mapping)}\n"
        else:
            new_xml += f"{line}\n"
    return new_xml

if __name__ == "__main__":
    xml = Path('./data/xml/མཁན་པོ་ཚུལ་ཁྲིམས་བློ་གྲོས།.xml').read_text(encoding='utf-8')
    new_xml = change_drive_link_to_youtube(xml)
    Path('./data/xml/new_xml.xml').write_text(new_xml, encoding='utf-8')
