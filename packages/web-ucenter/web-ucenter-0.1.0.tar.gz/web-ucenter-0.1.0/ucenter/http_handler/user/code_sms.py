from tweb.error_exception import ErrException, ERROR
from tweb import base_handler
from ucenter.services import verify_code, user_indicate
from tornado import gen

from ucenter.services.code import send_sms_code


class CodeSmsGenerating(base_handler.BaseHandler):
    @gen.coroutine
    def get(self):
        value = self.get_argument('indicator')

        if not user_indicate.is_mobile(value):
            # 无效的手机号码
            raise ErrException(ERROR.E40004)

        (code, ret) = verify_code.gen_code('mobile', value, 60)
        yield send_sms_code(business_id=ret.get('code_token'), mobile=value, code=code, tpl_type=0)

        self.write(ret)
