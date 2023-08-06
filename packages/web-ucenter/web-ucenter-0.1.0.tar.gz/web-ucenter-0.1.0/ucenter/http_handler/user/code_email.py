from tweb.error_exception import ErrException, ERROR
from tweb import base_handler
from ucenter.services import verify_code, user_indicate
from tornado import gen

from ucenter.services.code import send_email_code_sync


class CodeEmailGenerating(base_handler.BaseHandler):
    @gen.coroutine
    def get(self):
        value = self.get_argument('indicator')

        if not user_indicate.is_email(value):
            # 无效的email地址
            raise ErrException(ERROR.E40003)

        (code, ret) = verify_code.gen_code('email', value, 300)

        yield send_email_code_sync(email=value, code=code)

        self.write(ret)
