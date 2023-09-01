# pylint: disable=missing-function-docstring, missing-module-docstring, import-error, line-too-long
from unittest.mock import call, MagicMock, patch
from app import organisations


@patch("app.organisations.Salesforce", return_value="sf")
@patch("app.organisations.SALESFORCE_CONNECTED_APP_ID", "app_id")
@patch("app.organisations.SALESFORCE_USERNAME", "username")
@patch("app.organisations.SALESFORCE_PASSWORD", "password")
@patch("app.organisations.SALESFORCE_SECURITY_TOKEN", "token")
@patch("app.organisations.SALESFORCE_DOMAIN", "domain")
@patch("requests.Session", return_value="session")
def test_get_session(mock_requests_session, mock_get_session):
    assert organisations.get_session() == mock_get_session.return_value
    mock_get_session.assert_called_with(
        client_id="app_id",
        username="username",
        password="password",
        security_token="token",
        domain="domain",
        session="session",
    )


@patch("app.organisations.get_query", return_value="query")
def test_get_organisations(mock_query):
    mock_session = MagicMock()
    mock_session.bulk.Account.query.return_value = [
        {
            "Id": "1",
            "Name": "hello",
            "CDS_AccountNameFrench__c": "salut",
            "Type": "greeting",
        },
        {
            "Id": "2",
            "Name": "farewell",
            "CDS_AccountNameFrench__c": "bon soir",
            "Type": "goodbye",
        },
    ]
    assert organisations.get_organisations(mock_session) == [
        {
            "id": "1",
            "name_eng": "hello",
            "name_fra": "salut",
            "type": "greeting",
        },
        {
            "id": "2",
            "name_eng": "farewell",
            "name_fra": "bon soir",
            "type": "goodbye",
        },
    ]
    mock_session.bulk.Account.query.assert_called_with("query")
    mock_query.assert_called_with(None, "Name")


@patch("builtins.print")
@patch("app.organisations.get_query", return_value="query")
def test_get_organisations_warning(mock_query, mock_print):
    mock_session = MagicMock()
    mock_session.bulk.Account.query.return_value = [
        {
            "Name": "hello",
            "Type": "greeting",
        },
        {
            "Name": "",
            "CDS_AccountNameFrench__c": "bon soir",
            "Type": "goodbye",
        },
        {
            "Name": "uhh",
            "CDS_AccountNameFrench__c": None,
            "Type": "indecisive",
        },
    ]
    assert organisations.get_organisations(mock_session, "the", "one") == []
    mock_session.bulk.Account.query.assert_called_with("query")
    mock_query.assert_called_with("the", "one")
    mock_print.assert_has_calls(
        [
            call(
                "::warning file=app/organisations.py,::Missing org data 'hello', 'None', 'greeting'"
            ),
            call(
                "::warning file=app/organisations.py,::Missing org data '', 'bon soir', 'goodbye'"
            ),
            call(
                "::warning file=app/organisations.py,::Missing org data 'uhh', 'None', 'indecisive'"
            ),
        ]
    )


def test_get_query():
    assert (
        organisations.get_query()
        == "SELECT Id, Name, CDS_AccountNameFrench__c, Type FROM Account WHERE CDS_Department_list_export__c = TRUE ORDER BY Name"
    )
    assert (
        organisations.get_query(filter_type="foo")
        == "SELECT Id, Name, CDS_AccountNameFrench__c, Type FROM Account WHERE CDS_Department_list_export__c = TRUE AND Type = 'foo' ORDER BY Name"
    )
    assert (
        organisations.get_query(order_by="bar")
        == "SELECT Id, Name, CDS_AccountNameFrench__c, Type FROM Account WHERE CDS_Department_list_export__c = TRUE ORDER BY bar"
    )
    assert (
        organisations.get_query(order_by="bam", filter_type="baz")
        == "SELECT Id, Name, CDS_AccountNameFrench__c, Type FROM Account WHERE CDS_Department_list_export__c = TRUE AND Type = 'baz' ORDER BY bam"
    )
