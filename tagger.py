import json
import os
import subprocess
from helper import error_out, cmdline
import getpass
from copy import deepcopy
import argparse


def get_args():
    parser = argparse.ArgumentParser(description='Update tags in 1Password')
    parser.add_argument("-o", '--old-tag', help="The old tag", dest="old_tag", required=True)
    parser.add_argument("-n", '--new-tag', help="The new tag to use", dest="new_tag", required=True)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--override', help="Replace the old tag with the new one. If there's other tags on the item, all will be removed", action='store_true')
    group.add_argument('--sub', help="Substitute old tag with new. All other tags are preserved", action='store_true')
    group.add_argument('--append', help="Simply append the new tag and keep the old", action='store_true')
    args = parser.parse_args()
    return args

def get_1p_items_with_tag(tag: str):
    cmd = f'op list items --tags {tag} > /tmp/1p_item_with_tag_{tag}'
    response = cmdline(cmd)
    error_out(response)

    cmd = f"jq '[.[] | {{id: .uuid, tags: .overview.tags}}]' /tmp/1p_item_with_tag_{tag} > /tmp/1p_{tag}.json"
    response = cmdline(cmd)
    error_out(response)

def change_1p_tag(old_tag:str, new_tag: str, override: bool = False, substitute: bool = False, append: bool = False):

    with open(f'/tmp/1p_{old_tag}.json') as myjson:
        my_json_dict = json.load(myjson)
        if not my_json_dict:
            print("The tag you indicated seems to not exist")
            exit(1)
        for item in my_json_dict:
            if override and (not substitute and not append):
                cmd = f"op edit item {item['id']} tags={new_tag}"
            elif substitute and (not override and not append):
                tags = deepcopy(item['tags'])
                tags.remove(old_tag)
                existing_tags = ','.join(tags)
                cmd = f"op edit item {item['id']} tags={existing_tags},{new_tag}"
            elif append and (not override and not substitute):
                existing_tags = ','.join(item['tags'])
                cmd = f"op edit item {item['id']} tags={existing_tags},{new_tag}"
            else:
                print("No valid option selected")
                exit(1)
            response = cmdline(cmd)
            error_out(response)
    print("DONE")


def main():
    args = get_args()
    get_1p_items_with_tag(args.old_tag)
    if args.override:
        change_1p_tag(args.old_tag, args.new_tag, override=True)
    if args.sub:
        change_1p_tag(args.old_tag, args.new_tag, substitute=True)
    if args.append:
        change_1p_tag(args.old_tag, args.new_tag, append=True)
if __name__ == '__main__':
    main()

