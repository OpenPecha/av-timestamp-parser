
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

def av_layer_2_json(pecha_id, av_timestamp_layer):
    av_timestamp_json = {
        'id': pecha_id,
        'type': "video",
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
    av_timestamp_json['alignment'] = alignments
    return av_timestamp_json



def serialize_av_layer_to_json(opf_id, opf_path, json_path):
    pecha = OpenPechaFS(opf_id, opf_path)
    base_names = get_base_names(pecha.opf_path)
    for base_name in base_names:
        av_timestamp_layer = pecha.read_layers_file(base_name, LayerEnum.av_timestamp.value)
        av_timestamp_json = av_layer_2_json(opf_id, av_timestamp_layer)
        av_timestamp_json = json.dumps(av_timestamp_json, ensure_ascii=False)
        json_path.write_text(av_timestamp_json, encoding='utf-8')


if __name__ == "__main__":
    opf_path = Path('./data/opfs/OC579B0AC/OC579B0AC.opf')
    pecha_id = opf_path.stem
    json_path = Path(f'./data/json/{pecha_id}.json')
    serialize_av_layer_to_json(pecha_id, opf_path, json_path)

