import logging
from antx import transfer
from collections import defaultdict
from pathlib import Path

from openpecha.blupdate import PechaBaseUpdate
from openpecha.core.pecha import OpenPechaFS
from openpecha.utils import dump_yaml, load_yaml

from text2AV_alignment_serializer import get_base_names

logging.basicConfig(filename="./data/transfer_issue_text.log", level=logging.INFO,)



def has_transfer_issue(derge_durchen_layer):
    if "fail" in str(derge_durchen_layer):
        return True
    return False

def transfer_timestamp_layer_2_open_edition_opf(open_edition_opf_path, initial_av_opf_path):
    oe_pecha_id = open_edition_opf_path.stem
    initial_av_pecha_id = initial_av_opf_path.stem
    oe_pecha = OpenPechaFS(oe_pecha_id, open_edition_opf_path)
    initial_av_pecha = OpenPechaFS(initial_av_pecha_id, initial_av_opf_path)
    oe_base_names = get_base_names(open_edition_opf_path)
    initial_av_base_names = get_base_names(initial_av_opf_path)
    for oe_base_name,initial_av_base_name in zip(oe_base_names, initial_av_base_names):
        initial_av_timestamp_layer = initial_av_pecha.read_layers_file(initial_av_base_name, "AVTimestamp")
        (open_edition_opf_path / f"layers/").mkdir()
        (open_edition_opf_path / f"layers/{oe_base_name}").mkdir()
        dump_yaml(initial_av_timestamp_layer, (open_edition_opf_path / f"layers/{oe_base_name}/AVTimestamp.yml"))
        transfer_timestamp_layer(initial_av_opf_path, open_edition_opf_path, initial_av_base_name, oe_base_name)
        oe_av_timestamp_layer = oe_pecha.read_layers_file(oe_base_name, "AVTimestamp")
        if has_transfer_issue(oe_av_timestamp_layer):
            print('transfer issue')
    return oe_pecha.opf_path



def transfer_timestamp_layer(src_opf, trg_opf, src_base_name, trg_base_name):
    pecha_updater = PechaBaseUpdate(src_opf, trg_opf)
    pecha_updater.update_vol(src_base_name, trg_base_name)

if __name__ == "__main__":
    open_edition_opf_path = Path('./data/opfs/open_opfs/O2FCA4A99/O2FCA4A99.opf')
    initial_av_opf_path = Path('./data/opfs/initial_opfs/OC579B0AC/OC579B0AC.opf')
    transfer_timestamp_layer_2_open_edition_opf(open_edition_opf_path, initial_av_opf_path)
    


