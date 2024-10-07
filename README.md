# wthrnuri

일상에서 사용하는 언어로부터 날씨 정보를 제공 합니다.  
e.g) "내일 서울 날씨 어때?" -> "내일 서울(의) 날씨는 맑음 (입)니다."

## Quick Start

* MacOS에서 Anaconda 사용 환경 기준으로 작성합니다.
* 타 OS의 경우 링크 된 사이트를 통해 사용할 수 있습니다.

1.**openweaathermap api key 발급**

[openweatherapi 키 발급 사이트](http://home.openweathermap.org)

2.**mecab 설치**

일상 용어를 처리할 수 있도록 하는데 사용됩니다.

```cmd
$ bash <(curl -s https://raw.githubusercontent.com/konlpy/konlpy/master/scripts/mecab.sh) # (Optional) Install MeCab
```

자세한 내용은 [링크](https://konlpy.org/ko/v0.4.0/install/)를 참고해주세요.

3.**사용법**

* example_wthrnuri.py 작성

```python
# example_wthrnuri.py
import wthrnuri

if __name__ == '__main__':
    answer = wthrnuri.query(question="내일 서울 날씨 알려줘")

    print(answer)
```

## test

```cmd
$ pytest
```