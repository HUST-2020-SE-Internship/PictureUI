document.getElementById("upload_pic").addEventListener("click", e => {
    hideWheel();
    document.getElementById("input_pic").click() ;
})

document.getElementById("upload_dir").addEventListener("click", e => {
    hideWheel();
    document.getElementById("input_dir").click() ;
})

var check_all_enable = false;
var edit_enable = true;

$("#btn-mov-dstfolder").click(function(){
    hideWheel();
    var dst_folder = $("#select-mov-dst").val();
    var root_type = $("#select-mov-dst option:selected").parent().attr('label');
    var sub_type = '';
    if(dst_folder.indexOf("(root)") < 0)
        sub_type = dst_folder;
    var old_root_type = $("#root-classified-type").html().toLowerCase();

    $(".image-item").each(function(){
        // svgs[0]对应pic-checked
        if ($(this).children("svg").first().css("display") == "block"){
            //请求删除
            $.ajax({
                url:'/main/account/moveImage',
                type:'POST',
                data:{
                    root_type: root_type,
                    sub_type: sub_type,
                    old_root_type: old_root_type,
                    img_url: $(this).children("img").first().attr("src").replace('\\', '/')
                },
                beforeSend: function(xhr, settings){
                    xhr.setRequestHeader("X-CSRFToken", $("input[name='csrfmiddlewaretoken']").val());
                },
                success: result => {
                    //判定是不是没移走...原地TP,如蜜传如蜜
                    if(!(root_type == old_root_type && sub_type == $(".classified-subType").html()))
                        $(this).remove();
                    updatePhotosNum();
                }
            });
        }
    })
    $("#moveImageModal").modal('hide');
})

$("#input_pic").change(e =>{
    var files = e.target.files;
    var re = new FileReader();
    re.readAsDataURL(files[0]);
    re.onload = function(re){
        console.log("read image success => " + getObjectURL(files[0])) ;
        var image = re.target.result ;
        document.getElementById("upload-msg").innerHTML = "正在读取图片"
        showImage(image) ;
    }
    check_all_enable = true;
    $("#check_all").removeAttr("disabled");
    edit_enable = false;
    $("#edit_saved").attr("disabled","disabled");
})

$("#input_dir").change(e =>{
    var files = e.target.files;
    var count = files.length ;
    var index = 1 ;
    for(var file of files){
        var re = new FileReader();
        re.readAsDataURL(file);
        re.onload = function(re){
            console.log("read image success => " + getObjectURL(file)) ;
            var image = re.target.result ;
            showImage(image) ;
            $("#upload-msg").html(`正在上传图片 ${index} / ${count}`);
            index++ ;
            if(index > count)
                $("#upload-msg").html(`上传完成`)
        }
    }
    check_all_enable = true;
    $("#check_all").removeAttr("disabled");
    edit_enable = false;
    $("#edit_saved").attr("disabled","disabled");
})

checked_svg = `<svg t="1600160114988" class="icon pic-checked" style="display:none" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="2025" width="200" height="200"><path d="M512 512m-512 0a512 512 0 1 0 1024 0 512 512 0 1 0-1024 0Z" fill="#1AAC19" p-id="2026"></path><path d="M809.691429 392.777143L732.16 314.514286 447.634286 599.771429 292.571429 443.977143 214.308571 521.508571l155.794286 155.794286 77.531429 77.531429 362.057143-362.057143z" fill="#FFFFFF" p-id="2027"></path></svg>`
unchecked_svg = `<svg t="1600159587297" class="icon pic-unchecked" style="display:block" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="1217" width="200" height="200"><path d="M512 512m-512 0a512 512 0 1 0 1024 0 512 512 0 1 0-1024 0Z" fill="#dbdbdb" p-id="1218"></path><path d="M809.691429 392.777143L732.16 314.514286 447.634286 599.771429 292.571429 443.977143 214.308571 521.508571l155.794286 155.794286 77.531429 77.531429 362.057143-362.057143z" fill="#FFFFFF" p-id="1219"></path></svg>`

