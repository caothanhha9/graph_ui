from knowledge_network.utility.service import gen_key


class Login(object):
    def __init__(self):
        """
        Create default values
        :return:
        """
        self.status = False
        self.token = None
        self.default_id = 'xdm'
        self.default_pass = 'iloveyou'
        self.default_token = '123456789101112131415'
        self.user = None
        self.password = None

    def validate(self, _acc_id, _acc_pass):
        """
        Check if account match with db
        :param _acc_id: user account
        :param _acc_pass: user password
        :return: reassign status and token
        """
        if (_acc_id == self.default_id) and (_acc_pass == self.default_pass):
            user_status = True
            if user_status:
                self.status = True
                self.token = gen_key.id_generator()
                self.user = _acc_id
                self.password = _acc_pass

    def security_check(self, _acc_id, _acc_tok):
        """
        check to authenticate the user
        :param _acc_id: user account
        :param _acc_tok: token sent from client
        :return: True or False
        """
        check = False
        if (_acc_id == self.default_id) and (_acc_tok == self.default_token):
            check = True
        return check


