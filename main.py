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
        if message._message_type == 'text':
            incoming_text = message._text
            incoming_id = viber_request.sender.id
            output_ids, output_msg = incoming_parsing(incoming_id, incoming_text)
            for output_id in output_ids:
                viber.send_messages(output_id, [
                    TextMessage(text=output_msg)
                ])
            if END_COUNTDOWN:
                output_ids, output_msg = incoming_parsing('', '')
                for output_id in output_ids:
                    viber.send_messages(output_id, [
                        TextMessage(text=output_msg)
                    ])
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



'''
{"event":"message",
 "timestamp":1687200046080,
 "chat_hostname":"SN-CALLBACK-04_",
 "message_token":5851650804048782321,
 "sender":{"id":"5h2COTj83ZE6IAsIcTEVGw==",
           "name":"\xd0\x94\xd0\x9a",
           "avatar":"https://media-direct.cdn.viber.com/download_photo?dlid=sRvVjYPcpzjFDu5Qbvqox1MFElVrX4MEnRDmf2KRRaoIIOHf4Z9lu2S1eZ8y5WNCg25FRLmTOl4g_7gv7kiRKLqjSFQ4YrG8JTbmnCo8p2_Go5fSBzHsei0hl_QRFDv5au2VFw&fltp=jpg&imsz=0000",
           "language":"ru-RU",
           "country":"RU",
           "api_version":10},
 "message":{"text":"\xf0\x9f\x99\x84",
            "type":"text"},
 "silent":false}
 '''