function showImage(image){
    $(".not-sub-classified .image-container").prepend(
        `<div class="image-item" onclick="checkImage(this)">
                ${checked_svg}
                ${unchecked_svg}
            <img src=${image} alt="">
        </div>
        ` 
    );
}

function getObjectURL(file) {
    var url = null ;
    if (window.createObjectURL!=undefined) { // basic
        url = window.createObjectURL(file) ;
    } else if (window.URL!=undefined) { // mozilla(firefox)
        url = window.URL.createObjectURL(file) ;
    } else if (window.webkitURL!=undefined) { // webkit or chrome
        url = window.webkitURL.createObjectURL(file) ;
    }
    return url ;
}

$("#remove_checked").on("click", function(){
    hideWheel();
    $(".image-item").each(function(){
        // svgs[0]对应pic-checked
        if ($(this).children("svg").first().css("display") == "block"){
            //请求删除
            $.ajax({
                url:'/main/account/removeImage',
                type:'POST',
                async:false, //很重要,success回调函数会落后于函数体内其他函数再执行!
                data:{
                    typeName: $("#root-classified-type").html().toLowerCase(),
                    img_url: $(this).children("img").first().attr("src").replace('\\', '/')
                },
                beforeSend: function(xhr, settings){
                    xhr.setRequestHeader("X-CSRFToken", $("input[name='csrfmiddlewaretoken']").val());
                },
                success: result => {
                    $(this).remove();
                }
            });
        }
    })
    if($(".image-item").find("svg").length == 0){
        check_all_enable = false;
        $("#check_all").attr("disabled", "disabled");
        edit_enable = true;
        $("#edit_saved").removeAttr("disabled");
    }
    // 更新各子分类的图片数目
    updatePhotosNum();
    //最后检查是否有子分类被删空!!alert:不适配如今的逻辑,删空了也依然可以存在
    /*$("div[class$='sub-classified']").each(function(){
        if($(this).find('.image-item').length == 0)
            $(this).remove();
    })*/
})

$("#save_checked").on("click", function(){
    hideWheel();
    var typeName = $("#root-classified-type").html().toLowerCase();
    var isZero = true;
    $(".image-item").each(function(e){
        // svgs[0]对应pic-checked
        if ($(this).children("svg").first().css("display") == "block"){
            var image = $(this).children("img").first();
            image = image.attr("src");
            $.ajax({
                url: "/main/saveImage/",
                type: "POST",
                async: false,
                data: {
                    typeName: typeName,
                    image: JSON.stringify(image),
                },
                beforeSend: function(xhr, settings){
                    xhr.setRequestHeader("X-CSRFToken", $("input[name='csrfmiddlewaretoken']").val());
                },
                success: result => {
                    $(this).children("svg").remove();
                }
            })
        }
    })
    edit_enable = true;
    $("#edit_saved").removeAttr("disabled");
})

var isEdit = false;
$("#edit_saved").on("click", function(){
    hideWheel();
    if(edit_enable){
        isEdit = !isEdit;
        if (isEdit){
            $(".image-item").prepend(
                `
                ${checked_svg}
                ${unchecked_svg}
                `
            )
            check_all_enable = true;
            $("#check_all").removeAttr("disabled");
        }else{
            check_all_enable = false;
            $("#check_all").attr("disabled", "disabled");
            $(".image-item").children("svg").remove();
        }
        isEdit ? $(this).html("取消编辑"): $(this).html(`<i class="iconfont icon-bianji"></i>`);
    }
})

function checkImage(obj){
    var pic_checked = obj.querySelector(".pic-checked") ;
    var pic_unchecked = obj.querySelector(".pic-unchecked");
    if(pic_checked == undefined || pic_unchecked == undefined)
        return false;
    if(pic_checked.style.display == "none"){
        pic_checked.style.display = "block" ;
        pic_unchecked.style.display = "none";
    }else{
        pic_checked.style.display = "none" ;
        pic_unchecked.style.display = "block" ;
    }
}

