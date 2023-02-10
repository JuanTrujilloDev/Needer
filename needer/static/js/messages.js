let input_message = $('#input-message')
let message_body = $('.msg_card_body')
let send_message_form = $('#send-message-form')
const USER_ID = $('#logged-in-user').val()



let loc = window.location
let wsStart = 'ws://'

if(loc.protocol === 'https') {
    wsStart = 'wss://'
}
let endpoint = wsStart + loc.host + loc.pathname

var socket = new WebSocket(endpoint)

socket.onopen = async function(e){
    /* console.log('open', e) */
    send_message_form.on('submit', function (e){
        e.preventDefault()
        let message = input_message.val()
        let send_to = get_active_other_user_id()
        let thread_id = get_active_thread_id()

        let data = {
            'message': message,
            'sent_by': USER_ID,
            'send_to': send_to,
            'thread_id': thread_id
        }
        data = JSON.stringify(data)
        socket.send(data)
        $(this)[0].reset()
    })
}

socket.onmessage = async function(e){
    /* console.log('message', e) */
    let data = JSON.parse(e.data)
    let message = data['message']
    let sent_by_id = data['sent_by']
    let thread_id = data['thread_id']
    newMessage(message, sent_by_id, thread_id)
}

socket.onerror = async function(e){
    console.log('error', e)
}

socket.onclose = async function(e){
    console.log('close', e)
}


function newMessage(message, sent_by_id, thread_id) {
	if ($.trim(message) === '') {
		return false;
	}
	let message_element;
	let chat_id = 'chat_' + thread_id
    let imag = document.getElementById('image_profile').src;

	if(sent_by_id == USER_ID){
	    message_element = `
        <div class="row d-flex col-9 m-2 mx-0 px-0 py-0 float-end justify-content-end align-items-center">
            <div class="col-12 col-md-12 mx-2 rounded-4 py-0 justify-content-start respuesta">
                <p class="mb-0 mb-lg-0 mb-xl-0 mb-md-0 mb-sm-2 my-0 py-0 text-start nombreuser ">
					${message}
                </p>
			</div>
		</div>
	    `

    }
	else{
	    message_element = `
        <div class="row d-flex col-12 m-2 mx-0 px-0 py-0 justify-content-start align-items-center">
            <div class="col-3 col-md-1 d-flex pe-0 py-2 justify-content-start">
                <a href="#" class="text-center">
                <img
                    class="rounded-circle d-lg-block d-none img-fluid my-auto img-perfil"
                    alt="profile"
                    src="${imag}"
                    data-holder-rendered="true"
            >   
                </a>
                
              </div>
              <div class="col-9 mx-2 rounded-4 py-0 justify-content-start mensajes">
                <p class="mb-0 mb-lg-0 mb-xl-0 mb-md-0 mb-sm-2 my-0 py-0 text-break text-start nombreuser">
                    ${message}
                </p>
              </div>
              
        </div>
        `


    }

    let message_body = $('.messages-wrapper[chat-id="' + chat_id + '"] .msg_card_body')
	message_body.append($(message_element))
    message_body.animate({
        scrollTop: $(document).height()
    }, 100);
	input_message.val(null);
}



function get_active_other_user_id(){
    let other_user_id = $('.messages-wrapper').attr('other-user-id')
    other_user_id = $.trim(other_user_id)
    return other_user_id
}

function get_active_thread_id(){
    let chat_id = $('.messages-wrapper').attr('chat-id')
    let thread_id = chat_id.replace('chat_', '')
    return thread_id
}


