# 게시물 등록 API 
DRF를 활용한 게시물 등록 API 개발 중
### 목표
1. 필수 기능 구현 
    - 카테고리 별 게시글 등록
    - 게시글 검색
    - 댓글, 대댓글(1 depth)
    - 대댓글 pagination
    - 게시글 view counting
2. Rest API 설계
3. Unit Test
4. redis 적용하여 loadtest
<br>

### 사용기술
- DRF, mysql
<br>

### 구현 API

1. User
  - 회원가입
  - 로그인
  - JWT token 인가
  
2. Board
  - 게시물 CRUD
  - 게시물 검색 : 카테고리 이름, 태그 이름 
  - cookie 활용하여 조회수 증가 방지 

3. Review
  - 댓글 & 대댓글
  - pagination


### UnitTests(진행중)
1. Board 
  - 게시물 CRUD
2. Review
  - 댓글 CRUD

<br>


### ERD
<br>

![스크린샷 2022-03-08 오후 11 44 39](https://user-images.githubusercontent.com/90910405/157261204-0d97c761-4776-42c2-a916-6632fd8d1086.png)
