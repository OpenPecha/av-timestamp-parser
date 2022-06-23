import json
from pathlib import Path

from openpecha.utils import load_yaml
from json_serializer import av_layer_2_json


def test_json_serializer():
    av_layer = load_yaml(Path('./data/tests/test_av_layer.yml'))
    expected_json = load_yaml(Path('./data/tests/expected_json.yaml'))
    pecha_id = "OLA001007"
    av_json = av_layer_2_json(pecha_id, av_layer)
    assert expected_json == av_json
