/* The scroll reveal for Gastronomy, September.

   The Culinary fusion row needs no script at all: it is a native scroll-snap
   track, so it swipes on touch, scrolls with a trackpad and takes arrow keys
   when focused on its own. The dots this file used to wire up are gone by
   request, and their code with them. */
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
       legal text, and its stylesheet narrows the <main> around it too. The
       stylesheet undoes both with :has(), and marks them here as well for
       browsers without :has(). See section 1 of the stylesheet. */
    var host = gs.closest && gs.closest('.content');
    if (host) host.classList.add('gs-host');
    var main = gs.closest && gs.closest('main');
    if (main) main.classList.add('gs-main');

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

  /* The countdown on the anniversary page.

     The date lives in the markup as data-until, in the hotel's own time, and
     the block stays hidden until real figures are in it, so nothing flashes 00
     on the way. Once the date has passed the block removes itself: the page
     spent a day showing "-1 days, -23 hours" after the eclipse, and a missing
     countdown reads better than a wrong one. */
  Array.prototype.forEach.call(document.querySelectorAll('[data-until]'), function (box) {
    var until = new Date(box.getAttribute('data-until').replace(' ', 'T') + '+01:00');
    if (isNaN(until)) { box.remove(); return; }

    var cells = {};
    ['days', 'hours', 'minutes', 'seconds'].forEach(function (unit) {
      cells[unit] = box.querySelector('[data-unit="' + unit + '"]');
    });

    function tick() {
      var left = until - new Date();
      if (left <= 0) { box.remove(); clearInterval(timer); return; }
      var s = Math.floor(left / 1000);
      var v = { days: Math.floor(s / 86400), hours: Math.floor(s / 3600) % 24,
                minutes: Math.floor(s / 60) % 60, seconds: s % 60 };
      Object.keys(cells).forEach(function (unit) {
        if (cells[unit]) {
          var n = String(v[unit]);
          cells[unit].textContent = n.length < 2 ? '0' + n : n;
        }
      });
      box.classList.add('is-running');
    }

    tick();
    var timer = setInterval(tick, 1000);
  });

})();
