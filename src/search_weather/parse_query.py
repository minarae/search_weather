import spacy
from geopy.geocoders import Nominatim
from datetime import datetime, timedelta
from typing import Tuple, Optional, List


def parse_query(query: str) -> Tuple[Optional[datetime], Optional[List[str]]]:
    """
    쿼리를 파싱하여 날짜와 위치 정보를 추출합니다.

    Args:
        query (str): 사용자 입력 쿼리

    Returns:
        Tuple[Optional[datetime], Optional[List[str]]]: 추출된 날짜와 위치 리스트
    """
    # 한글 모델 로드
    nlp = spacy.load("ko_core_news_sm")

    # 사용자 정의 엔티티 추가
    ruler = nlp.add_pipe("entity_ruler")
    patterns = [
        {"label": "LC", "pattern": "하와이"},
        {"label": "LC", "pattern": "LA"},
        {"label": "LC", "pattern": "뉴욕"},
        # 필요한 만큼 추가 가능
    ]
    ruler.add_patterns(patterns)

    doc = nlp(query)
    date = extract_date(doc)
    location = extract_location(doc)
    raw_location = None
    if location:
        raw_location = location[0]
        location = validate_location(location[0])

    return date, raw_location, location


def extract_location(doc: spacy.tokens.Doc) -> Optional[List[str]]:
    """
    주어진 문서에서 위치 정보를 추출합니다.

    Args:
        doc (spacy.tokens.Doc): spaCy로 처리된 문서

    Returns:
        Optional[List[str]]: 추출된 위치 리스트 또는 None
    """

    locations = []
    for ent in doc.ents:
        if ent.label_ == "LC":
            locations.append(ent.text)

    if not locations:
        # 엔티티로 인식되지 않은 위치명을 찾습니다.
        location_keywords = ["서울", "부산", "인천", "대구", "광주", "대전", "울산", "세종", "제주"]
        for token in doc:
            if token.text in location_keywords:
                locations.append(token.text)

    return locations if locations else None


def validate_location(location):
    geolocator = Nominatim(user_agent="search_weather")
    try:
        location = geolocator.geocode(location)
        return location if location else None
    except Exception:
        return None


def extract_date(doc: spacy.tokens.Doc) -> datetime:
    """
    주어진 문서에서 날짜 정보를 추출합니다.

    Args:
        doc (spacy.tokens.Doc): spaCy로 처리된 문서

    Returns:
        datetime: 추출된 날짜 또는 현재 날짜
    """
    date_keywords = {
        '오늘': 0,
        '내일': 1,
        '모레': 2,
        '글피': 3,
        '주말': [5, 6],  # 토요일, 일요일
    }

    for ent in doc.ents:
        if ent.label_ == "DATE":
            # DATE 엔티티가 발견되면 해당 텍스트를 반환
            # 여기서는 간단히 현재 날짜를 반환하지만, 실제로는 텍스트를 날짜로 파싱해야 합니다.
            return datetime.now()

    for token in doc:
        if token.text in date_keywords:
            days = date_keywords[token.text]
            if isinstance(days, list):
                today = datetime.now()
                saturday = today + timedelta((5 - today.weekday() + 7) % 7)
                return saturday
            else:
                return datetime.now() + timedelta(days=days)

    # 날짜를 찾지 못한 경우 오늘 날짜 반환
    return datetime.now()


def main():
    """
    메인 함수: 테스트 쿼리를 실행하고 결과를 출력합니다.
    """
    queries = [
        "내일 서울의 날씨는 어때",
        "내일 모레 하와이 날씨는 어떨거 같아",
        "주말에 부산 날씨는 어떨거 같아",
        "이번 주말 제주도 날씨 좋아?",
        "다음달 뉴욕 날씨 어떨까"
    ]

    for query in queries:
        date, location = parse_query(query)
        print(f"쿼리: {query}")
        print(f"추출된 날짜: {date}")
        print(f"추출된 위치: {location}")
        print("-" * 50)


if __name__ == "__main__":
    main()
