from flask import Flask, request, Response, render_template
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages import VideoMessage
from viberbot.api.messages.text_message import TextMessage
import logging

from viberbot.api.viber_requests import ViberConversationStartedRequest
from viberbot.api.viber_requests import ViberFailedRequest
from viberbot.api.viber_requests import ViberMessageRequest
from viberbot.api.viber_requests import ViberSubscribedRequest
from viberbot.api.viber_requests import ViberUnsubscribedRequest
from my_config_utilites import *


app = Flask(__name__)
viber = Api(BotConfiguration(
    name=NAME_BOT,
    avatar=AVATAR_BOT,
    auth_token=AUTH_TOKEN
))
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

my_config: Any = MyConfig()

@app.route('/', methods=['POST'])
def incoming():

    logger.debug("received request. post data: {0}".format(request.get_data()))
    # # every viber message is signed, you can verify the signature using this method
    # if not viber.verify_signature(request.get_data(), request.headers.get('X-Viber-Content-Signature')):
    #     print(viber.verify_signature(request.get_data(), request.headers.get('X-Viber-Content-Signature')))
    #     return Response(status=403)

    # this library supplies a simple way to receive a request object
    viber_request = viber.parse_request(request.get_data().decode('utf8'))
    if isinstance(viber_request, ViberMessageRequest):
        message = viber_request.message
        # прикручиваем обработку входящего мессаджа
        if message['type'] == 'text':
            incoming_text = message['text']
            incoming_id = message['receiver']
            output_ids, output_msg = incoming_parsing(incoming_id, incoming_text)
            for receiver_id in output_ids:
                # viber_request.sender.id = receiver_id
                # viber.send_messages(viber_request.sender.id, [
                #     message, TextMessage(text=str(viber_request.sender.id))
                # ])
                viber.send_messages(receiver_id, [
                    TextMessage(text=output_msg)
                ])
            my_config = output_my_config
        else:
            # если не текст, то просто эхо отвечает
            viber.send_messages(viber_request.sender.id, [
                   message, TextMessage(text=str(viber_request.sender.id))
                ])
    elif isinstance(viber_request, ViberSubscribedRequest):
        viber.send_messages(viber_request.get_user.id, [
                TextMessage(text="thanks for subscribing!")
            ])
    elif isinstance(viber_request, ViberFailedRequest):
        logger.warning("client failed receiving message. failure: {0}".format(viber_request))

    return Response(status=200)





if __name__ == "__main__":
    context = ('server.crt', 'server.key')
    app.run(host='0.0.0.0', port=443, debug=True)

    viber.set_webhook('https://volleyball78bot.onrender.com:443/')


