$("#create_dir").click(function(){
    $("#input_new_dir").animate({right:"100", opacity:1}, 500, function(){
        $(this).css({display:"block"});
        $(this).focus();
    })
})

$("#input_new_dir").blur(function(){
    $(this).animate({left:"100", opacity:0}, 500, function(){
        $(this).css({display:"none"});
    })
})