var checkAll = false ;
$("#check_all").on("click", function(){
    hideWheel();
    if (check_all_enable){
        checkAll = !checkAll;
        $(".pic-checked").each(function(){
            checkAll ? $(this).css("display", "block"):$(this).css("display", "none");
        })
        $(".pic-unchecked").each(function(){
            checkAll ? $(this).css("display", "none"):$(this).css("display", "block");
        })
        checkAll ? $(this).children("i").first().attr('class','iconfont icon-quxiaoquanxuan') : $(this).children("i").first().attr('class','iconfont icon-quanxuan');
    }
})

function updatePhotosNum(){
    var totalNum = 0;
    $("div[class$='sub-classified']").each(function(){
        photosNum =  $(this).find(".image-item").length;
        totalNum += photosNum;
        if($(this).find("h1 small").length > 0)
            $(this).find("h1 small").html(`${photosNum} pcs`);
        else
            $(this).find("h1").append(`<small>${photosNum}`+` pcs</small>`);
    })
}

$(document).ready(updatePhotosNum);

$(".sub-classified h1 .classified-subType").dblclick(function(){
    $(this).html(`<input type='text' placeholder='`+ $(this).html() +`' class="change_sub_typename">`);
    $("input.change_sub_typename").focus();
})

//更改子分类的框失焦后使用ajax请求沟通
$("body").on('blur', 'input.change_sub_typename', function(){
    //先判空
    if($(this).val() == ""){
        $(this).parent('.classified-subType').html($(this).attr('placeholder'));
        updatePhotosNum();
        return false;
    }

    $.ajax({
        url:'/main/account/changeSubFolder',
        type:'POST',
        data:{
            typeName: $("#root-classified-type").html().toLowerCase(),
            old_name: $(this).attr("placeholder"),
            new_name: $(this).val()
        },
        beforeSend: function(xhr, settings){
            xhr.setRequestHeader("X-CSRFToken", $("input[name='csrfmiddlewaretoken']").val());
        },
        success: callback =>{
            if (callback.status == "1"){
                new_name = $(this).val();
                $(this).val(callback.msg);
                setTimeout(() => {
                    $(this).parent(".classified-subType").html(new_name);
                    //跳转至新分类, 截取后拼接再跳转
                    var url = window.location.href;
                    var patterns = url.split("/");
                    patterns[patterns.length - 1] = new_name;
                    window.location.href = patterns.join("/");
                }, 1000);
                
            }else{
                $(this).val(callback.msg);
                setTimeout(() => {
                    $(this).parent('.classified-subType').html($(this).attr('placeholder'));
                    updatePhotosNum();
                }, 1000);
            }
        }
    })
})

$('span.introduction').dblclick(function(){
    $(this).html(`<textarea placeholder='`+ $(this).text() +`' class="change_introduction" cols="10" rows="5"></textarea>`);
    $("textarea.change_introduction").focus();
})

$("span.introduction").on('blur', 'textarea.change_introduction', function(){
    //先判空
    if($(this).val() == ""){
        $(this).parent('.introduction').html($(this).attr('placeholder'));
        return false;
    }
    $.ajax({
        url:'/main/account/updateIntroduction',
        type:'POST',
        data:{
            typeName: $("#root-classified-type").html().toLowerCase(),
            subType: $(".classified-subType").html(),
            new_intro: $(this).val()
        },
        beforeSend: function(xhr, settings){
            xhr.setRequestHeader("X-CSRFToken", $("input[name='csrfmiddlewaretoken']").val());
        },
        success: callback =>{
            if (callback.status == "1"){
                $("span.introduction").html($(this).val());
            }else{
                $(this).val(callback.msg);
                setTimeout(() => {
                    $("span.introduction").html($(this).attr('placeholder'));
                }, 1000);
            }
        }
    })
})

$('#moveImageModal').on('show.bs.modal', function (e) {
    $("#select-mov-dst").selectpicker({"width":"100%"});
    $("#select-mov-dst").selectpicker('refresh');
    // 关键代码，如没将modal设置为 block，则$modala_dialog.height() 为零
    $(this).css('display', 'block');
    var modalHeight=$(window).height() / 2 - $('#moveImageModal .modal-dialog').height() / 2;
    $(this).find('.modal-dialog').css({
        'margin-top': modalHeight
    });
});