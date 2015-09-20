var main = function(){
	$('#wrapper').addClass("garage_closed");
	$('.form-group').click(function(){
		if ($('#wrapper').hasClass("garage_closed")){
			$('#wrapper').css('background-image', 'url(../static/img/garage_sale_login.gif)')
			$('#wrapper').removeClass("garage_closed");
			setTimeout(function close(){
				$('#wrapper').addClass("garage_opened");
				$('#wrapper').css('background-image', 'url(../static/img/garage_sale_login_open.png)')
			}, 2000);
		}
		else if ($('#wrapper').hasClass("garage_opened")){
			$('#wrapper').css('background-image', 'url(../static/img/garage_sale_login_close.gif)')
			$('#wrapper').removeClass("garage_opened");
			setTimeout(function close(){
				$('#wrapper').addClass("garage_closed");
				$('#wrapper').css('background-image', 'url(../static/img/garage_sale_login.png)')
			}, 2000);
		}
	});
};

$(document).ready(main);
