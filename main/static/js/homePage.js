"use strict";
var menuDisabled = false;
jQuery(document).ready(function($){

    /************** Menu Content Opening *********************/
    /*
	$(".main_menu a").on('click',function(){
		var id =  $(this).attr('class');
		id = id.split('-');
		//$("#menu-container .content").hide();
		//$("#menu-container #menu-"+id[1]).show();
		//$("#menu-container .homepage").hide();
		return false;
	});
	*/
	$(".main_menu a.about-backhome").click(function(){
		$('#menu-container .about').fadeOut(1000, function(){
        $('#menu-container .homepage').fadeIn(1000);
	    });
		return false;
	});

	$(".main_menu a.subpage-about").click(function(){    
    $('#menu-container .homepage').fadeOut(1000, function(){
        $('#menu-container .about').fadeIn(1000);
	    });
		return false;
	});
	
	$(".main_menu a.contact-backhome").click(function(){
		$('#menu-container .contact').fadeOut(1000, function(){
        $('#menu-container .homepage').fadeIn(1000);
	    });
		return false;
	});
	
	$(".main_menu a.random_photo_page").click(function(){    
    $('#menu-container .homepage').fadeOut(1000, function(){
        $('#menu-container .contact').fadeIn(1000);
		loadRandomPhoto();		
	    });
	});
	
	
	/************** Gallery Hover Effect *********************/
	$(".overlay").hide();

	$('.gallery-item').hover(
	  function() {
	    $(this).find('.overlay').addClass('animated fadeIn').show();
	  },
	  function() {
	    $(this).find('.overlay').removeClass('animated fadeIn').hide();
	  }
	);


	/************** LightBox *********************/
	$(function(){
		$('[data-rel="lightbox"]').lightbox();
	});


	$("a.menu-toggle-btn").click(function() {
	  $(".responsive_menu").stop(true,true).slideToggle();
	  return false;
	});
 
    $(".responsive_menu a").click(function(){
		$('.responsive_menu').hide();
	});

});

function loadScript() {
  var script = document.createElement('script');
  script.type = 'text/javascript';
  script.src = 'https://maps.googleapis.com/maps/api/js?v=3.exp&sensor=false&' +
      'callback=initialize';
  document.body.appendChild(script);
}

function initialize() {
    var mapOptions = {
      zoom: 12,
      center: new google.maps.LatLng(40.7823234,-73.9654161)
    };
    var map = new google.maps.Map(document.getElementById('templatemo_map'),  mapOptions);
}

function loadRandomPhoto(){
	$.ajax({
		url:'/main/test/getRandomPhoto',
		type:'post',
		beforeSend: function(xhr, settings){
			xhr.setRequestHeader("X-CSRFToken", $("input[name='csrfmiddlewaretoken']").val());
		},
		success: callback => {
			$.each(callback.photoDict, function(classname, photourl){

				var html = `<div class="scene">
							<div class="card">
								<div class="image-item card__face card__face--front">
									<a href="/main/account/${callback.user_id}/classified/${classname}">
									<img src="${photourl}" alt="">
									</a>
								</div>
								<div class="image-item card__face card__face--back">
									<a href="/main/account/${callback.user_id}/classified/${classname}">
										<div class="post-card">
											<img class="post-background" src="${photourl}">
											<div class="post-card-mask--special">
												<div class="post-card-container">
													<h2 class="post-card-title" itemprop="headline">${classname}</h2>
													<div class="post-card-info">
														<span>AutoAlbum v0.1</span>
													</div>
												</div>
											</div>
										</div>
									</a>
								</div>
							</div>
							</div>`
				$(".contact-container").html(html);
			})
		}
	})
}