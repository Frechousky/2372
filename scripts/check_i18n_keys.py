#!/usr/bin/env python
"""
checks that:
    - all i18n JSON files contain the same keys
    - all i18n keys from JSON files are used in source file
    - all i18n keys used in source files are present in JSON files
"""
import glob
import json
import os
import re
import sys

I18N_DIR = os.path.join("assets", "i18n")
SRC_DIR = os.path.join("src")


def parse_json_files(i18n_dir: str):
    i18n_fname_json = {}
    keys_from_json = set()  # keys from all JSON files
    for fname in glob.iglob(os.path.join(i18n_dir, "*.json")):
        with open(fname, "r") as f:
            i18n_fname_json[fname] = json.load(f)
            for root_k in i18n_fname_json[fname].keys():
                for k in i18n_fname_json[fname][root_k].keys():
                    # add all keys from JSON file (except root key which is locale)
                    keys_from_json.add(k)
    return i18n_fname_json, keys_from_json


def parse_source_files(src_dir: str):
    # look for i18n keys in python source files
    # eg. tmp.py contains "i18n.t('game_over')" => retrieves 'game_over'
    regex = re.compile("i18n\.t\(['\"]([^'\"]+)")
    keys_from_python = set()  # all i18n keys from python source files
    for fname in glob.iglob(os.path.join(src_dir, "**", "*.py"), recursive=True):
        with open(fname, "r") as f:
            for find in regex.findall(f.read()):
                keys_from_python.add(find)
    return keys_from_python


def compare_json_files(i18n_fname_json, keys_from_json) -> bool:
    success = True
    for fname in i18n_fname_json.keys():
        for root_k in i18n_fname_json[fname].keys():
            for k in keys_from_json:
                if k not in i18n_fname_json[fname][root_k].keys():
                    print(f"missing key '{k}' in '{fname}'")
                    success = False
    return success


def compare_keys_from_json_and_sources(keys_from_json, keys_from_python) -> bool:
    success = True
    for k in keys_from_json.difference(keys_from_python):
        print(f"key '{k}' is not used in source files")
        success = False
    for k in keys_from_python.difference(keys_from_json):
        print(f"key '{k}' is used in source files but not defined in JSON files")
        success = False
    return success


i18n_fname_json, keys_from_json = parse_json_files(I18N_DIR)
keys_from_python = parse_source_files(SRC_DIR)

json_compare = compare_json_files(i18n_fname_json, keys_from_json)
json_source_compare = compare_keys_from_json_and_sources(
    keys_from_json, keys_from_python
)

if json_compare and json_source_compare:
    print("success")
    sys.exit(0)

print("failure")
sys.exit(1)
