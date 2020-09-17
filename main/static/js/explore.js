document.getElementById("upload_pic").addEventListener("click", e => {
    document.getElementById("input_pic").click() ;
})

document.getElementById("upload_dir").addEventListener("click", e => {
    document.getElementById("input_dir").click() ;
})

document.getElementById("input_pic").addEventListener("change", e => {
    var files = e.target.files;
    var re = new FileReader();
    re.readAsDataURL(files[0]);
    re.onload = function(re){
        console.log("read image success => " + getObjectURL(files[0])) ;
        var image = re.target.result ;
        document.getElementById("upload-msg").innerHTML = "正在上传图片"
        classifyImage(image) ;
    }
})

document.getElementById("input_dir").addEventListener("change", e => {
    var files = e.target.files;
    console.log(files);
    console.log(typeof files);
    var count = files.length ;
    var index = 1 ;
    for(var file of files){
        var re = new FileReader();
        re.readAsDataURL(file);
        re.onload = function(re){
            // console.log("read image success => " + getObjectURL(file)) ;
            var image = re.target.result ;
            // classifyImage(image) ;
            (function(i) {
                setTimeout(function() {
                    classifyImage(image, i, count) ;
                }, i * 550);
            })(index)
            // document.getElementById("upload-msg")
            //     .innerHTML = `正在上传图片 ${index} / ${count}` ;
            index++ ;
            // if(index > count){
            //     document.getElementById("upload-msg").innerHTML = `上传完成` ;
            // }
        }
    }
})

function classifyImage(image, index=1, count=1){
    console.log("发送图片时间：" + new Date())
    document.getElementById("upload-msg")
                .innerHTML = `正在上传图片 ${index} / ${count}` ;
    $.ajax({
        url: "/main/classify/",
        type: "POST",
        data: {
            image: JSON.stringify(image),
            // csrfmiddlewaretoken: `{{ csrf_token }}`
        },
        beforeSend: function(xhr, settings){
            xhr.setRequestHeader("X-CSRFToken", $("input[name='csrfmiddlewaretoken']").val());
        },
        success: result => {
            typeName = JSON.parse(result) ;
            // console.log("receive: " + typeName) ;
            showLabelInFront(image, typeName) ;
        }
    })
}

checked_svg = `<svg t="1600160114988" class="icon pic-checked" style="display:none" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="2025" width="200" height="200"><path d="M512 512m-512 0a512 512 0 1 0 1024 0 512 512 0 1 0-1024 0Z" fill="#1AAC19" p-id="2026"></path><path d="M809.691429 392.777143L732.16 314.514286 447.634286 599.771429 292.571429 443.977143 214.308571 521.508571l155.794286 155.794286 77.531429 77.531429 362.057143-362.057143z" fill="#FFFFFF" p-id="2027"></path></svg>`
unchecked_svg = `<svg t="1600159587297" class="icon pic-unchecked" style="display:block" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="1217" width="200" height="200"><path d="M512 512m-512 0a512 512 0 1 0 1024 0 512 512 0 1 0-1024 0Z" fill="#dbdbdb" p-id="1218"></path><path d="M809.691429 392.777143L732.16 314.514286 447.634286 599.771429 292.571429 443.977143 214.308571 521.508571l155.794286 155.794286 77.531429 77.531429 362.057143-362.057143z" fill="#FFFFFF" p-id="1219"></path></svg>`

function showLabelInFront(image, typeName){
    var main_container = document.getElementById("main-container") ;
    var classifies = document.querySelectorAll(".classify") ;

    var isClassify = false ;

    for(var classify of classifies){
        var classifyTitle = classify.querySelector(".classify-title").innerHTML ;

        if(typeName == classifyTitle){
            classify.querySelector(".image-container").innerHTML += `
                <div class="image-item" onclick="checkImage(this)">
                    ${checked_svg}
                    ${unchecked_svg}
                    <img src=${image} alt="">
                </div>
            ` ;
            isClassify = true ;
            break ;
        }
    }

    if(!isClassify){
        main_container.innerHTML += `
            <div class="classify">
                <h1 class="classify-title">${typeName}</h1>
                <div class="clear"></div>
                <div class="image-container">
                    <div class="image-item" onclick="checkImage(this)">
                        ${checked_svg}
                        ${unchecked_svg}
                        <img src="${image}" alt="">
                    </div>
                </div>
            </div>
        ` ;
    }
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

// 给待选中的图片增加勾选
document.getElementById("save_checked").addEventListener("click", e => {
    var isZero = true ;
    var classifies = document.querySelectorAll(".classify") ;
    for(var classify of classifies){
        var typeName = classify.querySelector(".classify-title").innerHTML ;
        var imageItems = classify.querySelectorAll(".image-item") ;
        for(var imageItem of imageItems){
            var image = imageItem.querySelector("img") ;
            var svgs = imageItem.querySelectorAll("svg") ;
            // svgs 为界定是否选中的两个字体图标, svg[0]对应pic-checked
            if(svgs[0].style.display == "block"){
                isZero = false ;
                image = image.getAttribute("src") ;
                // console.log(typeName, images[1].getAttribute("src")) ;

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
                        // typeName = JSON.parse(result) ;
                        // console.log("receive: " + typeName) ;
                        // showLabelInFront(image, typeName) ;
                    }
                })
            }
        }
    }
    if(isZero){
        alert("选中数量图片为0") ;
    }
})

$("#remove_checked").on("click", function(){
    $(".classify").each(function(){
        $(this).find(".image-item").each(function(){
            if ($(this).children("svg").first().css("display") == "block")
                $(this).remove();
        })
        //注意this对应的作用域 .classify->.image-container->.image-item, 所以children方法只会找childNode的第一层子元素,find方法会进入每个childNode嵌套寻找
        if ($(this).find(".image-item").length == 0)
            $(this).remove();
    })
    /*
    var classifies = document.querySelectorAll(".classify") ;
    for(var classify of classifies){
        var imageItems = classify.querySelectorAll(".image-item") ;
        for(var imageItem of imageItems){
            var svgs = imageItem.querySelectorAll("svg");
            if(svgs[0].style.display == "block"){
                imageItem.remove();
            }
        }
        // 删除后如果该分类下为空, 移除该分类
        if(classify.querySelectorAll(".image-item").length == 0)
            classify.remove();
    }
    */
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
document.getElementById("check_all").addEventListener("click", e => {
    var pic_checked = document.querySelectorAll(".pic-checked");
    var pic_unchecked = document.querySelectorAll(".pic-unchecked");
    checkAll = !checkAll ;
    for(var checked of pic_checked){
        if(checkAll){
            checked.style.display = "block" ;
        }else{
            checked.style.display = "none" ;
        }
    }
    for(var unchecked of pic_unchecked){
        if(checkAll){
            unchecked.style.display = "none" ;
        }else{
            unchecked.style.display = "block" ;
        }
    }
    if(checkAll){
        document.getElementById("check_all").innerHTML = "取消全选" ;
    }else{
        document.getElementById("check_all").innerHTML = "选中所有" ;
    }
})