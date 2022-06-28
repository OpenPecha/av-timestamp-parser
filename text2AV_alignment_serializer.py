
import json
import yaml

from enum import Enum
from pathlib import Path

from openpecha.core.layer import LayerEnum
from openpecha.core.pecha import OpenPechaFS
from openpecha.utils import dump_yaml

extended_LayerEnum = [(l.name, l.value) for l in LayerEnum] + [("av_timestamp", "AVTimestamp")]
LayerEnum = Enum("LayerEnum", extended_LayerEnum)


def get_base_names(opf_path):
    base_names = []
    for base_path in list((opf_path / "base").iterdir()):
        base_names.append(base_path.stem)
    return base_names

def get_text2av_alignment(pecha_id, av_timestamp_layer):
    text2av_alignment = {
        'alignment' : []
    }
    alignments = []
    for _, ann in av_timestamp_layer['annotations'].items():
        cur_alignment = {
            'source_segment': {
                'start': ann['span']['start'],
                'end': ann['span']['end']
            },
            'target_segment': {
                'timestamp': ann['timestamp'],
                'src_url': ann['src_url']
            }
        }
        alignments.append(cur_alignment)
    text2av_alignment['alignment'] = alignments
    return text2av_alignment



def serialize_av_layer_to_text2av_alignment(opf_id, opf_path, json_path):
    pecha = OpenPechaFS(opf_id, opf_path)
    base_names = get_base_names(pecha.opf_path)
    for base_name in base_names:
        av_timestamp_layer = pecha.read_layers_file(base_name, LayerEnum.av_timestamp.value)
        text2av_alignment = get_text2av_alignment(opf_id, av_timestamp_layer)
        text2av_alignment = json.dumps(text2av_alignment, ensure_ascii=False)
        json_path.write_text(text2av_alignment, encoding='utf-8')


if __name__ == "__main__":
    opf_path = Path('./data/opfs/open_opfs/O2FCA4A99/O2FCA4A99.opf')
    pecha_id = opf_path.stem
    json_path = Path(f'./data/json/{pecha_id}.json')
    serialize_av_layer_to_text2av_alignment(pecha_id, opf_path, json_path)

