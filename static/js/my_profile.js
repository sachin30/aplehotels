//ajax javascript for my profile

function profile_info(){
    
    $('#my_profile_div_id').attr('class','my-4 border bg-success py-2')
    $('#reservations_div_id').attr('class','my-4 border bg-warning py-2')
    $('#change_password_div_id').attr('class','my-4 border bg-warning py-2')
    data="<div class='row'><div class='col-lg-3 col-sm-8 border'><img class='border border-dark' height=300 width=300 src="+img_source+"></div><div class='col-lg-9 col-sm-8 border pt-2'><table class='table table-striped'><tr><th>Name :</th><td>"+user_first_name+"  "+user_last_name+"</td></tr><tr><th>Email :</th><td>"+user_email+"  </td></tr><tr><th>Username :</th><td>"+user_username+" </td></tr></table></div></div>";
    console.log('data added to html ')
    $('#profile_content').html(data);

}
function reservations_info(){
    
    $('#my_profile_div_id').attr('class','my-4 border bg-warning py-2')
    $('#reservations_div_id').attr('class','my-4 border bg-success py-2')
    $('#change_password_div_id').attr('class','my-4 border bg-warning py-2')
    $.ajax({
        url:reservations_url,
        method:"POST",
        data:{csrfmiddlewaretoken:csr},
        success:function(data){
            active_reservations=data.active_reservations;
            old_reservations=data.old_reservations;
            
            console.log(active_reservations);
            console.log(old_reservations);
            console.log(data.status);
            let output='';
            let output2='';
            let top_row='';
            let middle_row='';
            if(active_reservations.length !== 0){
                console.log("active reservations")
                top_row="<div><div><h3 class='my-2'>Active Bookings</h3></div><div><table id='active_reservations_table' class='table table-striped'><tr><th>Hotel</th><th>Room</th><th>Check In</th><th>Check Out</th><th>Total Rooms</th><th>Total Amount</th><th>Payment Status</th></tr></table></div></div>";
                for(i=0;i<active_reservations.length;i++){
                    output += "<tr><td>"+active_reservations[i].hotel+"</td><td>"+active_reservations[i].room_type+"</td><td>"+active_reservations[i].start_date+"</td><td>"+active_reservations[i].end_date+"</td><td>"+active_reservations[i].rooms_reserved+"</td><td>"+active_reservations[i].total_amount+"</td><td>"+active_reservations[i].payment_status+"</td></tr>";
                }
            }
            if(old_reservations.length !== 0){
                middle_row="<div><div><h3 class='my-2'>Old Bookings</h3></div><div><table id='old_reservations_table' class='table table-striped'><tr><th>Hotel</th><th>Room</th><th>Check In</th><th>Check Out</th><th>Total Rooms</th><th>Total Amount</th><th>Payment Status</th></tr></table></div></div>";
                for(i=0;i<old_reservations.length;i++){
                    output2 += "<tr><td>"+old_reservations[i].hotel+"</td><td>"+old_reservations[i].room_type+"</td><td>"+old_reservations[i].start_date+"</td><td>"+old_reservations[i].end_date+"</td><td>"+old_reservations[i].rooms_reserved+"</td><td>"+old_reservations[i].total_amount+"</td><td>"+old_reservations[i].payment_status+"</td></tr>";
                }
            }
            $('#profile_content').html(top_row);
            $('#profile_content').append(middle_row);
            $('#active_reservations_table').append(output);
            $('#old_reservations_table').append(output2);
        }
    })

}
function change_password_page(){
    
    $('#my_profile_div_id').attr('class','my-4 border bg-warning py-2')
    $('#reservations_div_id').attr('class','my-4 border bg-warning py-2')
    $('#change_password_div_id').attr('class','my-4 border bg-success py-2')
    data="<div id='form_div'><form id='change_password_form' action='' name='change_password'><h3 class='my-3'>Change Password  <span title='Show/Hide Password' onclick='toggle_show_password()'><i class='fa fa-eye'></i></span></h3><h5>Enter Your new password</h5><input class='form-control' type='password' name='change_password1' id='change_password1'><h5 class='my-3'>Confirm Changed Password</h5><input class='form-control' type='password' name='change_password2' id='change_password2'> <br/><button class='btn btn-success my-3' type='submit' onclick='change_password_validation()'>Change Password</button></form></div>";
    console.log('change pass html ');
    $('#profile_content').html(data);
}


//change form validation
function change_password_validation(){

    $("#change_password_form").validate({
        rules: {
                    change_password1:{
                        required:true,
                        minlength: 8
                    },
                    change_password2:{
                        required:true,
                        equalTo:"#change_password1"
                    }
                },
                
        messages: {
                    change_password1:{
                        required:"Please enter password",
                        minlength: "Your password must be at least 8 characters long"
                    },
                    change_password2:{
                        required:"Please enter password to confirm",
                        equalTo:"passwords did not match"
                    }
                }
    });
    
    
}
//toggle password display
function toggle_show_password(){
    let type1=$('#change_password1').attr('type')
    let type2=$('#change_password2').attr('type')
    if(type1 == undefined && type2 == undefined){
        $('#change_password1').attr('type','password')
        $('#change_password2').attr('type','password')
    }else{
        $('#change_password1').removeAttr('type')
        $('#change_password2').removeAttr('type')
    }
}

//for changing password
$(document).on('submit','#change_password_form',function(e){
    e.preventDefault();
    change_password1 = $('#change_password1').val()
    change_password2 = $('#change_password2').val()


    $.ajax({
        url: change_password_url,
        method:"POST",
        data:{csrfmiddlewaretoken:csr,change_password1:change_password1,change_password2:change_password2},
        success:function(data){
            console.log(data.status)
            if(data.status == 'success'){
                output_html="<div><h3>Password changed successfully</h3><a class='btn btn-success' href="+my_profile_url+"> Go to Login</a></div>"
                $('#profile_content').html(output_html);
            }
            if(data.status == 'failed'){
                output_html="<div><h3>Password Not strong enough</h3><a class='btn btn-success' href="+my_profile_url+"> Go to Profile</a></div>"
                $('#profile_content').html(output_html);
            }
        }
    })
})



