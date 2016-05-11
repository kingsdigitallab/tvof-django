/* UI and Foundation stuff here */

$(document).ready(function() {

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
		$this = $(this);
		var text = ($this.text() == 'Show less') ? 'Show more' : 'Show less';
		$this.text(text).toggleClass('secondary darker'); 
		$(this).prev('.long-list').children('li.more-items').slideToggle();
	});
});