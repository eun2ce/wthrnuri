import pytest

from wthrnuri.weather import get_weather_from_geocode, get_geocode, parse_region_name, parse_sentence, get_ent_date, \
    get_weather, query


def test_query(mocker):
    question = "내일 서울 날씨 어때?"

    mocker.patch("wthrnuri.weather.get_geocode", return_value=(37.5667, 126.9783))
    mocker.patch("wthrnuri.weather.get_weather_from_geocode", return_value="맑음")

    er = "내일 서울(의) 날씨는 맑음 (입)니다."
    ar = query(question)

    assert ar == er


def test_get_weather(mocker):  # wrapping function... 무엇을 확인 해야 좋을지 고민해 볼 것
    region_name, day_after = "서울", "1"
    mocker.patch("wthrnuri.weather.get_geocode", return_value=(37.5667, 126.9783))
    mocker.patch("wthrnuri.weather.get_weather_from_geocode", return_value="맑음")

    er = "맑음"
    ar = get_weather(region_name, day_after)

    assert ar == er


def test_get_weather_from_geocode(mocker):
    mock_data = {"lat": 37.5667, "lon": 126.9783, "timezone": "Asia/Seoul", "timezone_offset": 32400, "daily": [
        {"dt": 1728270000, "sunrise": 1728250359, "sunset": 1728292016, "moonrise": 1728265320, "moonset": 1728299400,
         "moon_phase": 0.13, "summary": "There will be partly cloudy today",
         "temp": {"day": 293.37, "min": 289.32, "max": 294.92, "night": 291.41, "eve": 292.34, "morn": 289.32},
         "feels_like": {"day": 292.75, "night": 291.07, "eve": 291.91, "morn": 288.53}, "pressure": 1018,
         "humidity": 50, "dew_point": 282.41, "wind_speed": 2.97, "wind_deg": 326, "wind_gust": 3.45,
         "weather": [{"id": 804, "main": "Clouds", "description": "온흐림", "icon": "04d"}], "clouds": 100, "pop": 0.03,
         "uvi": 4.36},
        {"dt": 1728356400, "sunrise": 1728336813, "sunset": 1728378327, "moonrise": 1728355500, "moonset": 1728388380,
         "moon_phase": 0.16, "summary": "Expect a day of partly cloudy with clear spells",
         "temp": {"day": 295.16, "min": 288.42, "max": 296.81, "night": 291.78, "eve": 295.08, "morn": 288.5},
         "feels_like": {"day": 294.64, "night": 291.34, "eve": 294.43, "morn": 288.08}, "pressure": 1018,
         "humidity": 47, "dew_point": 283.16, "wind_speed": 2.69, "wind_deg": 92, "wind_gust": 5.62,
         "weather": [{"id": 800, "main": "Clear", "description": "맑음", "icon": "01d"}], "clouds": 0, "pop": 0.18,
         "uvi": 4.35},
        {"dt": 1728442800, "sunrise": 1728423267, "sunset": 1728464639, "moonrise": 1728445500, "moonset": 1728477900,
         "moon_phase": 0.2, "summary": "Expect a day of partly cloudy with rain",
         "temp": {"day": 295.45, "min": 289.23, "max": 296.2, "night": 292.26, "eve": 294.41, "morn": 289.29},
         "feels_like": {"day": 294.94, "night": 291.77, "eve": 293.79, "morn": 288.89}, "pressure": 1018,
         "humidity": 46, "dew_point": 283.01, "wind_speed": 2.43, "wind_deg": 98, "wind_gust": 5.58,
         "weather": [{"id": 500, "main": "Rain", "description": "실 비", "icon": "10d"}], "clouds": 39, "pop": 0.29,
         "rain": 0.16, "uvi": 4.1},
        {"dt": 1728529200, "sunrise": 1728509721, "sunset": 1728550951, "moonrise": 1728535200, "moonset": 1728567900,
         "moon_phase": 0.23, "summary": "Expect a day of partly cloudy with rain",
         "temp": {"day": 295.04, "min": 289.46, "max": 296.35, "night": 292.28, "eve": 293.72, "morn": 289.46},
         "feels_like": {"day": 294.54, "night": 291.82, "eve": 293.14, "morn": 289.16}, "pressure": 1017,
         "humidity": 48, "dew_point": 283.39, "wind_speed": 3.59, "wind_deg": 260, "wind_gust": 3.44,
         "weather": [{"id": 500, "main": "Rain", "description": "실 비", "icon": "10d"}], "clouds": 3, "pop": 0.56,
         "rain": 0.77, "uvi": 4.05},
        {"dt": 1728615600, "sunrise": 1728596176, "sunset": 1728637265, "moonrise": 1728624420, "moonset": 1728658380,
         "moon_phase": 0.25, "summary": "There will be clear sky today",
         "temp": {"day": 296.04, "min": 289.27, "max": 297.22, "night": 293.02, "eve": 294.52, "morn": 289.27},
         "feels_like": {"day": 295.53, "night": 292.68, "eve": 294.07, "morn": 288.84}, "pressure": 1020,
         "humidity": 44, "dew_point": 283, "wind_speed": 3.15, "wind_deg": 271, "wind_gust": 3.42,
         "weather": [{"id": 800, "main": "Clear", "description": "맑음", "icon": "01d"}], "clouds": 0, "pop": 0,
         "uvi": 4.19},
        {"dt": 1728702000, "sunrise": 1728682631, "sunset": 1728723579, "moonrise": 1728713280, "moonset": 0,
         "moon_phase": 0.3, "summary": "There will be clear sky today",
         "temp": {"day": 296.71, "min": 290, "max": 298.24, "night": 294.33, "eve": 296.42, "morn": 290},
         "feels_like": {"day": 296.27, "night": 293.81, "eve": 295.79, "morn": 289.7}, "pressure": 1024, "humidity": 44,
         "dew_point": 283.72, "wind_speed": 1.14, "wind_deg": 80, "wind_gust": 2.22,
         "weather": [{"id": 800, "main": "Clear", "description": "맑음", "icon": "01d"}], "clouds": 0, "pop": 0.04,
         "uvi": 5},
        {"dt": 1728788400, "sunrise": 1728769086, "sunset": 1728809893, "moonrise": 1728801780, "moonset": 1728749100,
         "moon_phase": 0.33, "summary": "You can expect clear sky in the morning, with partly cloudy in the afternoon",
         "temp": {"day": 296.72, "min": 290.26, "max": 298.26, "night": 294.29, "eve": 296.11, "morn": 290.26},
         "feels_like": {"day": 296.18, "night": 293.69, "eve": 295.43, "morn": 289.62}, "pressure": 1026,
         "humidity": 40, "dew_point": 282.22, "wind_speed": 1.76, "wind_deg": 102, "wind_gust": 2.93,
         "weather": [{"id": 800, "main": "Clear", "description": "맑음", "icon": "01d"}], "clouds": 0, "pop": 0,
         "uvi": 5},
        {"dt": 1728874800, "sunrise": 1728855542, "sunset": 1728896209, "moonrise": 1728889980, "moonset": 1728839940,
         "moon_phase": 0.37, "summary": "There will be partly cloudy today",
         "temp": {"day": 294.66, "min": 290.74, "max": 296.4, "night": 293.65, "eve": 295.08, "morn": 290.74},
         "feels_like": {"day": 294.2, "night": 293.22, "eve": 294.58, "morn": 290.04}, "pressure": 1023, "humidity": 51,
         "dew_point": 284.1, "wind_speed": 2.07, "wind_deg": 132, "wind_gust": 3.16,
         "weather": [{"id": 804, "main": "Clouds", "description": "온흐림", "icon": "04d"}], "clouds": 100, "pop": 0,
         "uvi": 5}]}

    # 내일 서울 날씨
    lat, lon, day_after = 37.5667, 126.9783, 1

    mock_response = mocker.MagicMock()
    mock_response.json.return_value = mock_data

    mocker.patch("requests.get", return_value=mock_response)

    er = "맑음"
    ar = get_weather_from_geocode(lat, lon, day_after)

    assert ar == er


