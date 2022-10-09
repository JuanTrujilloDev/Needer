
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
    var coment = document.getElementById('comentarios');
    e.preventDefault();
    $.ajax({
      type: 'POST',
      url: a.url_coment,
      data: {
        comentario: $('#id_comentario').val(),
        csrfmiddlewaretoken: getCookie('csrftoken'),
        action: 'post',
        
      },
      success: function (listadocomentarios) {
            document.getElementById('id_comentario').value  = ''
            data = JSON.parse(listadocomentarios.listadocomentarios)
            coment.insertAdjacentHTML('afterbegin', 
            `<div class="align-middle mt-2 py-2 text-break">
                <div class="col-12 d-flex align-items-center justify-content-start pt-4 gap-0 row">
                <!--Foto del usuario-->
                    <div class="col-lg-2 col-md-2 col-3 justify-content-center d-flex pe-0 mb-3">
                        <a href="`+data[0].url+`" class="text-center">
                            <img class="rounded-circle img-fluid profile-img" alt="profile" src="`+data[0].img+`"data-holder-rendered="true">
                        </a>
                    </div>

                <!--Autor-->
                    <div class="row col-7 col-md-8 col-lg-8 ms-1 align-baseline mb-auto">
                        <h5 class="text-secondary fw-bold mb-0 mb-lg-0 mb-xl-0 mb-md-0 mb-sm-2 mw-100 my-0 py-0">
                            <a href="`+data[0].url+`" class="text-decoration-none text-secondary"> 
                                `+data[0].apodo+`
                            </a> 
                        </h5>
                        <p class="my-0 text-muted">@`+data[0].username+`</p>
                    </div>   
                </div>
                <div class="col-12">
                    <p class="text-muted">`+data[0].comentario+`</p>
                </div>
                <!--Botones de la Publicación--> 
                <div class="col-12 row text-decoration-none border-bottom border-top">
                    <button id='likecoment' class="btn text-primary col-6 like z-2"><i class="bi bi-heart"></i></button>
                </div>
            </div>`
            );
      },

      error: function (xhr, errmsg, err) {

      }
    })
  })

/* ajax para dar like publicacion*/
$(document).on('click', '#like', function (e) {
    e.preventDefault();
    let a = window.data

    $.ajax({
      type: 'POST',
      url: a.url_like,
      data: {
        
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        action: 'post'
      },
      success: function (json) {
        document.getElementById("like_count").textContent = json['result']
        document.getElementById("divlike").innerHTML  = `<button id="dislike" class="btn text-primary  border-secondary col-6 like z-2"><i class="bi bi-heart"></i> No Me gusta</button>
                                                        <button class="btn text-primary col-6 like z-2"><i class="bi bi-chat-left"></i> Comentar </button>`
      },

      error: function (xhr, errmsg, err) {

      }
    });
  })

  /* ajax para dar dislike publicacion*/
  $(document).on('click', '#dislike', function (e) {
    let a = window.data

    e.preventDefault();
    $.ajax({
      type: 'POST',
      url: a.url_dislike,
      data: {
        
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        action: 'post'
      },
      success: function (json) {
        document.getElementById("like_count").textContent = json['result']
        document.getElementById("divlike").innerHTML  = `<button id="like" class="btn text-primary col-6 like z-2"><i class="bi bi-heart"></i> Me gusta</button> 
                                                        <button class="btn text-primary col-6 like z-2"><i class="bi bi-chat-left"></i> Comentar </button>`
      },

      error: function (xhr, errmsg, err) {

      }
    });
  })

/* ajax para dar like comentario*/
$(document).on('click', '#likecoment', function (e) {
    e.preventDefault();
    let a = window.data

    $.ajax({
      type: 'POST',
      url: a.url_like_coment,
      data: {
        
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        action: 'post'
      },
      success: function (json) {
        document.getElementById("like_count").textContent = json['result']
        document.getElementById("divlike").innerHTML  = `<button id="dislike" class="btn text-primary  border-secondary col-6 like z-2"><i class="bi bi-heart"></i> No Me gusta</button>
                                                        <button class="btn text-primary col-6 like z-2"><i class="bi bi-chat-left"></i> Comentar </button>`
      },

      error: function (xhr, errmsg, err) {

      }
    });
  })