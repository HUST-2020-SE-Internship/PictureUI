$(function(){
    $("#selectImg").change(function(){
        $("#profile").attr("src",URL.createObjectURL($(this)[0].files[0]));
    });

    $("#btn_upload").click(function(){
        $.ajax({
            
        })
    })
})