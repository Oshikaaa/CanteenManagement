
/* ===================================
    Loading Timeout
    ====================================== */

    $(window).on("load", function() {
      "use strict";
      setTimeout(function() {
          $('.preloader').fadeOut();
      }, 400);
  });


  /* ===================================
    Testimonials Slider
    ====================================== */

    $('.testimonials-slider').bxSlider({
      auto: true,
      controls: true,
      nextText: '',
      prevText: '',
      pause: 5000,
      speed: 500,
      pager: true,
      pagerCustom: '.testimonials-slider-pager-one, .testimonials-slider-pager-two, .testimonials-slider-pager-three'
  });

/* ===================================
    Our Item Slider
    ====================================== */
    $('.breakfast-slider').bxSlider({
       auto: false,
       controls: true,
       nextText: '<i class="fas fa-arrow-right"></i>',
       prevText: '<i class="fas fa-arrow-left"></i>',
       pause: 5000,
       speed: 500,
       slideMargin: 30,
       pager: true,
       pagerCustom: ''
   });
    $('.launch-slider').bxSlider({
       auto: false,
       controls: true,
       nextText: '<i class="fas fa-arrow-right"></i>',
       prevText: '<i class="fas fa-arrow-left"></i>',
       pause: 5000,
       speed: 500,
       slideMargin: 30,
       pager: true,
       pagerCustom: ''
   });

    $('.dinner-slider').bxSlider({
       auto: false,
       controls: true,
       nextText: '<i class="fas fa-arrow-right"></i>',
       prevText: '<i class="fas fa-arrow-left"></i>',
       pause: 5000,
       speed: 500,
       slideMargin: 30,
       pager: true,
       pagerCustom: ''
   });
    $('.dessert-slider').bxSlider({
      auto: false,
      controls: true,
      nextText: '<i class="fas fa-arrow-right"></i>',
      prevText: '<i class="fas fa-arrow-left"></i>',
      pause: 5000,
      speed: 500,
      slideMargin: 30,
      pager: true,
      pagerCustom: ''
  });
    $('.shake-slider').bxSlider({
      auto: false,
      controls: true,
      nextText: '<i class="fas fa-arrow-right"></i>',
      prevText: '<i class="fas fa-arrow-left"></i>',
      pause: 5000,
      speed: 500,
      slideMargin: 30,
      pager: true,
      pagerCustom: ''
  });

  /* ===================================
   Chef Slider
   ====================================== */
   $('.chef-slider').bxSlider({
      auto: true,
      controls: true,
      nextText: '<i class="fas fa-arrow-right"></i>',
      prevText: '<i class="fas fa-arrow-left"></i>',
      pause: 5000,
      speed: 500,
      slideMargin: 30,
      pager: true,
      pagerCustom: '.chef-slider'
  });

/*  ===================================
   sticky header
   ====================================== */
   window.onscroll = function() {
      myFunction();
  };
  var header = document.getElementById("myHeader");
  var sticky = header.offsetTop;

  function myFunction() {
      if (window.pageYOffset > sticky) {
        header.classList.add("sticky");
    } else {
        header.classList.remove("sticky");
    }
}



/*  ===================================
   scroll active class menu
   ====================================== */
   $('body').scrollspy({
      target: '#myHeader'
  });

  // scroll bottom to top button
  $(document).ready(function() {
      $(window).scroll(function() {
          if ($(this).scrollTop() > 100) {
              $('.scroll-top').fadeIn();
          } else {
              $('.scroll-top').fadeOut();
          }
      });
      $('.scroll-top').click(function() {
          $("html, body").animate({
              scrollTop: 0
          }, 100);
          return false;
      });
  });


  /*  ===================================
      search toggle
      ====================================== */
      $(document).ready(function() {

          $('.nav-link').on( "click", function() {
              $('.navbar-toggler').addClass('collapsed');
              $('.tr-nabar-collapse').removeClass('show');
              $('.fullscreen-menu-list').removeClass('show');
          });

          $(' .fa-search').on( "click", function() {
              $('.header-search .header-input').css("display","inline-block");
              $('.close-icon').css("display","inline-block");
              $('.search-icon').css("display","none");
          });

          $( ".close-icon" ).on( "click", function() {
              $('.header-search .header-input').css("display","none");
              $('.close-icon').css("display","none");
              $('.search-icon').css("display","inline-block");
          });


      });

  /*  ===================================
      iframe video script
      ====================================== */
      var tag = document.createElement('script');

      tag.src = "https://www.youtube.com/iframe_api";
      var firstScriptTag = document.getElementsByTagName('script')[0];
      firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

      var player;
      function onYouTubeIframeAPIReady() {
          player = new YT.Player('player', {
            videoId: 'F3zw1Gvn4Mk',
            playerVars: { 'autoplay': 1, 'playsinline': 1, 'loop': 1, 'playlist': 'F3zw1Gvn4Mk', 'controls': 0, 'fs': 1 },
            events: {
              'onReady': onPlayerReady
          }
      });
      }

      function onPlayerReady(event) {
         event.target.mute();
         event.target.playVideo();
     }
