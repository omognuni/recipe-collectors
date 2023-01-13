# 과정

1. 한 페이지의 recipe list를 받아온다. - I/O 바운드
2. 해당 recipe list에서 각 recipe들의 url을 파싱 - CPU 바운드
3. 각 recipe를 받아온다. - I/O 바운드
4. recipe 파싱 - CPU 바운드

# 결과
- 10페이지 크롤링 기준
  1. asyncio만 적용한 경우 - 72초
  2. multiprocessing만 적용한 경우 - 28초
  3. 과정 1,3은 asyncio, 4는 multiprocessing 적용한 경우 (2는 오래 걸리지 않으므로 적용 x) - 20초

# 추가 개발
- DB에 recipe 저장 (url을 unique constraint)
- DB에 재료별 영양 정보 배치 작업
- 조리 과정 tts로 저장