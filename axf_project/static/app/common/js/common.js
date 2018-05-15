function subShop( goods_id) {
    csrf = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url: '/axf/subshop/',
        type: 'POST',
        data: {'goods_id': goods_id},
        headers: {'X-CSRFToken': csrf},
        datatype: 'json',
        success: function (msg) {
            $('#number_' + goods_id).html(msg.c_num);
            $('#total_price').html('总价:'+ msg.total_price)
        },
        error: function (msg) {
            alert('请求错误')
        }
    })
}

function addShop( goods_id) {
    csrf = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url: '/axf/addshop/',
        type: 'POST',
        data: {'goods_id': goods_id},
        headers: {'X-CSRFToken': csrf},
        datatype: 'json',
        success: function(msg) {
            $('#number_' + goods_id).html(msg.c_num);
            $('#total_price').html('总价:'+ msg.total_price)
        },
        error: function(msg) {
            alert('请求错误')
        }
    })
}


function changeselect( cart_id ) {
    csrf = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url: '/axf/changeselect/',
        type: 'POST',
        data: {'cart_id': cart_id},
        datatype: 'json',
        headers: {'X-CSRFToken': csrf},
        success: function (msg) {
            if(msg.is_select) {
                s = '<span onclick="changeselect(' + cart_id+ ')">√</span>'
            }else{
                s = '<span onclick="changeselect(' + cart_id+ ')">×</span>'
            }

            if(msg.is_select_all){
                ss = '<span><span onclick="select_all()">√</span></span>'
            }else{
                ss = '<span><span onclick="select_all()">×</span></span>'
            }
            $('#select_' + cart_id ).html(s);
            $('#total_price').html('总价:'+ msg.total_price);
            $('#all_select').html(ss)
        },
        error: function (msg) {
            alert('请求失败')
        }
    })
}

function select_all() {
    csrf = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url: '/axf/selectall/',
        type: 'POST',
        datatype: 'json',
        headers: {'X-CSRFToken': csrf},
        success: function(msg) {
            carts_id = msg.carts_id;
            if (carts_id.length > 0){
                for (var i = 0; i < carts_id.length; i++){
                    s = '<span onclick="changeselect(' + carts_id[i] + ')">√</span>';
                    $('#select_' + carts_id[i] ).html(s)
                }
            }
            $('#all_select').html('<span><span onclick="select_all()">√</span></span>')
            $('#total_price').html('总价:' + msg.total_price)
        },
        error: function(msg) {
            alert('请求错误')
        }

    })
}