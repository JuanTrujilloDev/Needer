
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
    document.getElementById('boton-comentar').disabled=true;
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
            document.getElementById('id_comentario').value  = ''
            document.getElementById('div-comentar').innerHTML =  `
                                        <button id='boton-comentar' class="btn text-primary like float-end" type="submit"><i class="bi bi-chat-left"></i> Comentar</button>`
            data_ = JSON.parse(json.listadocomentarios)
            console.log(data_)
            document.getElementById('coment'+data_[0].pk).innerHTML =  `<button class="btn text-primary align-middle border-secondary fs-5 fw-bold col-12 like z-2">`+data_[0].cantidad+` <i class="bi bi-chat-left"></i></button>`
            coment.insertAdjacentHTML('afterbegin', 
            `<div id = "comentarios`+data_[0].id+`">
            <div class="align-middle mt-2 py-2 text-break">
                <div class="col-12 d-flex align-items-center justify-content-start pt-4 gap-0 row">
                <!--Foto del usuario-->
                    <div class="col-lg-2 col-md-2 col-3 justify-content-center d-flex pe-0 mb-3">
                        <a href="`+data_[0].url+`" class="text-center">
                            <img class="rounded-circle img-fluid profile-img" alt="profile" src="`+data_[0].img+`"data-holder-rendered="true">
                        </a>
                    </div>

                <!--Autor-->
                    <div class="row col-7 col-md-8 col-lg-8 ms-1 align-baseline mb-auto">
                        <h5 class="text-secondary fw-bold mb-0 mb-lg-0 mb-xl-0 mb-md-0 mb-sm-2 mw-100 my-0 py-0">
                            <a href="`+data_[0].url+`" class="text-decoration-none text-secondary"> 
                                `+data_[0].apodo+`
                            </a> 
                        </h5>
                        <p class="my-0 text-muted">@`+data_[0].username+`</p>
                    </div>   
                </div>
                <div class="col-12">
                    <p class="text-muted">`+data_[0].comentario+`</p>
                </div>
                <!--Botones de la Publicación--> 
                <div class="col-12 row text-decoration-none border-bottom border-top">
                    <div id = 'divlike`+data_[0].id+`' class="col-12 text-decoration-none ">
                        <button id='like`+data_[0].id+`'  onclick="likepublicacion('`+data_[0].urllikecomentario+`')" class="btn text-primary align-middle fs-5 fw-bold col-12 like z-2"> 0 <i class="bi bi-heart"></i></button>
                    </div>
                    <button onclick="deletecomentario('`+data_[0].urlComentario+`', comentarios`+data_[0].id+`)" >ELIMINAR</button>
                </div>
            </div>
            </div>`
            );
      },

      error: function (xhr, errmsg, err) {

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
        document.getElementById("divlike"+data_[0].pk).innerHTML  = `<button id="dislike`+data_[0].pk+`" onclick = "dislikepublicacion('`+data_[0].url+`')" class="btn text-primary border-secondary align-middle fs-5 fw-bold col-12 like z-2">`+data_[0].likes +` <i class="bi bi-heart-fill"></i></button>`
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
        document.getElementById("divlike"+data_[0].pk).innerHTML  = `<button id="like`+data_[0].pk+`" onclick="likepublicacion('`+data_[0].url+`')" class="btn text-primary align-middle fs-5 fw-bold col-12 like z-2">`+data_[0].likes +` <i class="bi bi-heart"></i></button>`
        
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
        document.getElementById('coment'+data_[0].pk).innerHTML =  `<button class="btn text-primary align-middle border-secondary fs-5 fw-bold col-12 like z-2">`+data_[0].cantidad+` <i class="bi bi-chat-left"></i></button>`
    
        id_div.remove()

      },

      error: function (xhr, errmsg, err) {

      }
    });
}