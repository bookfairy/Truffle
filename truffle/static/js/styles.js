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

    // + 일정 영역에서는 헤더바를 투명하게 만듭니다
    if (
        window.location.pathname.includes('playlists') &&
        !window.location.pathname.includes('search')
    ) {
        if (current_scroll > navbar_height * 4) {
            $('.navbar.fixed-top').removeClass('transparent');
        } else {
            $('.navbar.fixed-top').addClass('transparent');
        }
    }
    $(window).scroll(function() {
        current_scroll = $(window).scrollTop();

        if (
            window.location.pathname.includes('playlists') &&
            !window.location.pathname.includes('search')
        ) {
            if (current_scroll > navbar_height * 4) {
                $('.navbar.fixed-top').removeClass('transparent');
            } else {
                $('.navbar.fixed-top').addClass('transparent');
            }
        }

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

    /*-------------------- 글 쓰기 페이지 --------------------*/
    // owl 캐러셀의 전통적 nexted 오류 해결
    function stopOwlPropagation(element) {
        jQuery(element).on('to.owl.carousel', function(e) { e.stopPropagation(); });
        jQuery(element).on('next.owl.carousel', function(e) { e.stopPropagation(); });
        jQuery(element).on('prev.owl.carousel', function(e) { e.stopPropagation(); });
        jQuery(element).on('destroy.owl.carousel', function(e) { e.stopPropagation(); });
        jQuery(element).on('add.owl.carousel', function(e) { e.stopPropagation(); });
        jQuery(element).on('remove.owl.carousel', function(e) { e.stopPropagation(); });
        jQuery(element).on('refresh.owl.carousel', function(e) { e.stopPropagation(); });
        jQuery(element).on('update.owl.carousel', function(e) { e.stopPropagation(); });
    }
    stopOwlPropagation('.owl-carousel');
    stopOwlPropagation('.owl-carousel-image');
    
    // 메인 이미지(.main-image) 클릭 시 사진 업로드(input#id_main_image)
    $('.main-image').on('click', function() {
        $('input#id_main_image').click();
    });

    // 사진 업로드(input#id_main_image) 시 두 군데에서 프리뷰
    $('input#id_main_image').on('change', function() {
        if (this.files && this.files[0]) {
            var reader = new FileReader();
            reader.onload = function(e) {
                $('.main-image').css('background-image', "url('" + e.target.result + "')");
                $('.background-main-image').css(
                    'background-image',
                    "linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), url('" +
                        e.target.result +
                        "')"
                );
            };
            reader.readAsDataURL(this.files[0]);
        }
    });

    // 카드 사진 업로드 버튼(button.upload) 클릭 시 사진 업로드(input#id_image1)
    $(document).on('click', '.upload', function() {
        $(this).next().click();
        return false;
    });

    // 사진 여러 개 업로드(input#id_image1) 시 파일 프리뷰
    $(document).on('change', '.upload + input[multiple]', function() {
        stopOwlPropagation('.owl-carousel');
        stopOwlPropagation('.owl-carousel-image');
        var $image_area = $(this).closest('.card.photo').children('.owl-carousel-image');
        
        for (var i = 0; i <= $image_area.find('.owl-item').length; i++) {
            $image_area.owlCarousel('remove', [i]).owlCarousel('refresh');
        }

        if (this.files) $.each(this.files, function(i, file) {
            if (!/\.(jpe?g|png|gif)$/i.test(file.name)) {
                return alert(file.name + ' 은 이미지 파일이 아닙니다!');
            } // else...

            var reader = new FileReader();
            
            // $image_area.owlCarousel('add', $('<img/>', { src: this.result }).html()).owlCarousel('update');
            
            $(reader).on('load', function() {
                $image_area.owlCarousel('add', $('<img/>', { src: this.result })).owlCarousel('update');
            });

            reader.readAsDataURL(file);
        });
    });

    // 카드 추가
    $(document).on('click', '#add-more', function() {
        stopOwlPropagation('.owl-carousel');
        stopOwlPropagation('.owl-carousel-image');
        var form_idx = parseInt($('#id_form-TOTAL_FORMS').val());
        $('#photos-container')
            .trigger('add.owl.carousel', [
                $('#empty-form')
                    .html()
                    .replace(/__prefix__/g, form_idx)
                    .replace('image', `img-card-${form_idx}`),
                $('.card.photo').length + 1
            ])
            .trigger('refresh.owl.carousel');

        $('#id_form-TOTAL_FORMS').val(form_idx + 1);
    });
    
    // 카드 삭제
    $(document).on("click", '.card-remove', function() {
        stopOwlPropagation('.owl-carousel');
        stopOwlPropagation('.owl-carousel-image');
        $('#photos-container').trigger('remove.owl.carousel', $(this).parents('.owl-item').index()).trigger('refresh.owl.carousel');
    });
    

    // 카드 수평 뷰
    $('.owl-carousel').owlCarousel({
        autoWidth: false,
        margin: 4,
        nav: true,
        dotsEach: true,
        mouseDrag: false,
        responsiveClass: true,
        responsive: {
            0: {
                items: 1
            },
            768: {
                items: 2
            },
            992: {
                items: 3
            }
        }
    });

    // 카드 내 이미지 수평뷰
    $('.owl-carousel-image').owlCarousel({ items: 1, lazyLoad: true, autoHeight: true, margin: 2 });

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