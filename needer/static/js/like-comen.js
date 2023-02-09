
/* Funcion para obtener el CRFTOKEN */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


/* ajax para mandar el formulario y listar el ultimo objeto creado */
$(document).on('submit', '#form-comentario', function (e) {
    let a = window.data
    /* div donde se va a adjuntar el nuevo comentario */
    var coment = document.getElementById('comentarios');
    url = a.url_coment
    e.preventDefault();
    $.ajax({
      type: 'POST',
      url: url,
      data: {
        comentario: $('#id_comentario').val(),
        csrfmiddlewaretoken: getCookie('csrftoken'),
        action: 'post',
        
      },
      success: function (json) {
            
        try{
            document.getElementById('id_comentario').value  = ''
            data_ = JSON.parse(json.listadocomentarios);

  

            document.getElementById('coment'+data_[0].pk).innerHTML =  `<a href="#" class="text-muted  botones-interaccion text-decoration-none align-middle fs-5 fw-bold col-12 like z-2"> <i class="text-primary bi bi-chat-left-fill"></i> `+data_[0].cantidad+`</a>`
            coment.insertAdjacentHTML('afterbegin', 
            `<div id = "comentarios`+data_[0].id+`" class=" row container mw-100">

            <!--Comentario Usuario-->
            <div class="align-middle px-2 mt-2 py-2 col-12 row container-fluid px-0 d-flex justify-content-start">
              <div class="container w-100 col-12 d-flex justify-content-start align-items-center align-middle">


                <!--Foto del usuario-->
                    
                      <a href="`+data_[0].url+`" class="px-0 text-start my-auto">
                          <img class="rounded-circle img-fluid img-comment" alt="profile" src="`+data_[0].img+`"data-holder-rendered="true">
                      </a>
                    

                <!--Autor-->
                    <div class="autor-comentario col-8 col-md-9 col-lg-9 col-sm-8 col-xs-6 gap-0 ms-2 d-flex align-items-center align-middle h-100 mb-auto">
                        <h5 class="text-break text-truncate fw-bold me-lg-2 me-xl-2 me-xxl-2 me-md-2 me-sm-2 me-2 mb-0 mb-lg-0 mb-xl-0 mb-md-0 mb-sm-2 mw-100 my-0 py-0 align-middle me-lg-2">
                            <a href="`+data_[0].url+`" class="text-decoration-none text-secondary"> 
                                `+data_[0].apodo+`
                            </a> 
                        </h5>
                        <p class="my-0 text-muted texti text-start text-break text-truncate">@`+data_[0].username+`</p>
                    </div>  
                    
                  <div class="col-1 d-flex align-items-center justify-content-end">
                    <div class="dropdown dropstart">
                        <a  role="button" id="dropdownMenuLink" data-bs-toggle="dropdown" aria-expanded="false">
                            <i class="bi bi-three-dots"></i>
                        </a>
        
                        <ul class="dropdown-menu" aria-labelledby="dropdownMenuLink">

                        <li>
                            <button class="dropdown-item" onclick="deletecomentario('`+data_[0].urlComentario+`', comentarios`+data_[0].id+`)" >Eliminar</button>
                        </li>
                        
                        </ul>
                    </div>   
                  </div>
                    
                </div>

                

                <div class="col-12 my-2 text-muted text-break">
                    `+data_[0].comentario+`
                </div>
                <!--Botones de la Publicación--> 
                <div class="col-12 d-flex align-items-center gap-0 d-inline-flex text-decoration-none">
                    <div id = 'divlike`+data_[0].id+`' class="text-decoration-none">
                        <a id='like`+data_[0].id+`' href="#"  onclick="likepublicacion('`+data_[0].urllikecomentario+`')" class="text-muted float-start pe-auto text-decoration-none text-start fs-5 fw-bold col like z-2"> <i class="bi bi-heart"></i> 0</a>
                    </div>
                    <!--Fecha de la creación de la publicación-->
                    <small class="col ms-2 fw-lighter text-muted">Hace unos instantes</small>
                    
                </div>
            </div>
            </div>`
            );

        }catch{
          //TODO AGREGAR MENSAJE DE ERROR
        
        }
      },

      error: function (xhr, errmsg, err) {
        var textarea = document.getElementsByName("comentario");
        textarea.className += "bg-red"
      }
    })
  })


/* ajax para dar like publicacion*/

