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
            csrfmiddlewaretoken: `{{ csrf_token }}`
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
                <div class="image-item">
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
                    <div class="image-item">
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