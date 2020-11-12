class Plants:

    def __init__(self, facility_code, plt_state_code, plt_name,  opr_name, opr_code):
        self.facility_code = facility_code
        self.plt_state_code = plt_state_code
        self.plt_name = plt_name
        self.opr_name = opr_name
        self.opr_code = opr_code

    def __repr__(self):
        return '<Post %r>' % self.plt_name


