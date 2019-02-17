# 데이터베이스 설정

* User : id(pk), email, name, password, register_date
* Follow : from_id(fk), to_id(fk), date
* Scrap : user_id(fk), playlist_id(fk), date
* Playlist : id(pk), title, description, content, date, tags, cost
  * Place : id(pk), address, name
    * Place_Content : id(pk), place_id(fk), content
      * Place_Content_Image : id(pk), place_content_id(fk), image
  * Photo : id(pk), photo, 
* Comment : id(pk), user_id(fk), travel_id(fk), content


# Assets
* [서버](https://truffle.run.goorm.io/)

# App
* 프로필, 로그인, 로그아웃, 피드(팔로우), 스크랩
* 여행 일정 게시판
* 코어

# 프론트
* 로그인 전 메인 : 랜딩 페이지
* 로그인 후 메인 : 피드 페이지
* 여행 일정 게시판 : 모든 일정 목록

# 페이지 종류
* 일정 피드 + 추천 게시물 
* 랜딩 페이지
* 일정 등록
* 프로필
-
* 회원가입
* 로그인
* 비밀번호 찾기
* 개인정보 수정

# 포스트 에디터 종류
* [스타 21k] https://quilljs.com/
* [스타 13k] https://yabwe.github.io/medium-editor/
* [스타 1k] http://linkesch.com/medium-editor-insert-plugin/
* [스타 2k] http://raphaelcruzeiro.github.io/jquery-notebook/

# 팔로잉
* 마이 페이지 (게시글 목록) 들어가면 Playlists, Places, Follwing/Followed 보여주기?

# 로그인
* https://www.w3schools.com/howto/howto_js_form_steps.asp
* https://codepen.io/collizo4sky/pen/ZGModv
