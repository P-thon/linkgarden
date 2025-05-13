try {
    var swiper2 = new Swiper(".slide-content2", {
        slidesPerView: 1,
        spaceBetween: 25,
        loop: true,
        centerSlide: 'true',
        fade: 'true',
        grabCursor: 'true',
        pagination: {
            el: ".pagination_addswiper",
            clickable: true,
            dynamicBullets: true,
        },
        navigation: {
            nextEl: ".next_addswiper",
            prevEl: ".prev_addswiper",
        },
        autoplay: {
            delay:5000,
            disableOnInteraction: false,
        },
    });
} catch {console.warn("SDEV - Can't load advantages swiper.")}