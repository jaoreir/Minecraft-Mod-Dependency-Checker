import os
import sys
import zipfile

import json
import prettytable as pt
import tomllib
from rich import print as rprint
from rich.tree import Tree


def parse_toml(mods_info, file_name, jar_file, inner_file_name):
    with jar_file.open(inner_file_name) as toml_file:
        try:
            content = toml_file.read().decode("utf-8")
            data = tomllib.loads(content)
            if "mods" in data and data["mods"]:
                mod_id = data["mods"][0].get("modId", "unknown")
                if mod_id != "unknown":
                    dependencies = data.get("dependencies", {}).get(mod_id, [])
                    mods_info[mod_id] = [
                        dep["modId"]
                        for dep in dependencies
                        if dep["modId"] not in ("forge", "minecraft")
                        # and dep.get("mandatory", False)
                    ]
        except tomllib.TOMLDecodeError as er:
            print(er, file=sys.stderr)
            print(f"Error parsing {file_name}", file=sys.stderr)
            print(f"Will skip {file_name}!", file=sys.stderr)
            return


def parse_json(mods_info, file_name, jar_file, inner_file_name):
    with jar_file.open(inner_file_name) as json_file:
        data = json.load(json_file)
        mod_id = data.get("id", "unknown")
        if mod_id != "unknown":
            dependencies = data.get("depends", {})
            mods_info[mod_id] = [
                dep for dep in dependencies.keys() if dep not in ("forge", "minecraft")
            ]


def parse_mods_info(mods_folder):
    mods_info = {}

    for file_name in os.listdir(mods_folder):
        if not file_name.endswith(".jar"):
            continue
        jar_path = os.path.join(mods_folder, file_name)
        with zipfile.ZipFile(jar_path, "r") as jar_file:
            for inner_file_name in jar_file.namelist():
                if inner_file_name.endswith("mods.toml"):
                    parse_toml(mods_info, file_name, jar_file, inner_file_name)
                elif inner_file_name.endswith("fabric.mod.json"):
                    parse_json(mods_info, file_name, jar_file, inner_file_name)

    return mods_info


def print_table(mods_info):
    table = pt.PrettyTable()
    table.field_names = ["MOD NAME", "DEPENDENCIES"]
    table.hrules = pt.HRuleStyle.ALL

    for mod, deps in mods_info.items():
        if deps:
            dep_list = ", ".join(deps)
        else:
            dep_list = "No mandatory dependencies found."
        table.add_row([mod, dep_list])

    table.align = "l"

    print(table)


def build_tree(node, deps, tree, seen):
    if node in seen:
        tree.add(f"{node} (already shown)")
        return

    seen.add(node)

    for dep in deps.get(node, []):
        branch = tree.add(dep)
        build_tree(dep, deps, branch, seen)


def find_unreferenced_nodes(deps):
    depended_on = set()

    for dependencies in deps.values():
        depended_on.update(dependencies)

    return set(deps) - depended_on


def print_tree(mods_info):
    dep_dict = {}
    for mod, deps in mods_info.items():
        if deps:
            dep_dict[mod] = list(deps)
        else:
            dep_dict[mod] = list()
    # rprint(dep_dict)

    for node in dep_dict.keys():
        tree = Tree(node)
        build_tree(node, dep_dict, tree, set())
        # rprint(tree)

    print("Mods with no dependents:")
    rprint(sorted(list(find_unreferenced_nodes(dep_dict))))


def main():
    # Ask for the mod folder path
    print("""Minecraft Mod Dependency Checker V1.0.0
    By Steven Wheeler (https://github.com/stevenjwheeler/Minecraft-Mod-Dependency-Checker/)

    This tool reads the manifests in your mod folders .jar files and extracts information about the mandatory dependencies that each mod requires. 
    This helps to determine what libraries your mods in your installation or modpack require to function. 
    (For example, I created this tool to figure out what libraries I no longer needed after removing some mods from my modpack.)
    """)
    if len(sys.argv) < 2:
        print("Path not provided!", file=sys.stderr)
        exit(1)
    mods_folder_path = sys.argv[1].strip()
    mods_info = parse_mods_info(mods_folder_path)
    # print_table(mods_info)
    print_tree(mods_info)


if __name__ == "__main__":
    main()
