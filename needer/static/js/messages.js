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
        let request_user = $('.messages-wrapper').attr('request_user')
      

        let data = {
            'message': message,
            'sent_by': USER_ID,
            'send_to': send_to,
            'thread_id': thread_id,
            'request_user':request_user
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
    let time = data['time']
    newMessage(message, sent_by_id, thread_id, time)
}




function newMessage(message, sent_by_id, thread_id, time) {
	if ($.trim(message) === '') {
		return false;
	}
	let message_element;
	let chat_id = 'chat_' + thread_id
    let imag = document.getElementById('image_profile').src;


	if(sent_by_id == USER_ID){
	    message_element = `
        <div class="col-12 row mx-0 d-flex justify-content-end mb-3">
            <div class=" text-wrap text-break mx-0 px-3 py-2 float-end respuesta
                        rounded-4 mensaje py-2 text-start d-inline-flex justify-content-end  align-items-center">
        
                    <div class="text-white">
                        ${message}
                    </div>
        
                
                
                        
            </div>
            <small class="my-0 hora text-end mx-0 px-0 fw-light d-flex justify-content-end text-wrap text-break">${time}</small> 
        </div>
	    `

    }
	else{
	    message_element = `
        <div class="col-12 row mx-0 container mensaje-container d-flex justify-content-start mb-3">
            <div class=" text-wrap text-break mx-0 px-0 py-2 float-end 
            rounded-4 mensaje py-2 text-start d-inline-flex justify-content-start  align-items-center">
                <a href="#" class="text-center me-0 col-3 px-0"">
                    
                    <img
                        class="rounded-circle d-lg-block d-none img-fluid my-auto img-perfil mx-0"
                        alt="profile"
                        src="${imag}"
                        data-holder-rendered="true"
                    >
                </a>
                <div class=" text-wrap text-break mx-0 px-3 py-2 float-end mensajes
                rounded-4 py-2 text-start d-inline-flex justify-content-start col-9 align-items-center">
            
                        <div class="text-white">
                            ${message}
                        </div>
            
                    
                    
                            
                </div>
            </div>
            <small class="my-0 hora text-end mx-0 px-0 fw-light d-flex justify-content-start text-wrap text-break">${time}</small> 
        </div>
        `


    }

    let message_body = $('.messages-wrapper[chat-id="' + chat_id + '"] .msg_card_body')
	message_body.append($(message_element))
    document.getElementById('scroll').scrollTop = 9999999;
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


