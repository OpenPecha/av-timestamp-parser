import json
from pathlib import Path

from openpecha.utils import load_yaml
from json_serializer import av_layer_2_json


def test_json_serializer():
    av_layer = load_yaml(Path('./data/tests/expected_av_timestamp.yaml'))
    expected_json = Path('./data/tests/expected_json.json').read_text(encoding='utf-8')
    expected_json = json.loads(expected_json)
    pecha_id = "OLA001007"
    av_json = av_layer_2_json(pecha_id, av_layer)
    assert expected_json == av_json


if __name__ == "__main__":
    test_json_serializer()