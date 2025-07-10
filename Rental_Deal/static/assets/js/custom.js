
    $(document).ready(function(){
  
   $("#date").datepicker({
      dateFormat: "dd-mm-yy",
      autoclosed:true,
      changeMonth: true,
      changeYear: true,
      yearRange: "-100:+0",
      maxDate: 0
     
  });

   
   $(".startDate").datepicker({
      dateFormat: "dd-mm-yy",
      changeMonth: true,
      changeYear: true,
      autoclosed:true,
      yearRange: "-100:+0",
      onSelect: function (date) {
          var date2 = $('#deal_start_date').datepicker('getDate');
          $('#deal_end_date').datepicker('option', 'minDate', date2);
          appendDate();
          $('#deal_end_date').datepicker('option', 'yearRange', "-100:+10");
      }
    });
    $('.endDate').datepicker({
      dateFormat: "dd-mm-yy",
      changeMonth: true,
      changeYear: true,
      onClose: function () {
           var dt1 = $('#deal_start_date').datepicker('getDate');
           var dt2 = $('#deal_end_date').datepicker('getDate');
           if (dt2 <= dt1) {
               var minDate = $('#deal_end_date').datepicker('option', 'minDate');
               $('#deal_end_date').datepicker('setDate', minDate);
           }
           
       }
      });
    $('#owner_source').val("Reference");
    $('#tenant_source').val("Reference");
});

   $(document).on('click','.remove_file',function(){
    
      var name = $(this).data("name");
     var  value = $(this).attr("id");
     var existingType = $(this).data("existing");                     
        if($('#'+name+'_removed').val().length == 0){           
          $('#'+name+'_removed').val(value);  
                    
        }
        else{ 
          $('#'+name+'_removed').val($('#'+name+'_removed').val()+', '+value);
        }
          if(existingType == "old"){
             $('#'+name+'_existing_count').val(parseInt($('#'+name+'_existing_count').val())-1); 
          } 
          else{
             $('#'+name+'_new_removed_count').val(parseInt($('#'+name+'_new_removed_count').val()) -1); 
          }                                               
        $(this).parent('div').remove();
       $(this).parents('span').remove(); 
    });
  $('input[type="file"]').on('change', function() {
    
    var  namedata =$(this).attr("id");
    $('.'+namedata+'_list').empty();              
     $('#'+namedata+'_new_removed_count').val(this.files.length);   
            
     if(this.files.length >0){        
    var filename = this.files[0].name;
    var lastIndex = filename.lastIndexOf("\\");
      if (lastIndex >= 0) {
          filename = filename.substring(lastIndex + 1);
      }
    
    $('#yt'+$(this).attr("id")).val("");
    filesize=0;
    var fileCount=4;
     if($('#'+$(this).attr("id")+'_existing_count').val()){
      fileCount=fileCount-parseInt($('#'+$(this).attr("id")+'_existing_count').val());
    } 
     
      files=this.files;    
      var result_array=Array.from(files);
      var added=false;      
   for(let i=0; i<this.files.length; i++){        
           filesize = parseFloat(filesize+this.files[i].size);
           var name=files[i].name
        $.map(result_array, function(name) {
         if (name!== filename) {
          var added=true;
         }
        })
        if (!added) {
            $('.'+namedata+'_list').append('<div class="upload_prev">'+'<a class="filenameupload">'+this.files[i].name+'</a>'+'<p class="remove_file" id="'+this.files[i].name+'" data-name="'+namedata+'"'+'>X</p></div>');
        }
        }
    if(filesize/1024/1024 > 3){
      $("#"+$(this).attr("id")+"_error").html("File size should be less than 3 mb").show();
      $('#'+$(this).attr("id")).val("");
      $('.'+namedata+'_list').empty();
       $('#'+namedata+'_new_removed_count').val('0');  
    }
    else if(this.files.length>fileCount) {
      alert("Length exceeded. Please select no more than 4 files");
          $('#'+$(this).attr("id")).val("");    
      $('.'+namedata+'_list').empty();
       $('#'+namedata+'_new_removed_count').val('0');
      } 
    else {
      $('#yt'+$(this).attr("id")).val("true");      
      $("#"+$(this).attr("id")+"_error").html('').hide();
      $("#"+$(this).attr("id")+"-error").html('').hide();
    }
     }

  }); 

    $('#deal_form').validate({
  ignore: "",
  rules: {
    date: {
      required: true,
    },
    submitted_by_agent: {
       required: true,
     },
    reference_number: {
      alphanum_special: true,
      required: true,
      maxlength: 15,

    },
    screening: {
      alphanum_special: true,
      required: true,
    },
    is_new_deal: {
      alphanum_special: true,
      required: true,
    },

    project_name: {
      required: true,
      maxlength: 255,
    },
    mediating_agency: {
      alphanum_special: true,
      maxlength: 255,
    },
    mediating_agent_name: {
      alphanum_special: true,
      maxlength: 255,
    },
    mediating_agency_brn: {
      alphanum_special: true,
      maxlength: 255,
    },

    unit_details: {
      alphanum_special: true,
      required: true,
      maxlength: 15,
    },

    building_name: {
      alphanum_special: true,
      required: true,
      maxlength: 255,
    },

    rental_price: {
      numeric: false,
      required: false,
      maxlength: 100,
    },

    deal_start_date: {
      required: true,
    },

    deal_end_date: {
      required: true,
    },
    owner_first_name: {
      alphanum_special: true,
      required: true,
      maxlength: 255,
    },
    owner_source: {
      required: true,
    },
    owner_mobile: {
      phoneNumber: true,
      required: true,
      minlength: 6,
      maxlength: 15,
    },
    mediating_agent_phone: {
      phoneNumber: true,
      minlength: 6,
      maxlength: 15,
    },
    owner_email: {
      custom_email: true,
      required: true,
      maxlength: 100
    },
    tenant_first_name: {
      alphanum_special: true,
      required: true,
      maxlength: 255,
    },
    tenant_source: {

      required: true,
    },
    tenant_mobile: {
      phoneNumber: true,
      required: true,
      minlength: 6,
      maxlength: 15,
    },
    tenant_email: {
      custom_email: true,
      required: true,
      maxlength: 100
    },
     seller_nationality: {
              required: true,
              maxlength: 100,
    },
    buyer_nationality: {
      required: true,
      maxlength: 100,
    },
    agent_email: {
      custom_email: true,
      maxlength: 100
    },
    tenant_agent_email: {
      custom_email: true,
      maxlength: 100
    },
    mediating_agent_email: {
      custom_email: true,
      maxlength: 100
    },
    owner_agency: {
      alphanum_special: true,
      required: true,
      maxlength: 255,
    },
    agent_first_name: {
      alphanum_special: true,
      required: true,
      maxlength: 255,
    },
    brn: {
      alphanum_special: true,
      maxlength: 255,
    },
    agent_phone: {
      phoneNumber: true,
      required: true,
      minlength: 6,
      maxlength: 15,
    },

    tenant_agency: {
      alphanum_special: true,
      required: true,
      maxlength: 255,
    },
    tenant_agent_first_name: {
      alphanum_special: true,
      required: true,
      maxlength: 255,
    },
    tenant_brn: {
      alphanum_special: true,

      maxlength: 255,
    },
    tenant_agent_phone: {
      phoneNumber: true,
      minlength: 6,
      maxlength: 15,
    },
    total_commission: {
      numeric: true,
      required: true,
      maxlength: 10,
    },
    less_outsude_commission: {
      alphanum_special: true,
      required: true,
      maxlength: 100,
    },
    net_commission: {
      numeric: true,
      required: true,
      maxlength: 10
    },
    agent1: {
      required: true,
      numeric: true,
      maxlength: 10
    },
    agent2: {
      numeric: true,
      maxlength: 10
    },
    agent3: {
      numeric: true,
      maxlength: 10
    },
    classic: {
      numeric: true,
      maxlength: 10
    },
   
    
     plot_no: {
         alphanum_special: true,
        maxlength: 255,
          },
     
    mode_of_payment: {
        only_text: true,
        maxlength: 255,
       },        
    agent_comment: {
      maxlength: 255,
    },

    comments: {
      maxlength: 255,
    },
    receipt_no: {
      alphanum_special: true,
      required: true,
      maxlength: 100,
    },
    is_rental_aml: {
      required: false,
    },

    kyc_number: {
      numeric: true,
      maxlength: 45,
    },
    property_size: {
         alphanum_special: true,
         maxlength: 255,
       },
     premises_no: {
         alphanum_special: true,
         maxlength: 255,
         },
     security_deposit: {
         numeric: false,
         maxlength: 255,
           },
    property_type:{
      required: false,
      alphanum_special: true,
      maxlength: 255
     }     

  },
  messages: {
    owner_mobile: {
      phoneNumber: 'Phone number must only contain numbers and +'
    },
    mediating_agent_phone: {
      phoneNumber: 'Phone number must only contain numbers and +'
    },
    tenant_mobile: {
      phoneNumber: 'Phone number must only contain numbers and +'
    },
    agent_phone: {
      phoneNumber: 'Phone number must only contain numbers and +'
    },
    tenant_agent_phone: {
      phoneNumber: 'Phone number must only contain numbers and +'
    }
  },
  errorPlacement: function (error, element) {
       if (element.attr("type") == "radio") {
         var id = element.attr("id")
         $('#' + id + "_error").css('margin-right','200px');
         error.addClass('field_error');
         error.insertAfter('#' + id + "_error");
       } else {
         error.insertAfter(element);
       }
     }
});

