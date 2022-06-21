
  
function loadMore(){

       
        jQuery.ajax({
                url:jQuery('.load-more:last').attr('value'),
                method: 'GET',
                beforeSend: function() {
                    $('load-more').attr('value', '#');
                    $('.load-more').remove();
                    $('.infinite-content').append("<div class='d-flex justify-content-center my-3 loading'>\
                    <div class='spinner-border text-terciary' role='status'>\
                        <span class='sr-only'></span>\
                    </div>\
                </div>");
                
            }

            }).done(function(data){
                $('.loading').remove();
                jQuery('.infinite-content').append(data);


            });
        

        
}

$( document ).ready(function() {
  // Handler for .ready() called.

  
    $('.main').scroll(function(){

        if ($(this).scrollTop() > $('.infinite-content').height() && $('load-more:last').attr('value') != '#'){
              $('.load-more').click();
        }
    });

});