function likepublicacion(url){

    $.ajax({
      type: 'POST',
      url: url,
      data: {
        csrfmiddlewaretoken: getCookie('csrftoken'),
        action: 'post'
      },
      success: function (json) {
        data_ = JSON.parse(json.result)
        document.getElementById('like'+data_[0].pk).disabled=true;
        document.getElementById('like'+data_[0].pk).remove();
        document.getElementById("divlike"+data_[0].pk).innerHTML  = `<a href="#" id="dislike`+data_[0].pk+`" onclick = "dislikepublicacion('`+data_[0].url+`')" class="text-muted botones-interaccion px-0 fw-lighter text-decoration-none align-middle like z-2"> <i class="bi bi-heart-fill text-primary me-2"></i> `+data_[0].likes +`</a>`
      },

      error: function (xhr, errmsg, err) {

      }
    });

}


  /* ajax para dar dislike publicacion*/
  function dislikepublicacion(url){

    $.ajax({
      type: 'POST',
      url: url,
      data: {
        csrfmiddlewaretoken: getCookie('csrftoken'),
        action: 'post'
      },
      success: function (json) {
        data_ = JSON.parse(json.result)
        document.getElementById('dislike'+data_[0].pk).disabled=true;
        document.getElementById("divlike"+data_[0].pk).innerHTML  = `<a href="#" id="like`+data_[0].pk+`" onclick="likepublicacion('`+data_[0].url+`')" class="text-muted botones-interaccion px-0 fw-lighter text-decoration-none align-middle like z-2"> <i class="bi bi-heart me-2"></i> Like` +`</a>`//+data_[0].likes
        
      },

      error: function (xhr, errmsg, err) {

      }
    });
  }

function deletecomentario(url, id_div){
    $.ajax({
      type: 'POST',
      url: url,
      data: {
        csrfmiddlewaretoken: getCookie('csrftoken'),
        action: 'post'
      },
      success: function (json) {
        data_ = JSON.parse(json.json)

        if(data_[0].cantidad == 0){
          document.getElementById('coment'+data_[0].pk).innerHTML =  `<a href="#"  class="text-muted  botones-interaccion text-decoration-none align-middle fs-5 fw-bold col-12 like z-2" onclick="$('.form-comentario').focus();"><i class="bi bi-chat-left"></i> `+data_[0].cantidad+`</a>`
        }else{
          document.getElementById('coment'+data_[0].pk).innerHTML =  `<a href="#"  class="text-muted  botones-interaccion text-decoration-none align-middle fs-5 fw-bold col-12 like z-2" onclick="$('.form-comentario').focus();"><i class="bi text-primary bi-chat-left-fill"></i> `+data_[0].cantidad+`</a>`
        }
        
    
        id_div.remove()

      },

      error: function (xhr, errmsg, err) {

      }
    });
}

$("#id_comentario").keypress(function (e) {
  if(e.which === 13 && !e.shiftKey) {
      e.preventDefault();
  
      $(this).closest("form").submit();
  }
});

function seguirUsuario(url){


  $.ajax({
    type: 'POST',
    url: url,
    data: {
      csrfmiddlewaretoken: getCookie('csrftoken'),
      action: 'post'
    },
    success: function (json) {
      data_ = JSON.parse(json.result)
    
      document.getElementById('follow'+data_[0].pk+'').disabled=true;
      document.getElementById('follow'+data_[0].pk+'').remove();

      if (document.getElementById('cantidad_seguidores')){
        document.getElementById('cantidad_seguidores').innerText = data_[0].followers;
      }
      

      document.getElementById("seguir_usuario-"+data_[0].pk+"").innerHTML  = ` <a class="btn btn-md btn-followed rounded-pill" id="follow`+data_[0].pk+`" href="#" onclick="dejarSeguirUsuario('`+data_[0].url+`')">Seguido</a>`
    },

    error: function (xhr, errmsg, err) {

    }
  });

}


function dejarSeguirUsuario(url){


  $.ajax({
    type: 'POST',
    url: url,
    data: {
      csrfmiddlewaretoken: getCookie('csrftoken'),
      action: 'post'
    },
    success: function (json) {
      data_ = JSON.parse(json.result)
      document.getElementById('follow'+data_[0].pk+'').disabled=true;
      document.getElementById('follow'+data_[0].pk+'').remove();

      if (document.getElementById('cantidad_seguidores')){
        document.getElementById('cantidad_seguidores').innerText = data_[0].followers;
      }
      
      document.getElementById("seguir_usuario-"+data_[0].pk+"").innerHTML  = ` <a class="btn btn-md btn-primary fw-bold rounded-pill" id="follow`+data_[0].pk+`" href="#" onclick="seguirUsuario('`+data_[0].url+`')">Seguir</a>`
    },

    error: function (xhr, errmsg, err) {

    }
  });

}