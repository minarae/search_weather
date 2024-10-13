import spacy
from geopy.geocoders import Nominatim
from datetime import datetime, timedelta
from typing import Tuple, Optional, List

class QueryParser:
    def __init__(self):
        self.nlp = spacy.load("ko_core_news_sm")
        self._add_custom_entities()
        self.geolocator = Nominatim(user_agent="search_weather")

    def _add_custom_entities(self):
        ruler = self.nlp.add_pipe("entity_ruler")
        patterns = [
            {"label": "LC", "pattern": "하와이"},
            {"label": "LC", "pattern": "LA"},
            {"label": "LC", "pattern": "뉴욕"},
        ]
        ruler.add_patterns(patterns)

    def parse_query(self, query: str) -> Tuple[Optional[datetime], Optional[str], Optional[List[str]]]:
        """
        쿼리를 파싱하여 날짜와 위치 정보를 추출합니다.

        Args:
            query (str): 사용자 입력 쿼리

        Returns:
            Tuple[Optional[datetime], Optional[str], Optional[List[str]]]: 추출된 날짜, 원본 위치, 검증된 위치 리스트
        """
        doc = self.nlp(query)
        date = self._extract_date(query, doc)
        location = self._extract_location(doc)
        raw_location = None
        if location:
            raw_location = location[0]
            location = self._validate_location(location[0])

        return date, raw_location, location

    def _extract_location(self, doc: spacy.tokens.Doc) -> Optional[List[str]]:
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

    def _extract_date(self, query: str, doc: spacy.tokens.Doc) -> Optional[datetime]:
        """
        주어진 문서에서 날짜 정보를 추출합니다.

        Args:
            doc (spacy.tokens.Doc): spaCy로 처리된 문서

        Returns:
            Optional[datetime]: 추출된 날짜 또는 None
        """
        today = datetime.now().date()
        date_keywords = {
            '오늘': 0,
            '내일': 1,
            '모레': 2,
            '글피': 3,
            '주말': [5, 6],  # 토요일, 일요일
        }

        for ent in doc.ents:
            if ent.label_ == "DT":
                # DATE 엔티티에서 텍스트 추출
                date_text = ent.text
                # 내일 모레에 대한 처리
                if date_text == "내일" and "모레" in query:
                    date_text = "모레"

                # 현재 날짜 가져오기
                today = datetime.now().date()

                # 날짜 키워드에 따라 날짜 계산
                if "오늘" in date_text:
                    return datetime.combine(today, datetime.min.time())
                elif "내일" in date_text:
                    return datetime.combine(today + timedelta(days=1), datetime.min.time())
                elif "모레" in date_text:
                    return datetime.combine(today + timedelta(days=2), datetime.min.time())
                elif "글피" in date_text:
                    return datetime.combine(today + timedelta(days=3), datetime.min.time())
                elif "주말" in date_text:
                    days_until_saturday = (5 - today.weekday() + 7) % 7
                    return datetime.combine(today + timedelta(days=days_until_saturday), datetime.min.time())

        for token in doc:
            if token.text in date_keywords:
                days = date_keywords[token.text]
                if isinstance(days, list):
                    today = datetime.now()
                    saturday = today + timedelta((5 - today.weekday() + 7) % 7)
                    return saturday
                else:
                    return datetime.now() + timedelta(days=days)

        # 날짜를 찾지 못한 경우는 None 반환
        return None

    def _validate_location(self, location: str) -> Optional[List[str]]:
        """
        주어진 위치를 검증하고 좌표를 반환합니다.

        Args:
            location (str): 검증할 위치 문자열

        Returns:
            Optional[List[str]]: 검증된 위치의 [위도, 경도] 리스트 또는 None
        """
        try:
            location_info = self.geolocator.geocode(location)
            if location_info:
                return [str(location_info.latitude), str(location_info.longitude)]
        except Exception as e:
            print(f"위치 검증 중 오류 발생: {e}")
        return None


def main():
    """
    메인 함수: 테스트 쿼리를 실행하고 결과를 출력합니다.
    """
    # QueryParser 인스턴스 생성
    query_parser = QueryParser()
    queries = [
        "내일 서울의 날씨는 어때",
        "내일 모레 하와이 날씨는 어떨거 같아",
        "주말에 부산 날씨는 어떨거 같아",
        "이번 주말 제주도 날씨 좋아?",
        "다음달 뉴욕 날씨 어떨까"
    ]

    for query in queries:
        date, raw_location, location = query_parser.parse_query(query)
        print(f"쿼리: {query}")
        print(f"추출된 날짜: {date}")
        print(f"추출된 위치: {raw_location}")
        print(f"검증된 위치: {location}")
        print("-" * 50)


if __name__ == "__main__":
    main()
