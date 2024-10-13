# Search Weather

`search_weather`는 사용자가 입력한 자연어 쿼리를 기반으로 특정 위치와 날짜의 날씨 정보를 제공하는 Python 패키지입니다. 이 패키지는 외부 API를 사용하여 날씨 데이터를 가져오고, 사용자에게 친숙한 형식으로 응답을 생성합니다.

## 주요 기능

- **자연어 쿼리 파싱 및 날씨 정보 제공**: 사용자가 입력한 쿼리에서 날짜와 위치 정보를 추출하고, 해당 날짜의 날씨 정보를 제공합니다.

## 설치 방법

### pip를 사용한 설치

1. **패키지 설치**:
   ```bash
   pip install search_weather
   ```

### Poetry를 사용한 설치

1. **Poetry 설치**:
   ```bash
   poetry add search_weather
   ```

## 사용 전 준비

1. **OpenWeatherMap 계정 생성 및 API 키 발급**:
   - [OpenWeatherMap](https://openweathermap.org/) 웹사이트에서 계정을 생성합니다.
   - API 키를 발급받습니다.

2. **API 키 설정**:
   - `set_api_key` 함수를 사용하여 API 키를 설정합니다.

## 사용법

패키지를 설치한 후, `set_api_key` 함수를 호출하여 API 키를 설정한 다음 `query` 함수를 사용하여 날씨 정보를 조회할 수 있습니다:

```python
from search_weather import set_api_key, query

# API 키 설정
set_api_key("your_api_key_here")

# 쿼리 실행
result = query("내일 서울의 날씨는 어때")
print(result)
```

## 파일 구조

- `src/search_weather/`: 패키지의 주요 모듈들이 위치한 디렉토리입니다.
- `test/`: 프로젝트의 테스트 파일들이 위치한 디렉토리입니다.

## 테스트

- `pytest`를 사용하여 테스트를 실행할 수 있습니다.
  ```bash
  pytest
  ```

## 기여 방법

1. 이 저장소를 포크합니다.
2. 새로운 기능을 추가하거나 버그를 수정합니다.
3. 변경 사항을 커밋하고 푸시합니다.
4. 풀 리퀘스트를 생성합니다.

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.
