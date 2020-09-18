document.getElementById("upload_pic").addEventListener("click", e => {
    document.getElementById("input_pic").click() ;
})

document.getElementById("upload_dir").addEventListener("click", e => {
    document.getElementById("input_dir").click() ;
})

var check_all_enable = false;
var edit_enable = true;

$("#new_subfolder").click(function(){
    $("#input_subfolder").focus();
})

$("#btn-new-subfolder").click(function(){
    alert("我真的点击1了")
    if($("#input_subfolder").val() == ""){
        $("#input_subfolder").attr("placeholder", "请输入子分类的名称!");
        return false;
    }
    $.ajax({
        url:'/main/account/createSubFolder',
        type:'post',
        data:{
            typeName: $("#root-classified-type").html().toLowerCase(),
            subFolder: $("#input_subfolder").val()
        },
        beforeSend: function(xhr, settings){
            xhr.setRequestHeader("X-CSRFToken", $("input[name='csrfmiddlewaretoken']").val());
        },
        success: callback => {
            $("#input_subfolder").val(callback.msg);
            setTimeout(function(){
                $("#newFolderModal").modal('hide');
            }, 1000);
        }
    })
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
    $(".image-item").each(function(){
        // svgs[0]对应pic-checked
        if ($(this).children("svg").first().css("display") == "block")
            $(this).remove();
    })
    if($(".image-item").find("svg").length == 0){
        check_all_enable = false;
        $("#check_all").attr("disabled", "disabled");
        edit_enable = true;
        $("#edit_saved").removeAttr("disabled");
    }
    // TODO: 删除存在云端的图片需要确认?
})

$("#save_checked").on("click", function(){
    var typeName = $(".classified-title").html();
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
        isEdit ? $(this).html("取消编辑"): $(this).html("编辑模式");
    }
})

function checkImage(obj){
    var pic_checked = obj.querySelector(".pic-checked") ;
    var pic_unchecked = obj.querySelector(".pic-unchecked");
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
    if (check_all_enable){
        checkAll = !checkAll;
        $(".pic-checked").each(function(){
            checkAll ? $(this).css("display", "block"):$(this).css("display", "none");
        })
        $(".pic-unchecked").each(function(){
            checkAll ? $(this).css("display", "none"):$(this).css("display", "block");
        })
        checkAll ? $(this).html("取消全选") : $(this).html("选中所有");
    }
})
