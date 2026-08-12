/* Culinary fusion carousel, and the scroll reveal.

   The track is a native scroll-snap row, so it already swipes on touch, scrolls
   with a trackpad and takes arrow keys when focused - with or without this file.
   All this adds is the dots: click to move, and they follow the scroll. */
(function () {
  'use strict';

  /* The reveal.

     The theme hides [data-anim=fade] above 1200px and its anim.js adds
     .animated once the element scrolls into view. Pasted into a page as a
     block, this markup cannot count on that script reaching it, and the
     failure is not cosmetic: every section here carries the attribute, so a
     miss leaves the page blank. This does the same job for .gs, using the
     theme's own class so the theme's transitions still do the animating. If
     anim.js does run as well, it sets a class that is already set.

     The gs-js class below is the other half. The stylesheet keeps everything
     visible until it appears, so a page that never runs this file is merely
     unanimated rather than empty.

     Deliberately a scroll handler and a bounding box rather than an
     IntersectionObserver. The observer is the tidier tool, but it only
     delivers while the page is compositing, and anything that stops it
     delivering here does not leave the page unanimated, it leaves it empty. A
     handful of getBoundingClientRect calls on five elements is not a cost
     worth that risk. */
  Array.prototype.forEach.call(document.querySelectorAll('.gs'), function (gs) {

    /* The borrowed template wraps the content in a narrow column meant for
       legal text. The stylesheet undoes it with :has(), and marks it here as
       well for browsers without :has(). See section 1 of the stylesheet. */
    var host = gs.parentNode;
    if (host && host.classList && host.classList.contains('content')) {
      host.classList.add('gs-host');
    }

    var targets = Array.prototype.slice.call(gs.querySelectorAll('[data-anim]'));

    function reveal() {
      var edge = window.innerHeight * 0.9;
      targets = targets.filter(function (el) {
        if (el.getBoundingClientRect().top > edge) return true;
        el.classList.add('animated');
        return false;
      });
      if (!targets.length) {
        window.removeEventListener('scroll', onScroll);
        window.removeEventListener('resize', reveal);
      }
    }

    var frame;
    function onScroll() {
      cancelAnimationFrame(frame);
      frame = requestAnimationFrame(reveal);
    }

    // Hand over from the stylesheet only once the reveal is wired up, so there
    // is no instant in which nothing is keeping the content visible.
    gs.classList.add('gs-js');
    reveal();

    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', reveal);

    // Last resort. If a section is still hidden well after load, something
    // upstream is wrong and a still page beats an empty one.
    setTimeout(function () {
      targets.forEach(function (el) { el.classList.add('animated'); });
    }, 3000);
  });

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
