//get the image from Server
function postDownloadImage() {
    var xmlhttp;
    if (window.XMLHttpRequest) {
        //  IE7+, Firefox, Chrome, Opera, Safari 浏览器执行代码
        xmlhttp = new XMLHttpRequest();
    }
    else {
        // IE6, IE5 浏览器执行代码
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4 && xmlhttp.status == (200 || 304)) {
            var imgDown = document.getElementById("download-image");
            var obj = JSON.parse(xmlhttp.responseText);
            imgDown.src = obj["imageSrc"];
            console.log(imgDown.src)
            console.log(obj["imageSrc"])
            console.log(obj["len"])
            console.log(obj["result"])
            console.log(obj["result"][0].class_name)
            getResult(obj);
        }
    }
    xmlhttp.open("GET", "/imgDownload", true);
    xmlhttp.send();
    imgAdaptive(document.getElementById("download-image"));
}

//make image adaptive container
function imgAdaptive(obj) {
    parent = obj.parentNode;
    imgW = obj.width;
    imgH = obj.height;
    imgP = imgW / imgH;
    parW = parent.offsetWidth;
    parH = parent.offsetHeight;
    parP = parW / parH;
    if (imgP > parP) {
        obj.style.width = "100%";
        obj.style.height = "auto";
    }
    else {
        obj.style.width = "auto";
        obj.style.height = "100%";
    }
}

window.onload = function () {
    var img = document.getElementsByClassName("adaptiveImg");
    for (var i = 0; i < img.length; i++) {
       imgAdaptive(img[i]);
    }
    //getResult(testObj);
}

//show the image selected
function fileSelect(obj) {
    var imgFile = obj.files[0];
    var fr = new FileReader();
    fr.onload = function () {
        document.getElementById('upload-image').src = fr.result;
    };
    fr.readAsDataURL(imgFile);
    
    imgDown(obj);
    document.getElementById("download-image").src = "default_processed.png";
}

//post image selected to server
function imgPost() {
    var fd = new FormData();
    var img = document.getElementById("imageSelect").files[0];
    fd.append("image", img);
    $.ajax({
        url: '/upImg',
        type: 'POST',
        cache: false,
        data: fd,
        processData: false,
        contentType: false,
        success: function (data) {
            alert("upload success");
        },
        error: function (data) {
            alert("upload failed");
        }
    })
}

//process the json
var testJson = '{' +
    '"imageSrc": "test.jpg",'+
    '"len": 2,'+
    '"result": ['+
    '    {'+
    '        "class_name": "zang_wu",'+
    '        "score": "0.888",'+
    '        "x_min": "50",'+
    '        "x_max": "100",'+
    '        "y_min": "50",'+
    '        "y_max": "10"'+
    '    },'+
    '    {'+
    '        "class_name": "hua_heng",'+
    '        "score": "0,999",'+
    '        "x_min": "150",'+
    '        "x_max": "200",'+
    '        "y_min": "150",'+
    '        "y_max": "20"'+
    '    }'+
    ']'+
'}';

var testObj = JSON.parse(testJson);

function getResult(obj) {
    let rowNum = obj.len;
    let tableInner = ""
    for (let i in obj.result) {
        var num = parseInt(i) + 1;
        var tp = '<tr>' +
        '<th class="text-nowrap" scope="row">#'+ num +'</th>' +
        '<td class="text-center">'+ obj.result[i].class_name +'</td>' +
        '<td class="text-center">'+ obj.result[i].score +'</td>' +
        '<td class="text-center">'+ obj.result[i].description +'</td>' +
        '</tr>'
        tableInner += tp;
    }
    document.getElementById('resultTable').innerHTML = tableInner;
}
