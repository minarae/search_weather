import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from src.main import query, generate_natural_language_response

@pytest.fixture
def mock_query_parser():
    with patch('src.main.QueryParser') as MockQueryParser:
        mock_parser = MockQueryParser.return_value
        yield mock_parser

@pytest.fixture
def mock_weather_service():
    with patch('src.main.WeatherService') as MockWeatherService:
        mock_service = MockWeatherService.return_value
        yield mock_service

def test_query_with_valid_data(mock_query_parser, mock_weather_service):
    # Mock QueryParser
    mock_query_parser.parse_query.return_value = (datetime(2023, 10, 10), "서울", (37.5665, 126.9780))

    # Mock WeatherService
    mock_weather_service.get_weather.return_value = {
        '날씨': '맑음',
        '최고기온': '25°C',
        '최저기온': '15°C'
    }

    result = query("내일 서울의 날씨는 어때")
    assert "서울" in result
    assert "맑음" in result

def test_query_with_invalid_location(mock_query_parser):
    # Mock QueryParser
    mock_query_parser.parse_query.return_value = (datetime(2023, 10, 10), None, None)

    result = query("알 수 없는 장소의 날씨는 어때")
    assert result == "위치 정보를 추출할 수 없습니다."

def test_generate_natural_language_response_with_error():
    error_message = "날씨 정보를 가져올 수 없습니다."
    result = generate_natural_language_response("서울", datetime(2023, 10, 10), error_message)
    assert result == error_message
