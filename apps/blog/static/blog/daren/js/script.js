/* FIXED THD BOOK*/
$(function(){
	var sbOffLeft = $('#sidebar').offset().left+11;
	
	$(window).resize(function(){
		sbOffLeft = $('#sidebar').offset().left+11;
		if('fixed' != $('.book').css('position')){
			$('.book').css('left',sbOffLeft-$(window).scrollLeft());
		}
		if($(window).scrollTop()>385){
            $('.book').css('position', 'fixed');
            $('.book').css('top', 5);
			$('.book').css('left',sbOffLeft-$(window).scrollLeft());
		}
		})
	$(window).scroll(function(e){
        if($(window).scrollTop()>385){
            $('.book').css('position', 'fixed');
            $('.book').css('top', 5);
			$('.book').css('left',sbOffLeft-$(window).scrollLeft());
			
        } else {
            $('.book').css('position', '');
            $('.book').css('top', '');
			$('.book').css('left', '');
        }
		if(0 < $(window).scrollTop()){
	    	$('.top').fadeIn();
		}else{
	   		$('.top').fadeOut();
		}
		return false;
    });
	// scroll body to 0px on click
		$('.top').click(function () {
		$('body,html').animate({
			scrollTop: 0
		}, 800);
		return false;
	});
	})

/* archive scroll */
$(function(){
		$(".scroll").click(function(event){		
			event.preventDefault();
			$('html,body').animate({scrollTop:$(this.hash).offset().top}, 500);
		});
	});