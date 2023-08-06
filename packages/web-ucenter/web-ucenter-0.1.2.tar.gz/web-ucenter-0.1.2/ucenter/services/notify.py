from tweb.error_exception import ErrException, ERROR

from ucenter.services import ctrl_user
from ucenter.services.code import send_message
from ucenter.services.email import send_email

from asyncio import get_event_loop


async def send_notification_sync(uid, msg, types):
    args = uid, msg, types
    return await get_event_loop().run_in_executor(None, send_notification, *args)


def send_notification(uid, msg, types=['email', 'sms']):
    """
    发送通知
    :param uid: 用户 id
    :param msg: 通知内容 包含 subject: '标题', message: '内容'
    :param types: 通知形式 ['email', 'sms'] 默认为 邮件、短信同时发送
    :return:
    """
    print('send_notification', '{}- {}'.format(msg.get('subject'), msg.get('message')))

    user = ctrl_user.get(uid)

    if user is None:
        raise ErrException(ERROR.E40101)

    mobile = user.get('mobile')
    email = user.get('email')

    if mobile is not None and 'sms' in types:
        send_message(mobile, '{} - {}'.format(msg.get('subject'), msg.get('message')))

    if email is not None and 'email' in types:
        send_email(email, msg)
