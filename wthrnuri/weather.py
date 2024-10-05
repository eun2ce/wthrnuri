import re

import requests
from konlpy.tag import Okt

WEATHER_API_KEY = "*"

def query(question):
    answer = ""
    answer = get_weather_info(question)
    return answer

def get_entry_date(token, tag, sentence):
    day_after = "0"
    nday = re.compile("[가-힣\s\d]+일")
    nweek = re.compile("[가-힣\s\d]+주")

    TIME_KEYWORD = {"지금": 0, "오늘": 0, "현재": 0, "내일": 1, "내일모레": 2, "모레": 2}

    if (tag == "Noun") & (token in TIME_KEYWORD.keys()):
        day_after = TIME_KEYWORD[token]

    if (tag == "Number"):
        if (nday.match(sentence) != None):
            afterday = 1
            findDay = re.compile("[\d]+일")
            day = findDay.findall(sentence)[0][:-1]
            day_after = afterday * int(day)
        elif (nweek.match(sentence) != None):
            # 무료 api 기준 8일 까지 조회 가능 하니까 "일주일 뒤 날씨 어때?" 형태의 질문이 있을 수 있음
            afterday = 7
            findWeek = re.compile("[\d]+주")
            week = findWeek.findall(sentence)[0][:-1]
            day_after = afterday * int(week)
        else:
            day_after = 0
    # TODO)
    # 오늘 날짜 기준 며칠,,? 계산해서 반환해야 할 듯
    # if (token == "다음주"): day_after = 7
    #
    # if (token == "다음"):
    #     if (re.compile("다음 주").match(sentence) != None): day_after = 7
    #
    # if (token =="이번"):
    #     if (re.compile("이번주").match(sentence) != None) | (re.compile("이번 주").match(sentence) != None): eday_after = ?

    return day_after

def get_date(token, tag, entities, sentence):
    entities["after_day"] = get_entry_date(token, tag, sentence)
    return entities


def get_geocode(token, entities):
    # 지역의 위경도 반환
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={token}&appid={WEATHER_API_KEY}"

    response = requests.get(url).json()[0]
    lat,lon = response["lat"], response["lon"]

    entities["lat"] = lat
    entities["lon"] = lon

    return entities

def get_weather_info(sentence):
    entities = {}

    okt = Okt()
    # disintegrated sentence
    dsn_sentences = okt.pos(sentence, stem=True)  # norm 정규화, stem 어간 추출
    ndate = dsn_sentences[0]
    region_name = dsn_sentences[1]

    entities = get_date(ndate[0], ndate[1], entities, dsn_sentences)
    entities = get_geocode(region_name[0], entities)

    after_day = entities["after_day"]
    lat, lon = entities["lat"], entities["lon"]

    url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&lang=kr&exclude=daily&appid={WEATHER_API_KEY}"
    response = requests.get(url).json()["list"][after_day]

    return answer_format(date=ndate[0], region=region_name[0], state=response["weather"][0]["description"])

def answer_format(date, region, state):
    return f"{date} {region}(의) 날씨는 {state} (입)니다."