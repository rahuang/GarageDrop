var main = function(){
	$('#wrapper').css('background-image', 'url(../static/img/garage_sale_login_open.gif)')
			setTimeout(function close(){
				$('#wrapper').addClass("garage_opened");
				$('#wrapper').css('background-image', 'url(../static/img/garage_sale_login_open.png)')
			}, 2000);
	setTimeout(function bounce(){
		$('.ball_bounce').css('background-image', 'url(../static/img/ball_bounce.gif)')
		$('#wrapper').css('background-image', 'url(../static/img/garage_sale_login_open2.png)')
		setTimeout(function bounce_stop(){
			$('.ball_bounce').css('background-image', 'url(../static/img/ball_bounce_stop.png)')
		}, 1000)
	}, 3000);
	$('.form-group').click(function(){
		if ($('#wrapper').hasClass("garage_closed")){
			$('#wrapper').css('background-image', 'url(../static/img/garage_sale_login_open.gif)')
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
