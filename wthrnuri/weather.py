import os
import re

import requests
from MeCab import Tagger
from dotenv import load_dotenv
from konlpy.tag import Mecab


def query(question):
    answer = ""
    wthr = Weather()
    answer = wthr.get_weather_info(question)
    return answer

class Weather:
    def __init__(self):
        # env
        load_dotenv()
        self.API_KEY = os.environ["API_KEY"]
        self.API_BASE_URL = os.environ["API_BASE_URL"]

        self.mecab = Mecab()
        self.tagger = Tagger()
        self.entities = {}

    def get_weather_info(self, sentence):
        # disintegrated sentence
        dsn_sentences = self.tagger.parse(sentence).splitlines()

        date_keyword = None

        # e.g) ['서울\tNNP,지명,T,서울,*,*,*,*', '내일\tNNP,지명,T,내일,*,*,*,*', '날씨\tNNG,*,F,날씨,*,*,*,*', '좋\tVA,*,T,좋,*,*,*,*', '대\tEF,*,F,대,*,*,*,*', '?\tSF,*,*,*,*,*,*,*', 'EOS']
        for idx, pos in enumerate(dsn_sentences):
            token = pos.split("\t")[0]
            tag = pos.split("\t")[-1].split(",")[0]
            self.get_ent_date(token, tag, sentence)

            if "DATE" in self.entities:
                date_keyword = token
                dsn_sentences.pop(idx)
                break

        # 지명으로 분류된 형태소만 추출
        region_sentence = [s for s in dsn_sentences if "지명" in s]

        # 여러개면 처음 지명으로 조회
        region_name = region_sentence[0].split("\t")[0] or "서울"
        lat, lon = self.get_ent_geocode(region_name)

        url = self.API_BASE_URL + f"/data/3.0/onecall?lang=kr&exclude=current,minutely,hourly&lat={lat}&lon={lon}&appid={self.API_KEY}"
        response = requests.get(url)

        afterday = self.entities["DATE"]
        weather_info = response.json()["daily"][afterday]

        return self.get_answer_format(date=date_keyword, region=region_name, state=weather_info["weather"][0]["description"])

    def get_ent_date(self, token, tag, sentence):
        nday = re.compile("[가-힣\s\d]+일")
        nweek = re.compile("[가-힣\s\d]+주")

        DAY_KEYWORD = {"지금": 0, "오늘": 0, "현재": 0, "내일": 1, "내일모레": 2, "모레": 2}

        if (tag in {"MAG", "NNP", "NNG"}) & (token in DAY_KEYWORD.keys()):
            self.entities["DATE"] = DAY_KEYWORD[token]

        if (tag == "SN"):
            if (nday.match(sentence) != None):
                day_after = 1
                find_day = re.compile("[\d]+일")
                day = find_day.findall(sentence)[0][:-1]
                self.entities["DATE"] = day_after * int(day)
            elif (nweek.match(sentence) != None):
                # 무료 api 기준 8일 까지 조회 가능 하니까 "다음주 날씨 어때?" 형태의 질문이 있을 수 있음
                day_after = 7
                find_week = re.compile("[\d]+주")
                week = find_week.findall(sentence)[0][:-1]
                self.entities["DATE"] = day_after * int(week)
            else:
                self.entities["DATE"] = 0

        # TODO)
        # 오늘 날짜 기준 며칠,,? 계산해서 반환해야 할 듯
        # if (token == "다음주"): day_after = 7
        #
        # if (token == "다음"):
        #     if (re.compile("다음 주").match(sentence) != None): day_after = 7
        #
        # if (token =="이번"):
        #     if (re.compile("이번주").match(sentence) != None) | (re.compile("이번 주").match(sentence) != None): day_after = ?
        return token


    def get_ent_geocode(self, region_name):
        # 지역의 위경도 반환
        url = self.API_BASE_URL + f"/geo/1.0/direct?q={region_name}&appid={self.API_KEY}"

        response = requests.get(url)
        geo_info = response.json()[0]

        lat,lon = geo_info["lat"], geo_info["lon"]

        return lat, lon

    def get_answer_format(self, date, region, state):
        return f"{date} {region}(의) 날씨는 {state} (입)니다."