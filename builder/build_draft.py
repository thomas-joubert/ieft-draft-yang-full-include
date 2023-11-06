import json
import sys
from datetime import date
import os.path
import subprocess
from typing import List

from jinja2 import Environment, select_autoescape, FileSystemLoader

BUILDER_DIR = os.path.dirname(os.path.abspath(__file__))
YANG_DIR = os.path.join(os.path.dirname(BUILDER_DIR), "yang")
SM_YANG_DIR = os.path.join(YANG_DIR, "schema_mount_based", "yang")
JSON_DIR = os.path.join(os.path.dirname(BUILDER_DIR), "json")


env = Environment(
    loader=FileSystemLoader(BUILDER_DIR),
    autoescape=select_autoescape("xml")
)


def _execute_pyang(options: List[str], filenames: List[str]):
    options += ["-p", YANG_DIR]
    args = ["pyang"] + options + filenames
    result = subprocess.run(args, capture_output=True, text=True)
    print()
    print("******************************************************")
    print(" ".join(args))
    print("******************************************************")
    print(" ERRORS ")
    print(result.stderr)
    print("******************************************************")
    print(" OUT ")
    print(result.stdout)
    print("******************************************************")
    return result.stderr, result.stdout


def _build_tree(filenames):
    return _execute_pyang(["-f", "tree", "--tree-line-length", "69"], filenames)


def _format_yang(filenames, ietf=True):
    if ietf:
        args = ["--ietf"]
    else:
        args = []
    return _execute_pyang(args +
                          ["-f", "yang",
                           "--yang-canonical",
                           "--yang-line-length", "69"], filenames)


def _find_yang_file(prefix: str):
    for yang_file in os.listdir(YANG_DIR):
        if yang_file.startswith(prefix) and yang_file.endswith("yang"):
            return os.path.join(YANG_DIR, yang_file)
    raise Exception(f"Yang file with prefix {prefix} not found.")


def _format_json(filename):
    try:
        return "", json.dumps(json.load(open(filename)), indent=2)
    except Exception as e:
        return str(e), ""


#EXT_TX_ID = _find_yang_file("ietf-external-transaction-id")
FULL_INCLUDE_YANG = _find_yang_file("ietf-yang-full-include")
DEVICE_LEVEL_YANG = _find_yang_file("device-level")
NETWORK_LEVEL_STUB_YANG = _find_yang_file("network-level-stub")
NETWORK_LEVEL_YANG = _find_yang_file("network-level")
NETWORK_LEVEL_SM_YANG = os.path.join(SM_YANG_DIR, "network-level.yang")


def draft_content():
    pyang_results = {
        "full_include_yang": _format_yang([FULL_INCLUDE_YANG]),
        "device_level_tree": _build_tree([DEVICE_LEVEL_YANG]),
        "network_level_tree_stub": _build_tree([NETWORK_LEVEL_STUB_YANG]),
        "network_level_fi_yang":  ("", open(NETWORK_LEVEL_YANG).read()),
        "network_level_sm_yang":  ("", open(NETWORK_LEVEL_SM_YANG).read()),
        "device_level_yang": _format_yang([DEVICE_LEVEL_YANG], ietf=False),
        "network_level_yanglib_data": ("", open(os.path.join(SM_YANG_DIR, "..", "network-level-yanglib.xml")).read()),
        "extension_data": ("", open(os.path.join(SM_YANG_DIR, "..", "extension-data.xml")).read()),
    }
    errors = []
    contents = {}
    for key, (error, output) in pyang_results.items():
        contents[key] = output.strip()
        if error != "":
            errors.append(key + "\n" + error)
    if errors:
        for error in errors:
            print("************ERROR********************")
            print(error)
        exit(1)
    add_date(contents)
    return contents


def add_date(contents):
    today = date.today()
    contents["day"] = today.day
    contents["month"] = today.month
    contents["year"] = today.year


if __name__ == '__main__':
    version = int(sys.argv[1])
    output = os.path.join(os.path.dirname(BUILDER_DIR), f"draft-jouqui-netmod-yang-full-include-{version:02}.xml")
    draft_text = env.get_template("draft-claise-yang-full-include.xml")
    with open(output, 'w') as xml_generated:
        xml_generated.write(draft_text.render(**draft_content(), version=f"{version:02}"))