def test_get_geocode(mocker):
    mock_data = [{"name": "Seoul",
                  "local_names": {"mk": "Сеул", "uz": "Seul", "gl": "Seúl", "zh": "首尔市 / 首爾", "be": "Сеул",
                                  "nl": "Seoel", "ta": "சியோல்", "ur": "سؤل", "eo": "Seulo", "el": "Σεούλ",
                                  "is": "Seúl", "hy": "Սեուլ", "he": "סיאול", "sv": "Seoul", "cv": "Сеул",
                                  "km": "សេអ៊ូល", "fa": "سئول", "bg": "Сеул", "qu": "Siul", "af": "Seoel", "mr": "सोल",
                                  "tr": "Seul", "tg": "Сеул", "es": "Seúl", "fi": "Soul", "bo": "སེ་ཨུལ།", "hr": "Seul",
                                  "os": "Сеул", "tk": "Seul", "am": "ሶል", "pl": "Seul", "ml": "സോൾ", "eu": "Seul",
                                  "bh": "सियोल", "an": "Seúl", "ka": "სეული", "ca": "Seül", "it": "Seul", "sr": "Сеул",
                                  "yi": "סעאל", "ja": "ソウル", "kk": "Сеул", "ky": "Сеул", "oc": "Seol",
                                  "my": "ဆိုးလ်မြို့", "la": "Seulum", "sl": "Seul", "ba": "Сеул", "de": "Seoul",
                                  "mn": "Сөүл", "bn": "সিওল", "cs": "Soul", "sk": "Soul", "bs": "Seul", "ru": "Сеул",
                                  "et": "Sŏul", "pt": "Seul", "lt": "Seulas", "uk": "Сеул", "kn": "ಸೌಲ್", "ku": "Sêûl",
                                  "ro": "Seul", "az": "Seul", "lv": "Seula", "th": "โซล", "vi": "Seoul", "en": "Seoul",
                                  "vo": "Söul", "ko": "서울", "ar": "سول", "hu": "Szöul", "fr": "Séoul", "hi": "सियोल"},
                  "lat": 37.5666791, "lon": 126.9782914, "country": "KR"}]

    # 서울의 위, 경도 조회
    region_name = "서울"

    mock_response = mocker.MagicMock()
    mock_response.json.return_value = mock_data

    mocker.patch("requests.get", return_value=mock_response)

    er = (37.5666791, 126.9782914)
    ar = get_geocode(region_name)

    assert ar == er


