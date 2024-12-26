#!/usr/bin/env python3
"""
hacked together script to generate a file that can be sourced
to allow one to ssh in and run the app pieces. It presumes
the file is named '/root/startup_based_env_var.env'. We get the other
part from os.environ (i.e, we are logging in).
"""
from pathlib import Path
import os

conflict_ignore_list = ['PWD', 'TERM', '_', 'SHLVL']


def load_map_from_file(file_name):
    file_path = Path(file_name)
    rmap = {}
    for line in file_path.read_text().split('\n'):
        line = line.strip()
        if len(line) > 0:
            key, value = line.split('=', 1)
            rmap[key] = value
    return rmap


ssh_map = dict(os.environ.items())
balena_map = load_map_from_file('/root/startup_based_env_var.env')

out_map = {}
ssh_key_set = frozenset(ssh_map.keys())
balena_key_set = frozenset(balena_map.keys())


def safe_write_export(env_name, env_value):
    print("export {}='{}'".format(env_name, env_value))


print("# keys only in ssh:", ssh_key_set - balena_key_set)
print("#  (not touching!)")
print("# keys only in balena", balena_key_set - ssh_key_set)
for set_key in (balena_key_set - ssh_key_set):
    safe_write_export(set_key, balena_map[set_key])

print("# keys in both", ssh_key_set & balena_key_set)
for set_key in (ssh_key_set & balena_key_set):
    if ssh_map[set_key] == balena_map[set_key]:
        print("#  {} same in both ({})".format(set_key, ssh_map[set_key]))
    elif set_key in conflict_ignore_list:
        print("#  explicit ignore of {} {} in ssh and {} in balena-started".format(
            set_key, ssh_map[set_key], balena_map[set_key]))
    else:
        print("# using balena-started {} over ssh based {} for {}".format(
            balena_map[set_key], ssh_map[set_key], set_key))
        safe_write_export(set_key,  balena_map[set_key])
