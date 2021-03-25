$(function() {

  'use strict';

  $('.js-menu-toggle').click(function(e) {

  	var $this = $(this);

  	

  	if ( $('body').hasClass('show-sidebar') ) {
  		$('body').removeClass('show-sidebar');
  		$this.removeClass('active');
  	} else {
  		$('body').addClass('show-sidebar');	
  		$this.addClass('active');
  	}

  	e.preventDefault();

  });

  // click outisde offcanvas
	$(document).mouseup(function(e) {
    var container = $(".sidebar");
    if (!container.is(e.target) && container.has(e.target).length === 0) {
      if ( $('body').hasClass('show-sidebar') ) {
			$('body').removeClass('show-sidebar');
			$('body').find('.js-menu-toggle').removeClass('active');
		}
    }
	}); 

    // function rendertime() {
	// 	$.ajax({
	// 		url: '/showtime',
	// 		method: 'get',
	// 		success:function(data) {
	// 			$("#time").text(data);
	// 			// console.log("time: "+data);
	// 		}
	// 	})
	// }
	

    $('.toastrDefaultSuccess').click(function() {
		toastr.success('Lorem ipsum dolor sit amet, consetetur sadipscing elitr.')
	});
	$('.toastrDefaultInfo').click(function() {
		toastr.info('Lorem ipsum dolor sit amet, consetetur sadipscing elitr.')
	});
	$('.toastrDefaultError').click(function() {
		toastr.error('Lorem ipsum dolor sit amet, consetetur sadipscing elitr.')
	});
	$('.toastrDefaultWarning').click(function() {
		toastr.warning('Lorem ipsum dolor sit amet, consetetur sadipscing elitr.')
	});

	function makeToast(type, message) {
		if (type == 'success') {			
			toastr.success(message);
		}
		else if (type == 'failed') {			
			toastr.warning(message);
		}
		else if (type == 'missing data') {
			toastr.warning(message);
		}
		else if (type == 'error') {
			toastr.error(message);
		}
		else {
			toastr.info(message);
		}
	}

	// $(".back").on("click", function(){
	// 	window.history.back();
	// })

	$(document).on('click', '.back', function(){
		window.history.back();
	})
});