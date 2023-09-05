# pylint: disable=missing-function-docstring, missing-module-docstring, import-error
from unittest.mock import patch
import main


@patch("main.organisations")
@patch("main.export")
def test_main(mock_export, mock_organisations):
    mock_organisations.get_session.return_value = "session"
    mock_organisations.get_organisations.return_value = [
        {
            "name_eng": "org1",
            "name_fra": "org4",
        },
        {
            "name_eng": "org2",
            "name_fra": "org3",
        },
    ]
    mock_organisations.add_notify_organisation_ids.return_value = [
        {
            "name_eng": "org1",
            "name_fra": "org4",
            "notify_organisation_id": "1234",
        },
        {
            "name_eng": "org2",
            "name_fra": "org3",
            "notify_organisation_id": "1235",
        },
    ]
    main.main()
    mock_organisations.get_organisations.assert_called_with("session")
    mock_export.export.assert_called_with(
        mock_organisations.add_notify_organisation_ids.return_value
    )
