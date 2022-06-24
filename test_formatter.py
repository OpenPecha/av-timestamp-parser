from pathlib import Path

from openpecha.utils import load_yaml
from opf_formatter import get_timestamp_layer

def test_formatter():
    xml = Path('./data/tests/test_xml.xml').read_text(encoding='utf-8')
    timestamp_layer, base_text = get_timestamp_layer(xml)
    timestamp_layer = dict(timestamp_layer)
    expected_timestamp_layer = load_yaml(Path('./data/tests/expected_av_timestamp.yaml'))
    expected_base_text = Path('./data/tests/expected_base.txt').read_text(encoding='utf-8')
    assert expected_base_text == base_text
    for (_, expected_ann),(_, ann) in zip(expected_timestamp_layer['annotations'].items(), timestamp_layer['annotations'].items()):
        assert expected_ann['span'] == ann['span']
        assert expected_ann['timestamp'] == ann['timestamp']
        assert expected_ann['src_url'] == ann['src_url']
    
if __name__ == "__main__":
    test_formatter()