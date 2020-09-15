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
    var count = files.length ;
    var index = 1 ;
    for(var file of files){
        var re = new FileReader();
        re.readAsDataURL(file);
        re.onload = function(re){
            console.log("read image success => " + getObjectURL(file)) ;
            var image = re.target.result ;
            classifyImage(image) ;
            document.getElementById("upload-msg")
                .innerHTML = `正在上传图片 ${index} / ${count}` ;
            index++ ;
            if(index > count){
                document.getElementById("upload-msg").innerHTML = `上传完成` ;
            }
        }
    }
})

function classifyImage(image){
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
            console.log("receive: " + typeName) ;	
            showLabelInFront(image, typeName) ;
        }
    })
}

function showLabelInFront(image, typeName){
    var main_container = document.getElementById("main-container") ;
    var classifies = document.querySelectorAll(".classify") ;

    var isClassify = false ;

    for(var classify of classifies){
        var classifyTitle = classify.querySelector(".classify-title").innerHTML ;

        if(typeName == classifyTitle){
            classify.querySelector(".image-container").innerHTML += `
                <div class="image-item" onclick="checkImage(this)">
                    <img class="pic-checked" src="/static/img/checked.png" style="display: none;">
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
                <div class="image-container">
                    <div class="image-item" onclick="checkImage(this)">
                        <img class="pic-checked" src="/static/img/checked.png" style="display: none;">
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
            var images = imageItem.querySelectorAll("img") ;
            if(images[0].style.display == "block"){
                isZero = false ;
                image = images[1].getAttribute("src") ;
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

function checkImage(obj){
    var pic_checked = obj.querySelector(".pic-checked") ;
    if(pic_checked.style.display == "none"){
        pic_checked.style.display = "block" ;
    }else{
        pic_checked.style.display = "none" ;
    }
}

var checkAll = false ;
document.getElementById("check_all").addEventListener("click", e => {
    var pic_checked = document.querySelectorAll(".pic-checked") ;
    checkAll = !checkAll ;
    for(var checked of pic_checked){
        if(checkAll){
            checked.style.display = "block" ;
        }else{
            checked.style.display = "none" ;
        }
    }
    if(checkAll){
        document.getElementById("check_all").innerHTML = "取消全选" ;
    }else{
        document.getElementById("check_all").innerHTML = "选中所有" ;
    }
})