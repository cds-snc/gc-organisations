"""
Export the organisation as various file formats.
"""
import csv
import json


def export(orgs):
    "Export the organisation as files."

    if len(orgs) == 0:
        print("::warning file=app/export.py,::Missing org data - nothing to export")
        return

    heading = {
        "name_eng": "English/Anglais",
        "name_fra": "French/Français",
        "type": "Type",
    }
    names_eng = sorted([o["name_eng"] for o in orgs])
    names_fra = sorted([o["name_fra"] for o in orgs])

    export_json("data/all.json", orgs)
    export_json("data/all-name-eng.json", names_eng)
    export_json("data/all-name-fra.json", names_fra)
    export_csv("data/all.csv", [heading] + orgs)
    export_csv("data/all-name-eng.csv", [heading["name_eng"]] + names_eng)
    export_csv("data/all-name-fra.csv", [heading["name_fra"]] + names_fra)


def export_csv(file_path, orgs):
    "Export a CSV file."
    with open(f"{file_path}", "w+", encoding="utf-8") as file:
        writer = csv.writer(file)
        for org in orgs:
            writer.writerow(list(org.values()) if isinstance(org, dict) else [org])


def export_json(file_path, orgs):
    "Export a JSON file."
    with open(f"{file_path}", "w+", encoding="utf-8") as file:
        json.dump(orgs, file, ensure_ascii=False)
