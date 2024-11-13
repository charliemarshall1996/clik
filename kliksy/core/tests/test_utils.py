import pytest
from core.utils import *  # adjust the import to the actual module


@pytest.mark.parametrize("mock_response, expected_result", [
    # Case 1: Valid response with latitude and longitude
    (
        {
            'status_code': 200,
            'json_data': [
                {
                    'lat': '51.2380469',
                    'lon': '-0.7687956'
                }
            ]
        },
        (51.2380469, -0.7687956)
    ),
    # Case 2: Valid response but no results
    (
        {
            'status_code': 200,
            'json_data': []
        },
        None
    ),
    # Case 3: Non-200 response from the API
    (
        {
            'status_code': 404,
            'json_data': None
        },
        None
    )
])
def test_get_coordinates(mocker, mock_response, expected_result):
    """Test the get_coordinates function with mocked API responses."""

    # Mock the requests.get call
    mock_get = mocker.patch('requests.get')

    # Configure the mock based on parameters
    mock_get.return_value.status_code = mock_response['status_code']
    if mock_response['json_data'] is not None:
        mock_get.return_value.json.return_value = mock_response['json_data']
    else:
        mock_get.return_value.json.side_effect = ValueError("No JSON data")

    # Test function call with sample address details
    result = get_coordinates(
        street="221 Weybourne Road",
        city="Aldershot",
        county="Hampshire",
        postalcode="GU11 3NE"
    )

    print(f"CO-ORDINATES RESULT: {result}")
    # Assert result matches expected result
    assert result == expected_result
