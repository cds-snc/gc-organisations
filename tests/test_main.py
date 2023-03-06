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
    main.main()
    mock_organisations.get_organisations.assert_called_with("session")
    mock_export.export.assert_called_with(
        mock_organisations.get_organisations.return_value
    )
