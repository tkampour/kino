$(document).ready(function(){
  
  $(".kino-home").click(function(e){
      $("a.active").removeClass("active");
      $(this).addClass("active");
      $(".sub").removeClass("active");
  });
  $(".kino-stats").click(function(e){
    e.preventDefault();
	$("#kino-main").empty().html("TEST");
	$(".art-postheadericon").empty().html("ΣΤΑΤΙΣΤΙΚΑ");
	$("a.active").removeClass("active");
	$(this).addClass("active");
	$(this).next().addClass("active");
  });
  $(".kino-top").click(function(e){
      e.preventDefault();
      $("#kino-main").empty().html("Under Construction");
      $(".art-postheadericon").empty().html("ΣΤΑΤΙΣΤΙΚΑ");
      $("a.active").removeClass("active");
      $(this).addClass("active");
  });
  $(".kino-delay").click(function(e){
      e.preventDefault();
      $("#kino-main").empty().html("Under Construction");
      $("a.active").removeClass("active");
      $(this).addClass("active");
  });
  $(".kino-full").click(function(e){
      $("a.active").removeClass("active");
      $(this).addClass("active");
  });

  $(".kino-fill").click(function(e){
	$(".art-postheadericon").empty().html("ΣΥΜΠΛΗΡΩΣΗ ΔΕΛΤΙΟΥ");
	$("a.active").removeClass("active");
	$(this).addClass("active");
//	$(".sub").removeClass("active");
  });

  $(".kino-check").click(function(e){

      $("a.active").removeClass("active");
      $(this).addClass("active");
      $(".sub").removeClass("active");
  });

  $(".kino-rules").click(function(e){
//    e.preventDefault();
	$(".art-postheadericon").empty().html("ΚΑΝΟΝΕΣ");

//        $.ajax({url:"rules.html",dataType:"html",success:function(result){ 	
//		
//	    $("#kino-main").html(result); 			
//	    $("#tabs ul li a").removeClass(); 			
//	    $("#tabs").tabs(); 			
//	    $('li').css('overflow-x', 'hidden'); 			
//	    $(".ui-widget ul *").css("font-size", "10px"); 			
//	    }, 			
//	    error: function(xhr,z,thrownError){ 			
//		alert(xhr.status); 			
//		alert(thrownError); 			
//		alert(xhr.responseText); 			
//	    } 			
//	}); 
	$("a.active").removeClass("active");
	$(this).addClass("active");
	$(".sub").removeClass("active");
  });
}); 
