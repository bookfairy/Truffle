$(document).ready(function() {
    /*--------------------  부트스트랩 기본 --------------------*/
    // 부트스트랩 툴팁을 활성화시키는 기본 코드
    $(function() {
        $('[data-toggle="tooltip"]').tooltip();
    });

    // 부트스트랩 토스트(알림)을 활성화시키는 기본 코드
    $('.toast').toast('show');
    
    // 파일 입력창에서 파일을 업로드할 때, input 태그 내 글자가 바뀌도록 하는 코드
    bsCustomFileInput.init();

    /*--------------------  전역 사용 --------------------*/
    // 스크롤을 인식하여 nav바를 자동으로 숨겨지도록 합니다
    // 상단바, 하단바(모바일), 토스트(알림) 등에 사용됩니다
    var last_scroll = 0;
    var current_scroll = 0;
    var $navbar = $('.navbar');
    var $toasts = $('#toast-container-inner');
    var navbar_height = $('.navbar.fixed-top').outerHeight();
    $toasts.css('margin-top', navbar_height);

    $(window).scroll(function() {
        current_scroll = $(window).scrollTop();

        if (current_scroll > last_scroll && current_scroll > navbar_height * 2) {
            $navbar.addClass('is-scrolled');
            $toasts.addClass('is-scrolled');
            $toasts.css('margin-top', 0);
        } else if (current_scroll < last_scroll && current_scroll > navbar_height) {
            $navbar.removeClass('is-scrolled');
            $toasts.removeClass('is-scrolled');
            $toasts.css('margin-top', navbar_height);
        }
        last_scroll = current_scroll;
    });

    // outline 클래스 아이콘을 가진 a 태그에 대해, hover시 클래스를 filled로 변화시켜주는 코드입니다
    // 헤더와 푸터 등의 아이콘 전 영역에서 사용됩니다
    $('a:has(.outline)')
        .mouseenter(function() {
            var $dest = $(this).find('.outline');
            $dest.removeClass('outline');
            $dest.addClass('filled');
        })
        .mouseleave(function() {
            var $dest = $(this).find('.filled');
            $dest.addClass('outline');
            $dest.removeClass('filled');
        });

    /*--------------------  메인 및 피드 페이지 --------------------*/
    // 이미지의 크기를 1:1 비율로 변화시킵니다
    // 피드 목록 페이지의 사진들에 사용됩니다
    $(window)
        .resize(function() {
            $('.feed-image-main').each(function() {
                $(this).css('height', $(this).width());
            });

            $('.feed-image-sub').each(function() {
                $(this).css('height', $(this).width());
            });
        })
        .resize();

    // 메인 이미지 위 3개의 서브 이미지에 hover 시 애니메이션과 함께 올라오도록 합니다
    // 피드 목록 페이지의 사진들에 사용됩니다
    $('.feed-image-sub-area')
        .mouseenter(function() {
            $(this).addClass('is-hovered');
        })
        .mouseleave(function() {
            $(this).removeClass('is-hovered');
        });

    /*-------------------- 기타 페이지 --------------------*/
    // 포스트 목록에서 태그를 클릭하면, 곧바로 검색하지 않고 상단의 검색창에 원격 입력시키는 코드입니다
    // 메인 페이지, 검색 페이지, 헤더에 사용됩니다
    $('.tag').on('click', function() {
        var tag_text = $(this)
            .text()
            .trim();
        var search_prev = $('#id_search').val();

        if (!search_prev.includes(tag_text)) {
            if (search_prev == '') {
                $('#id_search').val(search_prev + tag_text);
            } else {
                $('#id_search').val(search_prev + ' ' + tag_text);
            }
        }
    });
});