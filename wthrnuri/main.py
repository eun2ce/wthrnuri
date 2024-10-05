import weather

if __name__ == '__main__':
    answer = weather.query(question="내일 서울 날씨 좋대?")
    print(answer)