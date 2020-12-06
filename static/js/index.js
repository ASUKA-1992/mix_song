//タイトル入力欄表示選択
function change_input_title(prm) {
    if(prm == 'hide'){
        $("#div_input_title").fadeOut();
        $("#input_title").val("");
        //artist and titleボタンを非選択状態に
        $("#p_artist_title").addClass("not_selected_font");
        $("#p_artist_title").removeClass("selected_font");
        //onlyボタンを選択状態に
        $("#p_artist").addClass("selected_font");
        $("#p_artist").removeClass("not_selected_font");

        $('#input_title').prop('required',false);
    } else {
        $("#div_input_title").fadeIn();
        //onlyボタンを非選択状態に
        $("#p_artist").addClass("not_selected_font");
        $("#p_artist").removeClass("selected_font");
        //artist and titleボタンを選択状態に
        $("#p_artist_title").addClass("selected_font");
        $("#p_artist_title").removeClass("not_selected_font");

        $('#input_title').prop('required',true);
    }
}

//検索スタート
function input_start(){
    $('#form_input').click();
}

//画面ロード時
$(document).ready(function(){
    //インプットエリアを画面左下に配置
    var wH = $(window).height() - 60;
   	$('.right_div').css('height',wH+'px');
});

//ajax関連の記述
//おまじない ここから---------------------------
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
         }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

//おまじない ここまで---------------------------
