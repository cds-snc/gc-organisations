"""
Retrieve a list of GC organisations, add the notify organisation ids,
save them as a JSON file and commit back to the repo.
"""

from app import export, organisations


def main():
    "Retrieve the list of GC organisations and save them back to JSON files."
    session = organisations.get_session()
    _orgs = organisations.get_organisations(session)
    orgs = organisations.add_notify_organisation_ids(_orgs)
    export.export(orgs)


if __name__ == "__main__":
    main()
