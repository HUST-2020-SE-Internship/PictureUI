$(document).ready(function(){
    $("#selectImg").change(function(){
        if($(this)[0].files[0] != null){
            $("#profile").attr("src",URL.createObjectURL($(this)[0].files[0]));
        }
    });
    /*
    $("#selectAjaxImg").change(function(){
        if($(this)[0].files[0] != null){
            $("#ajax_profile").attr("src",URL.createObjectURL($(this)[0].files[0]));
        }
    });
    */
    $("#selectAjaxImg").on("change", function(){
        if($(this)[0].files[0] == null)
            return

        $("#ajax_profile").attr("src", URL.createObjectURL($(this)[0].files[0]));

        var files = $(this)[0].files;
        var re = new FileReader();
        re.readAsDataURL(files[0]); //reader读取完毕后会自动转换为base64编码的字符串
        re.onload = function(re){
            console.log("read image success => " + getObjectURL(files[0])) ;
            var image = re.target.result ;
            $("#upload-msg").html("正在上传图片");
            classifyImage(image) ;
        }
    })

    function classifyImage(image){
        $.ajax({
            url:"",
            type:"POST",
            data: {
                image: JSON.stringify(image)
            },
            // 注意:由于表单数据(formdata)采用了CSRF中间件验证, 使用ajax的话需要手动设置X-CSRFToken
            // 可以在后端DEBUG时查看整个request对象的值
            beforeSend: function(xhr, settings){
                xhr.setRequestHeader("X-CSRFToken", $("input[name='csrfmiddlewaretoken']").val());
            },
            error: function(data){
                alert("上传失败")
            },
            success:function(data){
                // console.log(data);
                // 不采用src形式的话 直接使用base64解码器
                $("#ajax_profile").attr("src", "data:image/jpeg;base64," + data);
            }
        })
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

    $("#btn_upload").click(function(){
        // 先验检查 待上传的图片是否为空
        if($("#selectAjaxImg")[0].files[0] == null)
            return

        formdata = new FormData
        formdata.append("file", $("#selectAjaxImg")[0].files[0])

        $.ajax({
            url:"",
            type:"POST",
            contentType: false,  // 不设置Content-Type请求头
            processData: false,  // 不去处理待发送的数据流
            data: formdata,
            // 注意:由于表单数据(formdata)采用了CSRF中间件验证, 使用ajax的话需要手动设置X-CSRFToken
            // 可以在后端DEBUG时查看整个request对象的值
            beforeSend: function(xhr, settings){
                xhr.setRequestHeader("X-CSRFToken", $("input[name='csrfmiddlewaretoken']").val());
            },
            error: function(data){
                alert("上传失败")
            },
            success:function(data){
                // console.log(data);
                // 不采用src形式的话 直接使用base64解码器
                $("#ajax_profile").attr("src", "data:image/jpeg;base64," + data);
            }
        })
    })
})