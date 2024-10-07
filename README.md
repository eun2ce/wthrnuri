# wthrnuri

일상에서 사용하는 언어로부터 날씨 정보를 제공 합니다.  
e.g) "내일 서울 날씨 어때?" -> "내일 서울(의) 날씨는 맑음 (입)니다."

## 사전 설정

* MacOS에서 Anaconda 사용 환경 기준으로 작성합니다.
* 타 OS의 경우 링크 된 사이트를 통해 사용할 수 있습니다.

1.**openweaathermap api key 발급**

* [openweatherapi 키 발급 사이트](http://home.openweathermap.org)

```env
# .env
# 자세한 내용은 https://github.com/theskumar/python-dotenv 참고
OPENWEATHER_API_KEY={발급받은 api key}
OPENWEATHER_BASE_URL=http://api.openweathermap.org
```

2.**mecab 설치**

일상 용어를 처리할 수 있도록 하기 위해 사용됩니다.

```cmd
$ bash <(curl -s https://raw.githubusercontent.com/konlpy/konlpy/master/scripts/mecab.sh) # (Optional) Install MeCab
```

자세한 내용은 [링크](https://konlpy.org/ko/v0.4.0/install/)를 참고해주세요.

## 설치

1.**패키지 다운로드**

```cmd
$ gh repo clone eun2ce/wthrnuri -- --branch main
$ cd wthrnuri
$ mv {작성한 .env 파일의 path}/.env . # .env 파일을 해당 프로젝트에 옮김 

.
├── .env # 이 위치에 들어갈 것
├── .git
├── LICENSE
├── README.md
├── requirements.txt
├── setup.py
├── tests
│   └── test_weather.py
└── wthrnuri
    ├── __init__.py
    └── weather.py
```

2.**환경변수 파일 작성**

```cmd
$ vi .env.temp
# 키를 작성하고 저장
OPENWEATHER_API_KEY={your api key}
OPENWEATHER_BASE_URL=http://api.openweathermap.org

# 파일명을 .env로 변경
$ mv .env.temp .env
```

3.**패키지 설치**

```cmd
# 패키지 다운로드
$ pip install -e {wthrnuri root path}
```

예제 코드:

```python
# example_wthrnuri.py
import wthrnuri

if __name__ == '__main__':
    answer = wthrnuri.query(question="내일 서울 날씨 알려줘")

    print(answer)
```

출력:

```cmd
$ python example_wthrnuri.py
내일 서울(의) 날씨는 구름조금 (입)니다.
```

## Testing

```cmd
$ pytest
```
