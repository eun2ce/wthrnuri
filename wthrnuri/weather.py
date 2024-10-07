import os
import re
from typing import Optional

import dotenv
import requests
from MeCab import Tagger

dotenv.load_dotenv()
openweather_api_key = os.getenv("OPENWEATHER_API_KEY")
openweather_base_url = os.getenv("OPENWEATHER_BASE_URL")


def query(question) -> str:
    """
    질의에 따라 텍스트에서 사용자가 궁금해하는 날씨 정보를 적절히 검색하여 제공
    e.g.) "오늘 서울 날씨가 어때?"
    :param question:
    :return:
    """
    # 문장 에서 필요한 정보만 추출
    entities = parse_sentence(question)

    # 질의에 날짜 정보가 없는 경우 default 는 "오늘"
    date, day_after = "오늘", 0
    for idx, entity in enumerate(entities):
        token, tag = entity["token"], entity["tag"]
        result = get_ent_date(token, tag, question)
        if result is not None:
            date = result[0]
            day_after = result[1]
            entities.remove(entity)
            break

    # 지역 정보 추출
    region = parse_region_name(entities)
    region_name = region["token"]

    # 날씨 정보 조회
    weather_info = get_weather(region_name, day_after)

    return f"{date} {region_name}(의) 날씨는 {weather_info} (입)니다."


def get_weather(region_name, day_after) -> str:
    """
    지역명으로 위 경도를 찾고, 날씨 요약 정보 조회하여 반환
    :param region_name:
    :param day_after:
    :return:
    """
    lat, lon = get_geocode(region_name)
    weather_description = get_weather_from_geocode(lat, lon, day_after)

    return weather_description


def get_weather_from_geocode(lat, lon, day_after) -> str:
    """
    날씨 정보를 제공해주는 api를 통해 위,경도,날짜에 맞는 날씨 반환
    https://openweathermap.org/api/one-call-3
    :param lat:
    :param lon:
    :param day_after:
    :return:
    """
    url = openweather_base_url + f"/data/3.0/onecall?lang=kr&exclude=current,minutely,hourly&lat={lat}&lon={lon}&appid={openweather_api_key}"
    response = requests.get(url)

    weather_info = response.json()["daily"][day_after]
    weather_info_description = weather_info["weather"][0]["description"]

    return weather_info_description


def get_geocode(region_name) -> tuple[float, float]:
    """
    지역명 으로 부터 위도, 경도 찾아 반환
    https://openweathermap.org/api/geocoding-api
    :param region_name:
    :return:
    """
    url = openweather_base_url + f"/geo/1.0/direct?q={region_name}&appid={openweather_api_key}"

    response = requests.get(url)
    geo_info = response.json()[0]

    lat, lon = geo_info["lat"], geo_info["lon"]

    return lat, lon


def parse_region_name(entities) -> dict:
    """
    단어의 의미가 지역명 인 것을 찾아 반환
    e.g) [{'token': '서울', 'tag': 'NNP', 'mean': '지명'},{...} ...]
    :param entities:
    :return:
    """
    region_names = [item for item in entities if item["mean"] == "지명"]
    # 여러개 면 첫 번째 것 반환
    return region_names[0]


def parse_sentence(sentence) -> list:
    """
    필요한 엔티티만 추출하여 dict in list 형태로 반환
    e.g) [{'token': '서울', 'tag': 'NNP', 'mean': '지명'},{...} ...]
    :param sentence:
    :return:
    """
    tagger = Tagger()

    parsed = []
    stop_tag = ["SF", "EOS"]  # 마침표, 물음표, 느낌표, EOS 는 담지 않음

    for chunk in tagger.parse(sentence).splitlines():
        token = chunk.split("\t")[0]
        info = chunk.split("\t")[-1].split(",")
        tag = info[0]
        if tag not in stop_tag:
            mean = info[1]
            parsed.append({"token": token, "tag": tag, "mean": mean})
    return parsed


def get_ent_date(token, tag, sentence) -> Optional[tuple]:
    """
    날씨를 구하고자하는 날짜를 찾아 반환한다.
    :param token:
    :param tag:
    :param sentence:
    :return:
    """
    nday = re.compile(r"[가-힣\s\d]+일")
    nweek = re.compile(r"[가-힣\s\d]+주")

    day_dict = {
        "": 0,
        "오늘": 0,
        "금일": 0,
        "내일": 1,
        "익일": 1,
        "명일": 1,
        "모레": 2,
        "내일모레": 2,
        "낼모레": 2,
        "글피": 3,
        "삼명일": 3,
        "그글피": 4
    }

    after_day = None

    if (tag in {"MAG", "NNP", "NNG"}) & (token in day_dict.keys()):
        after_day = day_dict[token]

    if (tag == "SN"):
        if (nday.match(sentence) != None):
            day_after = 1
            find_day = re.compile(r"[\d]+일")
            day = find_day.findall(sentence)[0][:-1]
            after_day = day_after * int(day)
        elif (nweek.match(sentence) != None):
            # 무료 api 기준 8일 까지 조회 가능 하니까 "다음주 날씨 어때?" 형태의 질문이 있을 수 있음
            day_after = 7
            find_week = re.compile(r"[\d]+주")
            week = find_week.findall(sentence)[0][:-1]
            after_day = day_after * int(week)

    # TODO)
    # 오늘 날짜 기준 며칠,,? 계산해서 반환해야 할 듯
    # if (token == "다음주"): day_after = 7
    #
    # if (token == "다음"):
    #     if (re.compile("다음 주").match(sentence) != None): day_after = 7
    #
    # if (token =="이번"):
    #     if (re.compile("이번주").match(sentence) != None) | (re.compile("이번 주").match(sentence) != None): day_after = ?
    return (token, after_day) if (after_day is not None) else None


# if __name__ == '__main__':
#     answer = query("내일 서울 날씨 어때?")
#     print(f"answer: {answer}")
