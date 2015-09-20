var main = function(){
	$('#house').attr('src', '../static/img/garage_sale_login_open.gif?' + Math.random());
	$('.moto').fadeOut();
	setTimeout(function open(){
		$('#house').attr('src', '../static/img/garage_sale_login_open.png');
		/*$('#ball').attr("src", "../static/img/ball_bounce.gif?" + Math.random());*/
		/*setTimeout(function bounce_stop(){
			$('#ball').attr("src", "../static/img/ball_bounce_stop.png");
		}, 1000);*/
	}, 900);

	$('.login_btn').click(function(){
		$('#house').attr('src', '../static/img/garage_sale_login_close.gif?' + Math.random());
		setTimeout(function login(){
			$('#house').attr('src', '../static/img/garage_sale_login.png');
			$('#wrapper').animate({'top' : '650px'}, {duration : 650});
			$('#clouds').animate({'top' : '0px'}, {duration : 650});
			$('.pin').animate({'top' : '20px'}, {duration : 1000});
			$('.moto').animate({'top' : '20px'}, {duration : 1000});
		}, 1000);
	});

	$('#pin').hover(function(){
		if($(this).hasClass("turned")){}
		else{
			$(this).addClass("turned");
			setTimeout(function turn(){
				$('#pin').attr('src', '../static/img/Pin.gif?' + Math.random());
				$('.moto').fadeIn(500);
			}, 1000);
		}
	});

	$('.moto').click(function(){
		
		$('#wrapper').animate({'top' : '0px'}, {duration : 1000});
		$('#clouds').animate({'top' : '-800px'}, {duration : 1000});
		$('.pin').animate({'top' : '-1500px'}, {duration : 650});
		$('.moto').animate({'top' : '-1500px'}, {duration : 650});
		setTimeout(function login(){
			$('#house').attr('src', '../static/img/garage_sale_login_open.gif?' + Math.random());
		}, 1000);
		setTimeout(function open2(){
				$('#house').attr('src', '../static/img/garage_sale_login_open.png');
				$('#pin').removeClass("turned");
				$('#pin').attr('src', '../static/img/Pin.png');
				$('.moto').fadeOut;
		}, 2000);
	});

}

$(document).ready(main);
