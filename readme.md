# ERD
<img src='/images/ERD.png'>


# 과정
1. 한 페이지의 recipe list를 받아온다. - I/O 바운드
2. 해당 recipe list에서 각 recipe들의 url을 파싱 - CPU 바운드
3. 각 recipe를 받아온다. - I/O 바운드
4. recipe 파싱 - CPU 바운드

# 설명
- recipes 경로에 **검색하려는 단어**(**keyword**)와 **page 번호**를 **query params**로 요청
  - api/v1/recipes/?search={keyword}&page={page}
- 레시피 사이트에서 검색한 단어와 page 번호만큼 크롤링
  - **Celery**를 이용하여 **requests를 요청 및 저장**하는 부분은 **비동기 수행**
  - 가져온 **html을 파싱하는 과정**은 **celery group**을 이용하여 **병렬 수행**
- 검색한 keyword는 **레시피와 다대다(ManyToMany) 관계로 저장**하여 **같은 단어로 검색 시 저장된 데이터를 먼저 불러온다.**
- 1 page 당 검색되는 레시피의 수는 **40개**로 제한


# 결과

### asyncio, multiprocessing
- 10페이지 크롤링 기준
  1. asyncio만 적용한 경우 - 72초
  2. multiprocessing만 적용한 경우 - 28초
  3. 과정 1,3은 asyncio, 4는 multiprocessing 적용한 경우 (2는 오래 걸리지 않으므로 적용 x) - 20초

### Celery
- 2페이지 크롤링 기준
- 레시피 크롤링 $\rightarrow$ 레시피 저장까지
  1. chain으로 크롤링한 경우 - 48.6초
  2. group으로 크롤링한 경우 - 9.7초


# Endpoints
### User

| 내용      | Method | URL                 |
| --------- | ------ | ------------------- |
| 회원가입  | POST   | api/v1/users/create |
| jwt token | POST   | api/v1/users/login  |

### Recipe
| 내용             | Method | URL                                                              |
| ---------------- | ------ | ---------------------------------------------------------------- |
| recipe 조회      | GET    | api/v1/recipes                                                   |
| recipe 검색&조회 | GET    | api/v1/recipes/?search={```keyword:str```}&page={```page:int```} |
| recipe 상세      | GET    | api/v1/recipes/{recipe_id}                                       |