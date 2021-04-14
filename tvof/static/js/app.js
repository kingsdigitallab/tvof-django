/* UI and Foundation stuff here */

$(function() {

  // Expand / Collapse

  $('.expander').bind("click", function() {
    $(this).next('.collapsible').slideToggle(400).removeClass("hide");
    $("i", this).toggleClass("fa-caret-down fa-caret-right");
    return false;
  });

  // Show more/less in long lists

  // Load the first 10 list items for each list
  $('.long-list').each(function() {
    // Count the list items
    var items = $(this).find('li').length;

    // If there are more than ten items, hide the rest
    if (items > 10) {
      $('li', this).eq(9).nextAll().hide().addClass('more-items');
    } else {
      $(this).next('.show-more').hide();
    }
  });

  $('.show-more').on('click', function(){
    var $this = $(this);
    var text = ($this.text() == 'Show less') ? 'Show more' : 'Show less';
    $this.text(text).toggleClass('secondary darker');
    $(this).prev('.long-list').children('li.more-items').slideToggle();
  });

    // Cookie consent
    // To be removed if switching to requirejs

    $(document).ready(function() {
        if (!window.Cookies.get('tvof-cookie')) {
            $("#cookie-disclaimer").removeClass('hide');
        }
        // Set cookie
        $('#cookie-disclaimer .closeme').on("click", function() {
            window.Cookies.set('tvof-cookie', 'tvof-cookie-set', { expires: 30 });
        });
    });

  // TVOF 131: click on PDF open the document in new tab instead of
  // downloading it
    $('a[href]').on('click', function() {
        var href = this.href;
        if (/.*\.pdf$/.test(href)) {
            window.open(href);
            return false;
        }
    });

    /*
    Returns the height $element should have to fill the remaining
    space in the viewport.
    If noscrollbar =  1, returns height so that the whole page is
    contained within the viewport. i.e. no scrollbar
    */
    function get_elastic_height($element, min, margin, noscrollbar) {
        var height = 0;

        // This is a hack for OL - we force 100% height when it is in
        // full screen mode. See zoom view of images on the faceted search.
        if ($element.find('.ol-full-screen-true').length > 0) {
            return '100%';
        }

        min = min || 0;
        margin = margin || 0;
        noscrollbar = noscrollbar || 0;

        var current_height = $element.outerHeight();
        if (noscrollbar) {
            // ! only works if body height is NOT 100% !
            height = $(window).outerHeight() - $('.text-viewer-wrapper').outerHeight() + current_height;
            height = (height <= min) ? min : height;
        } else {
            // Heights calculations:
            // viewport - bottom part (i.e. amrgin, e.g. footer)
            var window_height = $(window).height() - margin;
            // - top part (i.e. viewport space above the element)
            height = window_height - $element.offset().top + $(document).scrollTop();
            height = (height <= min) ? min : height;
            height = (height > window_height) ? window_height : height;
        }

        return Math.floor(height);
    }

    /*
        Make $target height elastic. It will take the rest of the
        viewport space. This is automatically updated when the user
        scrolls or change the viewport size.
        $callback is called each time the height is updated.
    */
    window.elastic_element = function($target, callback, min, margin) {
        var on_resize = function(e) {
            var height = get_elastic_height($target, min, margin);
            $target.css('height', height + 120);
            callback($target);
        };
        $(window).on('resize scroll', function(e) {on_resize(e);});
        $(document).on('webkitfullscreenchange mozfullscreenchange fullscreenchange MSFullscreenChange', function(e) {on_resize(e);});
        on_resize();
    };

});
