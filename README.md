# 데이터베이스 설정

* User : id(pk), email, name, password, register_date
* Follow : from_id(fk), to_id(fk), date
* Post : id(pk), title, content, date
* Travel : id(pk), title, description, content, date, tags, cost
  * Place : id(pk), address, name
    * Place_Content : id(pk), place_id(fk), content
      * Place_Content_Image : id(pk), place_content_id(fk), image
  * Photo : id(pk), photo, 
* Comment_Post : id(pk), user_id(fk), post_id(fk), content
* Comment_Travel : id(pk), user_id(fk), travel_id(fk), content
* Scrap : user_id(fk), travel_id(fk), date

유저가 여러 개의 글을 가질 수 있으면
각각의 글에 유저 id를 갖는게 나은가?

태그: 포스트가 여러 개의 태그를 가질 수 있고, 태그가 여러 개의 포스트를 가질 수 있다면
스크랩: 유저가 여러 개의 포스트를 가질 수 있고, 포스트가 여러 개의 유저를 가질 수 있는....

# Assets
* [서버](https://truffle.run.goorm.io/)
* [아이콘](https://icons8.com/icons/set/truffle)
* [Argon Document](https://demos.creative-tim.com/argon-design-system/docs/getting-started/quick-start.html)
* [Argon GitHub](https://github.com/creativetimofficial/argon-design-system/tree/master/assets)

https://docs.djangoproject.com/en/2.1/topics/forms/
