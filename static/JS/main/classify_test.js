$(function(){
    $("#selectImg").change(function(){
        if($(this)[0].files[0] != null){
            $("#profile").attr("src",URL.createObjectURL($(this)[0].files[0]));
        }
    });

    $("#selectAjaxImg").change(function(){
        if($(this)[0].files[0] != null){
            $("#ajax_profile").attr("src",URL.createObjectURL($(this)[0].files[0]));
        }
    });

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