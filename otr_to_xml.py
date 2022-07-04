
from bs4 import BeautifulSoup
from pathlib import Path

import re

def is_link_tag(p_tag):
    if "http" in p_tag:
        return True
    return False

def is_left_over_p_tag(p_tag):
    if "span" in p_tag or re.search("<p><span", p_tag) or re.search("<p><b", p_tag):
        return False
    return True

def get_last_p_tag(reformated_xml):
    p_tags = reformated_xml.splitlines()
    if p_tags:
        return p_tags[-1]
    return ""


def merge_left_over(p_tag, reformated_xml):
    print(p_tag)
    if "span" not in p_tag:
        left_over_text = re.search("<p>(.+?)</p>", p_tag).group(1)
        last_p_tag = get_last_p_tag(reformated_xml)
        reformated_last_p_tag = re.sub("</p>", f"{left_over_text}</p>", last_p_tag)
        reformated_xml = re.sub(last_p_tag, reformated_last_p_tag, reformated_xml)
    else:
        left_over_text = re.search("<p>([^<]+?)<span", p_tag).group(1)
        last_p_tag = get_last_p_tag(reformated_xml)
        reformated_last_p_tag = re.sub("</p>", f"{left_over_text}</p>", last_p_tag)
        reformated_xml = re.sub(last_p_tag, reformated_last_p_tag, reformated_xml)
        p_tag = re.sub(left_over_text, "", p_tag)
        reformated_xml += f"{p_tag}\n"
    return reformated_xml

def split_spans(p_tag):
    p_tag_splited = ""
    p_tag_parts = re.split("(<span.+?</span>)", p_tag)
    cur_p_tag = "<p>"
    for p_tag_part in p_tag_parts[1:]:
        if "<span" not in p_tag_part and "p>" not in p_tag_part:
            cur_p_tag += f"{p_tag_part}</p>\n"
            p_tag_splited += cur_p_tag
            cur_p_tag = "<p>"
        else:
            cur_p_tag += p_tag_part
    p_tag_splited += f"{cur_p_tag}\n"
    return p_tag_splited

def is_multispan_p_tag(p_tag):
    if p_tag.count("span") > 2:
        return True
    return False

def fix_multispan_p_tag(reformated_xml):
    fixed_xml = ""
    p_tags = reformated_xml.splitlines()
    for p_tag in p_tags:
        if is_multispan_p_tag(p_tag):
            fixed_xml += split_spans(p_tag)
        else:
            fixed_xml += f"{p_tag}\n"
    return fixed_xml


def beautify_xml(xml_text):
    beautified_xml = re.sub("</p>", "</p>\n", xml_text)
    beautified_xml = beautified_xml.replace("<p></p>", "")
    beautified_xml = beautified_xml.replace("\n\n","")
    reformated_xml = ""
    p_tags = beautified_xml.splitlines()
    for p_tag in p_tags:
        if is_link_tag(p_tag):
            reformated_xml += f"{p_tag}\n"
        elif is_left_over_p_tag(p_tag):
            reformated_xml = merge_left_over(p_tag, reformated_xml)
        else:
            reformated_xml += f"{p_tag}\n"
    reformated_xml = reformated_xml.replace("<p><span></span></p>" ,"")
    reformated_xml = reformated_xml.replace("\n\n", "")
    reformated_xml = fix_multispan_p_tag(reformated_xml)
    return reformated_xml


def rm_extras(otr_text):
    xml_text = re.sub("\{.+?<", "<", otr_text)
    xml_text = re.sub("\",.+\}", "", xml_text)
    xml_text = xml_text.replace("<p><br /></p>","")
    xml_text = xml_text.replace('\\"', '"')
    xml_text = xml_text.replace("<br />", "")
    xml_text = xml_text.replace("\xa0", "")
    return xml_text

def otr_to_xml(otr_file_path):
    xml_text = ""
    otr_text = otr_file_path.read_text(encoding='utf-8')
    xml_text = rm_extras(otr_text)
    xml_text = beautify_xml(xml_text)
    return xml_text


if __name__ == "__main__":
    otr_file_path = Path('./data/otr/མཁན་པོ་ཚུལ་ཁྲིམས་བློ་གྲོས།.otr')
    xml_text = otr_to_xml(otr_file_path)
    Path(f'./data/xml/{otr_file_path.stem}.xml').write_text(xml_text, encoding='utf-8')