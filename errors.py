class InvalidRequest(Exception):

    def __init__(self, err_msg, status_code=400, payload=None):
        super().__init__()
        self.err_msg = err_msg
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv["msg"] = self.err_msg
        return rv
