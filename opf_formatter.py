import re
import yaml
import json

from bs4 import BeautifulSoup
from collections import defaultdict
from enum import Enum
from pathlib import Path

from openpecha.core.annotations import BaseAnnotation, Span
from openpecha.core.layer import LayerEnum, Layer
from openpecha.core.metadata import OpenPechaMetadata, InitialCreationType
from openpecha.core.pecha import OpenPechaFS





extended_LayerEnum = [(l.name, l.value) for l in LayerEnum] + [("av_timestamp", "AVTimestamp")]
LayerEnum = Enum("LayerEnum", extended_LayerEnum)

class ExtentedLayer(Layer):
    annotation_type: LayerEnum

class AVTimeStamp(BaseAnnotation):
    timestamp: str
    src_url: str

def is_link_tag(p_tag):
    if "http" in p_tag.text:
        return True
    return False

def get_seconds(time_str):
    if len(time_str.split(':')) != 3:
        time_str = f"00:{time_str}"
    # split in hh, mm, ss
    hh, mm, ss = time_str.split(':')
    return int(hh) * 3600 + int(mm) * 60 + int(ss)

def get_p_tag_text(p_tag):
    p_tag_text = p_tag.text
    p_tag_text = re.sub("\d", "", p_tag_text)
    p_tag_text = p_tag_text.replace(":","")
    return p_tag_text


def get_timestamp_layer(xml):
    time_stamp_layer = ExtentedLayer(annotation_type=LayerEnum.av_timestamp)
    char_walker = 0
    base_text = ""
    cur_track_url = ""
    soup = BeautifulSoup(xml, 'html.parser')
    p_tags = soup.find_all("p")
    for p_tag in p_tags:
        if is_link_tag(p_tag):
            cur_track_url = re.search("http.+", p_tag.text)[0]
        else:
            p_tag_text = get_p_tag_text(p_tag)
            base_text += p_tag_text
            span_tag = p_tag.find("span")
            time_stamp = f"{cur_track_url}?t={get_seconds(span_tag.text)}"
            span = Span(start=char_walker,end=char_walker + len(p_tag_text))
            av_timestamp = AVTimeStamp(span=span, timestamp=time_stamp,src_url=cur_track_url)
            time_stamp_layer.set_annotation(av_timestamp)
            char_walker = len(base_text)
    return time_stamp_layer, base_text

def create_opf(xml_path, opf_path):
    timestamp_xml = xml_path.read_text(encoding="utf-8")
    metadata = OpenPechaMetadata(initial_creation_type=InitialCreationType.input)
    pecha = OpenPechaFS(metadata=metadata, base={}, layers=defaultdict(dict))
    timestamp_layer, base_text = get_timestamp_layer(timestamp_xml)
    base_name = pecha.set_base(base_text)
    pecha.set_layer(base_name, timestamp_layer)
    pecha.save(output_path = opf_path)

        
if __name__ == "__main__":
    xml_path = Path('./data/xml/གོང་ས་མཆོག་གི་སྤྱོད་འཇུག་བཀའ་ཁྲིད.xml')
    opf_path = Path('./data/opfs')
    create_opf(xml_path, opf_path)