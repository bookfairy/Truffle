function sns(f){
 var img = "썸네일 이미지 URL 을 입력하세요.";
 var title = "타이틀 내용을 입력하세요.";
 if(f == "F")  window.open("http://www.facebook.com/sharer/sharer.php?u=" + encodeURIComponent(location.href));
 else if(f == "T") window.open("http://twitter.com/intent/tweet?text="+encodeURIComponent(title)+"&url=" + encodeURIComponent(location.href));
}

 