def test_parse_region_name():
    mock_data = [{'token': '모레', 'tag': 'MAG', 'mean': '성분부사|시간부사'}, {'token': '도쿄', 'tag': 'NNP', 'mean': '지명'},
                 {'token': '날씨', 'tag': 'NNG', 'mean': '*'}, {'token': '가', 'tag': 'JKS', 'mean': '*'},
                 {'token': '좋', 'tag': 'VA', 'mean': '*'}, {'token': '대', 'tag': 'EF', 'mean': '*'}]

    er = {'token': '도쿄', 'tag': 'NNP', 'mean': '지명'}
    ar = parse_region_name(mock_data)

    assert ar == er


def test_parse_sentence():
    mock_data = "내일 방콕 날씨 비온다 했나?"

    er = [{'mean': '지명', 'tag': 'NNP', 'token': '내일'},
          {'mean': '지명', 'tag': 'NNP', 'token': '방콕'},
          {'mean': '*', 'tag': 'NNG', 'token': '날씨'},
          {'mean': '*', 'tag': 'NNP', 'token': '비온다'},
          {'mean': '*', 'tag': 'VV+EP', 'token': '했'},
          {'mean': '*', 'tag': 'EF', 'token': '나'}]
    ar = parse_sentence(mock_data)

    assert ar == er


@pytest.mark.parametrize("token, tag, sentence, er", [("내일", "NNP", "내일 방콕 날씨 비온다 했나?", ("내일", 1)),
                                                      ("모레", "MAG", "모레 도쿄 날씨가 좋대?", ("모레", 2)),
                                                      ("오늘", "MAG", "서울 날씨가 오늘 어떻대?", ("오늘", 0)),
                                                      ("8", "SN", "8일 뒤 베이징 날씨는?", ("8", 8))  # TODO) er: ("8일후", 8)
                                                      ])
def test_get_ent_date(token, tag, sentence, er):
    ar = get_ent_date(token, tag, sentence)
    assert ar == er
