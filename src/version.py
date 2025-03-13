import xml.etree.ElementTree as ET
import os


def get_version():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    xml_file_path = os.path.join(base_dir, "flatpak_builder/io.github.mak448a.QTCord.metainfo.xml")

    tree = ET.parse(xml_file_path)
    root = tree.getroot()
    release = root.find(".//release")

    if release is not None:
        version = release.get("version")
        if version:
            return version
        else:
            return "(Report bug if you see this)"
    else:
        return "(Report bug if you see this)"

if __name__ == "__main__":
    print(get_version())