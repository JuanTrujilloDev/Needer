jQuery(document).ready(function($){

    if ($('#id_groups').val() == "1"){
        $('#id_num_documento').prop('required', false)
        $('#id_first_name').prop('required', false)
        $('#id_last_name').prop('required', false)
        $('.pais').prop('required', false)
        $('.nombres').hide();
        $('.apellidos').hide();
        $('.documento').hide();
    }

    else if ($('#id_groups').val() == "2"){
        $('.nombres').show();
            $('.apellidos').show();
            $('.documento').show();
            $('#id_num_documento').prop('required', true)
            /* $('#id_num_documento').val('') */
            $('#id_first_name').prop('required', true)
            $('#id_last_name').prop('required', true)
            $('.pais').prop('required', true)
            /* $('.pais').val('') */
    }else{
        $('#id_num_documento').prop('required', false)
        $('#id_first_name').prop('required', false)
        $('#id_last_name').prop('required', false)
        $('.pais').prop('required', false)
        $('.nombres').hide();
        $('.apellidos').hide();
        $('.documento').hide();
    }


    $( "#signup_form" ).submit(function( event ) {
        if ($('#id_groups').val() == "1"){
            $('#id_num_documento').prop('required', false)
            $('#id_first_name').prop('required', false)
            $('#id_last_name').prop('required', false)
            $('.pais').prop('required', false)
            $('.nombres').hide();
            $('#id_first_name').val('')
            $('.apellidos').hide();
            $('#id_last_name').val('')
            $('.documento').hide();
            $('#id_num_documento').val('')
        }
    
        else if ($('#id_groups').val() == "2"){
            $('.nombres').show();
                $('.apellidos').show();
                $('.documento').show();
                $('#id_num_documento').prop('required', true)
                /* $('#id_num_documento').val('') */
                $('#id_first_name').prop('required', true)
                $('#id_last_name').prop('required', true)
                $('.pais').prop('required', true)
               /*  $('.pais').val('') */
        }else{
            $('#id_num_documento').prop('required', false)
        $('#id_first_name').prop('required', false)
        $('#id_last_name').prop('required', false)
        $('.pais').prop('required', false)
        $('.nombres').hide();
        $('.apellidos').hide();
        $('.documento').hide();
        }
      });
    
    

    $('select[name=groups]').change(function () {
    // hide all optional elements
    

        
    $("select[name=groups] option:selected").each(function () {
        var value = $(this).val();
        if(value == "1") {
            $('.nombres').hide();
            $('.apellidos').hide();
            $('.documento').hide();
            $('#id_num_documento').prop('required', false)
            $('#id_first_name').prop('required', false)
            $('#id_last_name').prop('required', false)
            $('.pais').prop('required', false)

           
        } else if(value == "2") {
            $('.nombres').show();
            $('.apellidos').show();
            $('.documento').show();
            $('#id_num_documento').prop('required', true)
           /*  $('#id_num_documento').val('') */
            $('#id_first_name').prop('required', true)
            $('#id_last_name').prop('required', true)
            $('.pais').prop('required', true)
            /* $('.pais').val('') */
           
        }

    });
}); 
});