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


// headbar
$(function(){
	
	var path_name = location.pathname.replace(new RegExp("/","gm"), "");
	$(".header .nav li.active").removeClass("active");	
	switch (path_name){
	case "about":
		$("#nav-about").addClass("active");
		break;
	case "guestbook":
		$("#nav-guestbook").addClass("active");
		break;
	default:
		$("#nav-home").addClass("active");
	};
	
	$(".search-wrap").click(function(a){
		return !1
	}).click(function(b){
		var c = $(b.currentTarget).closest(".search-wrap"),
        d = $(document),
        e = $("#form-search");		
		if (c.hasClass("active")) return;		
		c.addClass("active").find("#txt-search").focus(),
		d.one("click.search", function(a) {
		        c.removeClass("active").find("#txt-search").val(""), d.unbind("keyup.search")
			}).bind("keyup.search", function(a) {
                a.keyCode == 27 && (a.preventDefault(), d.trigger("click.search"))
            }), !1
	});
});