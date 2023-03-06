# pylint: disable=missing-function-docstring, missing-module-docstring, import-error
from unittest.mock import call, MagicMock, patch
from app import export


@patch("app.export.export_csv")
@patch("app.export.export_json")
def test_export(mock_export_json, mock_export_csv):
    export.export(
        [
            {
                "name_eng": "org1",
                "name_fra": "org4",
                "type": "org",
            },
            {
                "name_eng": "org2",
                "name_fra": "org3",
                "type": "org",
            },
        ]
    )
    mock_export_csv.assert_has_calls(
        [
            call(
                "data/all.csv",
                [
                    {
                        "name_eng": "English/Anglais",
                        "name_fra": "French/Français",
                        "type": "Type",
                    },
                    {
                        "name_eng": "org1",
                        "name_fra": "org4",
                        "type": "org",
                    },
                    {
                        "name_eng": "org2",
                        "name_fra": "org3",
                        "type": "org",
                    },
                ],
            ),
            call(
                "data/all-name-eng.csv",
                [
                    "English/Anglais",
                    "org1",
                    "org2",
                ],
            ),
            call(
                "data/all-name-fra.csv",
                [
                    "French/Français",
                    "org3",
                    "org4",
                ],
            ),
        ]
    )

    mock_export_json.assert_has_calls(
        [
            call(
                "data/all.json",
                [
                    {
                        "name_eng": "org1",
                        "name_fra": "org4",
                        "type": "org",
                    },
                    {
                        "name_eng": "org2",
                        "name_fra": "org3",
                        "type": "org",
                    },
                ],
            ),
            call(
                "data/all-name-eng.json",
                [
                    "org1",
                    "org2",
                ],
            ),
            call(
                "data/all-name-fra.json",
                [
                    "org3",
                    "org4",
                ],
            ),
        ]
    )


@patch("app.export.export_csv")
@patch("app.export.export_json")
@patch("builtins.print")
def test_export_no_data(mock_print, mock_export_json, mock_export_csv):
    export.export([])
    mock_print.assert_called_with(
        "::warning file=app/export.py,::Missing org data - nothing to export"
    )
    mock_export_json.assert_not_called()
    mock_export_csv.assert_not_called()


@patch("app.export.csv")
@patch("app.export.open")
def test_export_csv(mock_open, mock_csv):
    mock_file = MagicMock()
    mock_open.return_value.__enter__.return_value = mock_file
    export.export_csv(
        "data/all.csv",
        [
            {
                "name_eng": "English/Anglais",
                "name_fra": "French/Français",
                "type": "Type",
            },
            {"name_eng": "org1", "name_fra": "org4", "type": "org"},
            {"name_eng": "org2", "name_fra": "org3", "type": "org"},
        ],
    )
    mock_open.assert_called_with("data/all.csv", "w+", encoding="utf-8")
    mock_csv.writer.assert_called_with(mock_file)
    mock_csv.writer.return_value.writerow.assert_has_calls(
        [
            call(["English/Anglais", "French/Français", "Type"]),
            call(["org1", "org4", "org"]),
            call(["org2", "org3", "org"]),
        ]
    )


@patch("app.export.json")
@patch("app.export.open")
def test_export_json(mock_open, mock_json):
    mock_file = MagicMock()
    mock_open.return_value.__enter__.return_value = mock_file
    export.export_json(
        "data/all.json",
        [
            {"name_eng": "org1", "name_fra": "org4"},
            {"name_eng": "org2", "name_fra": "org3"},
        ],
    )
    mock_open.assert_called_with("data/all.json", "w+", encoding="utf-8")
    mock_json.dump.assert_called_with(
        [
            {"name_eng": "org1", "name_fra": "org4"},
            {"name_eng": "org2", "name_fra": "org3"},
        ],
        mock_file,
        ensure_ascii=False,
    )
