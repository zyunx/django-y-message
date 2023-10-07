
import ymessage

SAY_HELLO = 'SAY_HELLO'

@ymessage.message_handler(type=SAY_HELLO)
def process_SAY_HELLO(message):
    print(f"To process message {message.id}")
    # begin call other service api
    print(f"Hello, {message.content['name']}!")
    # end call other service api
    print(f"Message {message.id} processed.")

    message.sent()
