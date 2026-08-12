/* Culinary fusion carousel.

   The track is a native scroll-snap row, so it already swipes on touch, scrolls
   with a trackpad and takes arrow keys when focused - with or without this file.
   All this adds is the dots: click to move, and they follow the scroll. */
(function () {
  'use strict';

  document.querySelectorAll('[data-carousel]').forEach(function (root) {
    var track = root.querySelector('.gs-carousel__track');
    var slides = Array.prototype.slice.call(track.children);
    var dots = Array.prototype.slice.call(root.querySelectorAll('.gs-dot'));
    if (!track || dots.length !== slides.length) return;

    function setCurrent(i) {
      dots.forEach(function (d, n) {
        if (n === i) d.setAttribute('aria-current', 'true');
        else d.removeAttribute('aria-current');
      });
    }

    var still = window.matchMedia('(prefers-reduced-motion: reduce)');

    dots.forEach(function (dot, i) {
      dot.addEventListener('click', function () {
        // scroll the track itself rather than scrollIntoView, which would also
        // jump the page vertically
        track.scrollTo({
          left: slides[i].offsetLeft - slides[0].offsetLeft,
          behavior: still.matches ? 'auto' : 'smooth'
        });
        setCurrent(i);
      });
    });

    var frame;
    track.addEventListener('scroll', function () {
      cancelAnimationFrame(frame);
      frame = requestAnimationFrame(function () {
        var origin = track.scrollLeft + slides[0].offsetLeft;
        var nearest = 0;
        var best = Infinity;
        slides.forEach(function (s, i) {
          var d = Math.abs(s.offsetLeft - origin);
          if (d < best) { best = d; nearest = i; }
        });
        setCurrent(nearest);
      });
    }, { passive: true });
  });
})();
