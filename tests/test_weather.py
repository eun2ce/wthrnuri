import unittest
from unittest.mock import MagicMock, patch

from wthrnuri.weather import Weather


class TestWeather(unittest.TestCase):
    def setUp(self):
        self.wthr = Weather()

    def test_get_weather_info(self):
        er = "내일 레이캬비크(의) 날씨는 맑음 (입)니다."
        mock_data = {"lat": 64.146, "lon": -21.9422, "timezone": "Atlantic/Reykjavik", "timezone_offset": 0, "daily": [
            {"dt": 1728219600, "sunrise": 1728201123, "sunset": 1728239954, "moonrise": 1728223020,
             "moonset": 1728236520, "moon_phase": 0.11, "summary": "There will be clear sky today",
             "temp": {"day": 279.06, "min": 275.21, "max": 279.36, "night": 276.55, "eve": 277.16, "morn": 275.25},
             "feels_like": {"day": 277.53, "night": 274.31, "eve": 276.17, "morn": 272.12}, "pressure": 1021,
             "humidity": 44, "dew_point": 268.36, "wind_speed": 3.7, "wind_deg": 44, "wind_gust": 4.14,
             "weather": [{"id": 800, "main": "Clear", "description": "맑음", "icon": "01d"}], "clouds": 0, "pop": 0,
             "uvi": 0.78}, {"dt": 1728306000, "sunrise": 1728287699, "sunset": 1728326142, "moonrise": 0, "moonset": 0,
                            "moon_phase": 0.14,
                            "summary": "You can expect clear sky in the morning, with partly cloudy in the afternoon",
                            "temp": {"day": 277.71, "min": 275.21, "max": 278.08, "night": 276.12, "eve": 276.6,
                                     "morn": 275.32},
                            "feels_like": {"day": 276.38, "night": 276.12, "eve": 276.6, "morn": 272.71},
                            "pressure": 1022, "humidity": 45, "dew_point": 266.55, "wind_speed": 2.82, "wind_deg": 43,
                            "wind_gust": 2.82,
                            "weather": [{"id": 800, "main": "Clear", "description": "맑음", "icon": "01d"}], "clouds": 0,
                            "pop": 0, "uvi": 0.76},
            {"dt": 1728392400, "sunrise": 1728374276, "sunset": 1728412331, "moonrise": 0, "moonset": 0,
             "moon_phase": 0.18,
             "summary": "You can expect partly cloudy with snow in the morning, with partly cloudy with rain in the afternoon",
             "temp": {"day": 277.99, "min": 275.56, "max": 278.23, "night": 276.05, "eve": 275.62, "morn": 276},
             "feels_like": {"day": 275.02, "night": 274.03, "eve": 271.37, "morn": 273.55}, "pressure": 1020,
             "humidity": 61, "dew_point": 270.83, "wind_speed": 4.91, "wind_deg": 88, "wind_gust": 7.24,
             "weather": [{"id": 616, "main": "Snow", "description": "비와 눈", "icon": "13d"}], "clouds": 100, "pop": 0.54,
             "rain": 0.67, "snow": 0.16, "uvi": 0.53},
            {"dt": 1728478800, "sunrise": 1728460853, "sunset": 1728498521, "moonrise": 0, "moonset": 0,
             "moon_phase": 0.21, "summary": "There will be partly cloudy today",
             "temp": {"day": 275.55, "min": 274.42, "max": 276.13, "night": 274.59, "eve": 275.49, "morn": 274.72},
             "feels_like": {"day": 272.18, "night": 270.85, "eve": 271.37, "morn": 270.97}, "pressure": 1021,
             "humidity": 65, "dew_point": 269.27, "wind_speed": 4.62, "wind_deg": 347, "wind_gust": 5.98,
             "weather": [{"id": 803, "main": "Clouds", "description": "튼구름", "icon": "04d"}], "clouds": 62, "pop": 0.48,
             "uvi": 0.65}, {"dt": 1728565200, "sunrise": 1728547430, "sunset": 1728584710, "moonrise": 0, "moonset": 0,
                            "moon_phase": 0.25, "summary": "Expect a day of partly cloudy with rain",
                            "temp": {"day": 275.02, "min": 274.05, "max": 275.46, "night": 274.16, "eve": 274.93,
                                     "morn": 274.36},
                            "feels_like": {"day": 270.37, "night": 269.5, "eve": 270.59, "morn": 272.5},
                            "pressure": 1011, "humidity": 95, "dew_point": 274, "wind_speed": 5.38, "wind_deg": 150,
                            "wind_gust": 7.37,
                            "weather": [{"id": 500, "main": "Rain", "description": "실 비", "icon": "10d"}], "clouds": 99,
                            "pop": 1, "rain": 4.57, "uvi": 0.48},
            {"dt": 1728651600, "sunrise": 1728634009, "sunset": 1728670901, "moonrise": 1728673740,
             "moonset": 1728683820, "moon_phase": 0.27, "summary": "Expect a day of partly cloudy with clear spells",
             "temp": {"day": 273.74, "min": 272.51, "max": 275.11, "night": 275.11, "eve": 274.54, "morn": 272.54},
             "feels_like": {"day": 267.73, "night": 269.64, "eve": 269.13, "morn": 266.57}, "pressure": 1009,
             "humidity": 62, "dew_point": 267.11, "wind_speed": 7.74, "wind_deg": 1, "wind_gust": 11.5,
             "weather": [{"id": 800, "main": "Clear", "description": "맑음", "icon": "01d"}], "clouds": 9, "pop": 0.26,
             "uvi": 1},
            {"dt": 1728738000, "sunrise": 1728720588, "sunset": 1728757091, "moonrise": 1728758160, "moonset": 0,
             "moon_phase": 0.31, "summary": "Expect a day of partly cloudy with snow",
             "temp": {"day": 277.45, "min": 275.12, "max": 277.45, "night": 275.12, "eve": 275.95, "morn": 276.12},
             "feels_like": {"day": 273.74, "night": 275.12, "eve": 274.05, "morn": 271.25}, "pressure": 1014,
             "humidity": 67, "dew_point": 271.56, "wind_speed": 8.98, "wind_deg": 316, "wind_gust": 11.31,
             "weather": [{"id": 600, "main": "Snow", "description": "가벼운 눈", "icon": "13d"}], "clouds": 17, "pop": 0.28,
             "snow": 0.6, "uvi": 1},
            {"dt": 1728824400, "sunrise": 1728807167, "sunset": 1728843282, "moonrise": 1728843600,
             "moonset": 1728779040, "moon_phase": 0.35,
             "summary": "You can expect partly cloudy in the morning, with snow in the afternoon",
             "temp": {"day": 275.8, "min": 274.08, "max": 276.3, "night": 275.25, "eve": 275.09, "morn": 274.08},
             "feels_like": {"day": 272, "night": 271.87, "eve": 271.32, "morn": 270.8}, "pressure": 1012,
             "humidity": 51, "dew_point": 266.34, "wind_speed": 4.2, "wind_deg": 94, "wind_gust": 6.3,
             "weather": [{"id": 600, "main": "Snow", "description": "가벼운 눈", "icon": "13d"}], "clouds": 97, "pop": 0.4,
             "snow": 0.13, "uvi": 1}]}

        response = MagicMock()
        response.json.return_value = mock_data

        patch("requests.get", return_value=mock_data)

        ar = self.wthr.get_weather_info("내일 레이캬비크 날씨 알려줘")

        assert ar == er

    def test_get_ent_data(self):
        question = "내일 서울 날씨 알려줘"
        ar = self.wthr.get_ent_date("내일", "NNP", question)

        # 함수: 키워드 반환 e.g) "내일"
        # 클래스 init 변수 entities: 오늘 + after date
        er_date_keyword = "내일"
        er_dict_entities = {"DATE": 1}

        assert ar == er_date_keyword
        assert self.wthr.entities == er_dict_entities

    def test_get_ent_geocode(self):
        er = (39.906217, 116.3912757)
        mock_data = [{"name": "Beijing",
                      "local_names": {"tg": "Пекин", "th": "ปักกิ่ง", "su": "Beijing", "cs": "Peking", "hr": "Peking",
                                      "sv": "Beijing", "ro": "Beijing", "fo": "Beijing", "fr": "Pékin",
                                      "ta": "பெய்ஜிங்", "mi": "Beijing", "pl": "Pekin", "ug": "بېيجىڭ شەھىرى",
                                      "es": "Pekín", "ne": "बेइजिङ", "jv": "Beijing", "si": "බෙයිජිං", "za": "Baekging",
                                      "tl": "Beijing", "uz": "Pekin", "af": "Beijing", "am": "ቤዪጂንግ", "kn": "ಬೀಜಿಂಗ್",
                                      "kl": "Beijing", "sq": "Pekini", "eu": "Pekin", "dv": "ބީޖިންގ", "gd": "Beijing",
                                      "ca": "Pequín", "tk": "Pekin", "br": "Beijing", "qu": "Pikkin", "kv": "Пекин",
                                      "an": "Pequín", "pt": "Pequim", "zh": "北京市", "da": "Beijing", "mr": "ीजिंग",
                                      "sw": "Beijing", "be": "Пекін", "lv": "Pekina", "gl": "Pequín", "en": "Beijing",
                                      "te": "బీజింగ్", "hy": "Պեկին", "bn": "বেইজিং", "sa": "बीजिङ्ग्",
                                      "vi": "Bắc Kinh", "hu": "Peking", "de": "Peking", "is": "Beijing",
                                      "feature_name": "Beijing", "ht": "Peken", "eo": "Pekino", "tr": "Pekin",
                                      "sr": "Пекинг", "my": "ပေကျင်းမြို့", "mg": "Beijing", "cy": "Beijing",
                                      "ku": "Pekîn", "bg": "Пекин", "bo": "པེ་ཅིང་གྲོང་ཁྱེར།", "uk": "Пекін",
                                      "hi": "बीजिंग", "sc": "Beijing", "fa": "پکن", "lo": "ປັກກິ່ງ", "ur": "بیجنگ",
                                      "lt": "Pekinas", "ms": "Beijing", "na": "Beijing", "ko": "베이징 시", "gu": "બેઇજિંગ",
                                      "id": "Beijing", "ka": "პეკინი", "ml": "ബെയ്‌ജിങ്ങ്", "cv": "Пекин",
                                      "tt": "Пекин", "ba": "Пекин", "ru": "Пекин", "io": "Beijing", "et": "Peking",
                                      "fi": "Peking", "nn": "Beijing", "os": "Пекин", "it": "Pechino", "gn": "Pekĩ",
                                      "so": "Beijing", "mk": "Пекинг", "la": "Pechinum", "pa": "ਬੀਜਿੰਗ",
                                      "yi": "בייזשינג", "mn": "Бээжин", "az": "Pekin", "kw": "Beijing", "ia": "Beijing",
                                      "kk": "Бейжің", "he": "בייג'ין", "ar": "بكين", "ay": "Pekin'", "sl": "Peking",
                                      "ps": "بېجنګ", "ga": "Béising", "sk": "Peking", "no": "Beijing", "el": "Πεκίνο",
                                      "gv": "Beijing", "nl": "Peking", "oc": "Pequin", "km": "ប៉េកាំង",
                                      "ascii": "Beijing", "yo": "Beijing", "ja": "北京市"}, "lat": 39.906217,
                      "lon": 116.3912757, "country": "CN", "state": "Beijing"}]

        patch("requests.get", return_value=mock_data)
        ar = self.wthr.get_ent_geocode("베이징")

        assert ar == er

    def test_get_answer_format(self):
        pass
