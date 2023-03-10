"""
Retrieve the list of GC organisations.
"""
import base64
import os

from dotenv import load_dotenv
from simple_salesforce import Salesforce

load_dotenv()

SALESFORCE_CONNECTED_APP_ID = os.getenv("SALESFORCE_CONNECTED_APP_ID")
SALESFORCE_CONNECTED_APP_CONSUMER_KEY = os.getenv(
    "SALESFORCE_CONNECTED_APP_CONSUMER_KEY"
)
SALESFORCE_CONNECTED_APP_PRIVATE_KEY = os.getenv("SALESFORCE_CONNECTED_APP_PRIVATE_KEY")
SALESFORCE_DOMAIN = os.getenv("SALESFORCE_DOMAIN")
SALESFORCE_USERNAME = os.getenv("SALESFORCE_USERNAME")


def get_session():
    "Get Salesforce session using JWT authentication"
    return Salesforce(
        client_id=SALESFORCE_CONNECTED_APP_ID,
        username=SALESFORCE_USERNAME,
        consumer_key=SALESFORCE_CONNECTED_APP_CONSUMER_KEY,
        privatekey=base64.b64decode(SALESFORCE_CONNECTED_APP_PRIVATE_KEY),
        domain=SALESFORCE_DOMAIN,
    )


def get_organisations(session, filter_type=None, order_by="Name"):
    "Get the list of verified GC organisations"
    orgs = []
    orgs_query = get_query(filter_type, order_by)
    results = session.bulk.Account.query(orgs_query)
    for result in results:
        dept_id = result.get("Id")
        name_eng = result.get("Name")
        name_fra = result.get("CDS_AccountNameFrench__c")
        org_type = result.get("Type")

        # Make sure we've got everything
        if name_eng and name_fra and org_type:
            orgs.append(
                {
                    "id": dept_id,
                    "name_eng": name_eng,
                    "name_fra": name_fra,
                    "type": org_type,
                }
            )
        else:
            print(
                f"::warning file=app/organisations.py,::Missing org data '{name_eng}', '{name_fra}', '{org_type}'"
            )
    return orgs


def get_query(filter_type=None, order_by="Name"):
    "Get the query used to retrieve the list of GC organisations"
    where_filter_type = f"AND Type = '{filter_type}' " if filter_type else ""
    return (
        f"SELECT Id, Name, CDS_AccountNameFrench__c, Type FROM Account "
        f"WHERE CDS_Department_list_export__c = TRUE "
        f"{where_filter_type}"
        f"ORDER BY {order_by}"
    )
