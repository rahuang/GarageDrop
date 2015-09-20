var main = function(){
	$('#wrapper').css('background-image', 'url(../static/img/garage_sale_login_open.gif)');
	setTimeout(function open(){
		$('#wrapper').addClass("garage_opened");
		$('#wrapper').css('background-image', 'url(../static/img/garage_sale_login_open.png)');
		/*$('#ball').attr("src", "../static/img/ball_bounce.gif?" + Math.random());*/
		/*setTimeout(function bounce_stop(){
			$('#ball').attr("src", "../static/img/ball_bounce_stop.png");
		}, 1000);*/
	}, 1000);

	$('.login_btn').click(function(){
		$('#wrapper').css('background-image', 'url(../static/img/garage_sale_login_close.gif)');
		setTimeout(function login(){
			$('#wrapper').css('background-image', 'url(../static/img/garage_sale_login.png)');
			$('#wrapper').animate({'top' : '650px'}, {duration : 650});
			$('#clouds').animate({'top' : '0px'}, {duration : 650});
			$('.pin').animate({'top' : '50px'}, {duration : 1000});
		}, 1000);
	});

}

$(document).ready(main);
