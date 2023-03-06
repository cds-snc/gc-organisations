"""
Retrieve a list of GC organisations, save them as a JSON file and commit
back to the repo.
"""
from app import export, organisations


def main():
    "Retrieve the list of GC organisations and save them back to JSON files."
    session = organisations.get_session()
    orgs = organisations.get_organisations(session)
    export.export(orgs)


if __name__ == "__main__":
    main()