$.validator.addMethod('phoneNumber', function(value, element) {
      var exp = /^[\+]?\d*$/im;
    //console.log(exp.test(value));
      return exp.test(value);
   }, 'Phone number must only contain numbers and +');


 
 $(document).on('click', '#create_deal', function(event) {  
            $('[name="submitted_by_agent"],[name="owner_agency"],[name="agent_first_name"],[name="agent_phone"],[name="tenant_agency"],[name="tenant_agent_first_name"],[name="tenant_agent_phone"],[name="total_commission"],[name="less_outsude_commission"],[name="net_commission"],[name="classic"],[name="agent1"],[name="receipt_no"],[name="is_sale_aml"],[name="agent_name1"],[name="is_rental_aml"]').each(function () {
                  $(this).rules('add','required');
              });       
           if($('#deal_form').valid()){  
             $('#save_as').val("update-deal"); 
             var url="/list";

             
            if(countMultipleFiles('tenancy_contract') & countMultipleFiles('title_deed') & countMultipleFiles('owner_passport_copy') & countMultipleFiles('tenant_passport_visa_copy')  & countMultipleFiles('rental_deposit_cheque_copy') & countMultipleFiles('tenancy_application_form') & countMultipleFiles('screening') & countMultipleFiles('key_hand_over_form') & checkKyc()){              
               updatefunctionality(url);
            }
           }else{
               $('html, body').animate({
                     scrollTop: $('.main-header').offset().top
                   }, 1000);
            }
           
        });


     $(document).on('click', '#update_draft', function(event) {    
            $('[name="owner_agency"],[name="agent_first_name"],[name="agent_phone"],[name="tenant_agency"],[name="tenant_agent_first_name"],[name="tenant_agent_phone"],[name="total_commission"],[name="less_outsude_commission"],[name="net_commission"],[name="classic"],[name="agent1"],[name="receipt_no"],[name="is_rental_aml"],[name="agent_name1"]').each(function () {
                  $(this).rules('remove','required');
              });      
              if($('#deal_form').valid() & countMultipleFiles('screening')){     
                $('#save_as').val("update-draft"); 
                var url="/list/draft";                        
                updatefunctionality(url);
               }else{
               $('html, body').animate({
                     scrollTop: $('.main-header').offset().top
                   }, 1000);
            }
              
           });


      function checkKyc(){
            var result=true;
            $('#rental_kyc_number_error').empty();
          $('#kyc_number_error').empty();
            var existing_count=parseInt($('#rental_kyc_number_existing_count').val());
            var removed_count=parseInt($('#rental_kyc_number_new_removed_count').val());
            if($('#rental_kyc_number_new_removed_count').val() == ''){
                  var removed_count=0;
                }
            if((existing_count < 1) && (removed_count < 1) && ($('#kyc_number').val()=='')){
              result =false;
              $('#rental_kyc_number_error').html("Either KYC Form or KYC Number is required!").show();
              $('#kyc_number_error').html("Either KYC Form or KYC Number is required!").show();
              $(document).on("keyup", "input[name='kyc_number']", function(e){
                 $("#"+'kyc_number'+"_error").hide();
           });
            }
            return result;
          }

           function countMultipleFiles(feild){     
             var result=true;             
             if(($('#'+feild+'_existing_count').val() < 1) && ($('#'+feild+'_new_removed_count').val() < 1)){         
               result =false;             
          var  feildvalue= feild;
               $('#'+feild+'_error').html("This field is required.").show().css("text-transform", "capitalize");          
        }
          return result;
      }


        function updatefunctionality(url){
              var previous_url = document.referrer,
              parts = previous_url.split("/"),
              last_part = parts[parts.length-1];
                $('#create_deal').attr('disabled',true);
                $('.loadscreen').show();
                 $('html, body').animate({
                   scrollTop: $('.main-header').offset().top
                 }, 1000);
                 if(document.getElementById("date").disabled == true)
                  document.getElementById("date").removeAttribute('disabled');
                 $.ajax({
                     method: "POST",
                     headers: {
                         'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
                     },  
                     url: "http://dealsaws.classicproperties.ae/rental-deals/update",
                     data:new FormData($("#deal_form")[0]),
                     contentType: false,
                     processData: false,
                   })
                 .done(function( data ) {
                     $('.loadscreen').hide();
                     $('#create_deal').removeAttr('disabled',true);
                     if(data.status== 'success'){
                       $("#alert-primary").text("Rental Deal Updated Successfully");
                        $("#successmsg").show();
                        setTimeout(function() {  
                          if (url=='/list') {
                            if (last_part=='draft') {
                              window.location.href = "http://dealsaws.classicproperties.ae/rental-deals"+url;
                            }
                            else{
                              window.location.href = document.referrer;
                            }
                          }else{
                            window.location.href = "http://dealsaws.classicproperties.ae/rental-deals"+url;
                          }                                        
                        }, 2000); 
                     }
                      else if(data.status=='validation_error'){
                         $.each(data.data, function (key, val) {
                             $("#"+key+"_error").text(val[0]);
                             $("#"+key+"_error").show();
                             $(document).on("keyup", "input[name='"+key+"']", function(e){
                                   $("#"+key+"_error").hide();
                             });
                             $(document).on("change", "select[name='"+key+"']", function(e) {
                                   $("#"+key+"_error").hide();
                             });
                         });
                     }
                     else{
                      if(data.data == "DUF500")
                        var alertmsg = data.message;
                      else
                        var alertmsg = "Something Went Wrong !";
                      $("#alert-primary").text(alertmsg);
                      $("#successmsg").show();
                      setTimeout(function(){ $('#successmsg').fadeOut() }, 3000);
                     }
                     
                 });

            }

            $('#property').on('change',function() {
       var id = $(this).find(':selected').val();
      $.ajax({
        method:"POST",
        url:"http://dealsaws.classicproperties.ae/property/get-data",
        data:{
              "_token": "3rNPlBArTNIMRZurkbS34qEIQwfkHvK5Sa7TPJwT",
              "id"    : id
          },
      })
      .done(function( data ) {
        if(data.status=='success'){
          $('#reference_number').val(data.data.bayut_property_ref_no)
          $('#property_size').val(data.data.property_size)
          var property_usage= data.data.property_parent_type.toLowerCase();
          $("#property_usage").val(property_usage).change();
          $('#project_name').val(data.data.property_title)
         $('#building_name').val(data.data.tower_name)
         $('#rental_price').val(data.data.price)
         
         
        }
        else if(data.status=='fail'){
          $("#alert-primary").text('Data not Found!');
          $("#successmsg").show();
          $('html, body').animate({
            scrollTop: $('.main-header').offset().top
          }, 1000);
          setTimeout(function(){ $('#successmsg').fadeOut() }, 3000);
        }
      })
  })    
 