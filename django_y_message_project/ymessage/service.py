import traceback


all_handlers = {}


def add_handler(type, handler):
    handles_of_type = all_handlers.get(type, [])
    handles_of_type.append(handler)
    all_handlers[type] = handles_of_type


def message_handler(type):
    def add_handler_of_type(func):
        add_handler(type, func)
        return func 
    return add_handler_of_type


def compose(type, id, content=None):
    from .models import Message
    return Message.objects.create(type=type,
                                  id=id,
                                  content=content,
                                  status=Message.STATUS_QUEUING)


class NoMoreMessages(Exception):
    pass


def get_next_message_for_processing(types):
    import ool
    from .models import Message

    message = None
    while message is None:
        message = Message.objects.filter(status=Message.STATUS_QUEUING, type__in=types).order_by('create_at').first()
        if message is not None:
            try:
                message.status = Message.STATUS_PROCESSING
                message.save()
            except ool.ConcurrentUpdate:
                message = None
        else:
            raise NoMoreMessages()
    return message


def handle_message():
    
    message = get_next_message_for_processing(all_handlers.keys())

    try:
        handlers_for_type = all_handlers.get(message.type, [])
        for handler in handlers_for_type:
            handler(message)
            if not message.is_processing():
                break
        
        if message.is_processing():
            message.no_handler()
    except Exception as e:
        message.catch_exception({
            'trace': traceback.format_exc()
        })
        
