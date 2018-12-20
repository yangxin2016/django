var queryData = {};
$("#tb_users").bootstrapTable({
        url : '/user/getUserList',
        method:"post",
        clickToSelect: true,
        cache: false,
        striped: true,
        sortable: false,
        smartDisplay: true,
        // detailView: true,
        queryParamsType: 'other',
        pagination: true,
        sidePagination: 'server',
        pageNumber: 1,
        pageSize: 10,
        pageList: [10, 30, 50],
        queryParams: function(params) {
            for (var i in queryData) {
                if (queryData[i]) {
                    params[i] = queryData[i];
                }
            }
            return params;
        },
        columns: [{
                    field: '##',
                    valign: 'middle',
                    title: '全选/取消全选',
                    checkbox: true,
                    formatter:function(value, row, index){
                        return '';
                    }
                },{
                    field: 'user_name',
                    valign: 'middle',
                    title: '姓名',
                    formatter:function(value, row, index) {
                        return value || '--';
                    }
                },{
                    field: 'sex',
                    valign: 'middle',
                    title: '性别',
                    formatter:function(value, row, index) {
                        str = '--';
                        if(value=='m')
                            str = '男';
                        else if(value=='w'){
                            str = '女';
                        }
                        return str;
                    }
                },{
                    field: 'age',
                    valign: 'middle',
                    title: '年龄',
                    formatter:function(value, row, index) {
                        return value || '--';
                    }
                },{
                    field: 'address',
                    valign: 'middle',
                    title: '地址',
                    formatter:function(value, row, index) {
                        return value || '--';
                    }
                },{
                    field: 'create_time',
                    valign: 'middle',
                    title: '创建时间',
                    formatter:function(value, row, index) {
                        return value || '--';
                    }
                },{
                    field: 'update_time',
                    valign: 'middle',
                    title: '修改时间',
                    formatter:function(value, row, index) {
                        return value || '--';
                    }
                },{
                    field: '#',
                    title: '操作',
                    align: 'center',
                    valign: 'middle',
                    width: 200,
                    events: {
                        'click .edit': function (e, value, row, index) {
                            e.preventDefault();
                             $("#id").val(row.id);
                             $("#user_name").val(row.user_name);
                             $("#age").val(row.age);
                             $("#sex").val(row.sex);
                             $("#address").val(row.address);
                             $("#addFormDiv  .modal-title").html("修改用户");
                             $('#addFormDiv').modal();
                        },
                        'click .delete': function (e, value, row, index) {
                            e.preventDefault();
                            bootbox.confirm("确认删除？",function (res) {
                                if(res){
                                    ids = row.id
                                   $.post('/user/delete',{'ids':ids},function (data) {
                                       bootbox.alert(data.msg);
                                       refreshTable()
                                   })
                                }
                            })

                        }
                    },
                    formatter:function(value, row, index){
                        var ops = '';
                        ops +=  '<span class="edit" style="color:#2681b5;cursor: pointer;margin-right:4px;">修改</span>';
                        ops += '<span class="delete" style="color:#2681b5;cursor: pointer;margin-right:4px;">删除</span>';

                        return ops;
                    }
                }]
        ,
        responseHandler : function(res) {
            console.log(res.content)
            return res.content;
        },
        onLoadError: function(status){
            alert('请求失败');
        }
    });
$("#btn_add").click(function () {
    $("#addFormDiv  .modal-title").html("新增用户");
    $("#addFormDiv").modal();
})

function refreshTable() {
    let keyword = $('#keyword').val();
    if(keyword){
        queryData.keyword = keyword;
    }

    $("#tb_users").bootstrapTable('refresh', {
        method: 'post',
        url : '/user/getUserList',
        pageNumber: 1
    });
}
//名字模糊查询
$("#searchBtn").click(function () {
    refreshTable()
})

$("#submit").click(function(){
    let data={}
    let id = $("#id").val();
    if(id){
        data.id=id;
    }
    let user_name = $("#user_name").val()
    if(user_name){
        data.user_name = user_name;
    }
    let sex = $("#sex").val();
    if(sex){
        data.sex= sex;
    }
    let age = $("#age").val();
    if(age){
        data.age= age;
    }
    let address = $("#address").val();
    if(address){
        data.address= address;
    }
    $.post("/user/save",data,function (data) {
            alert(data.respMsg);
            if(data.status=="0000"){
                $("#addFormDiv").modal("hide");
                refreshTable()
            }else {
                return false
            }
        })
    })