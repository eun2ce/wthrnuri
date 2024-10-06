import weather

if __name__ == '__main__':
    answer = weather.query(question="내일 서울 날씨 알려줘")
    print(answer)