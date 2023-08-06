

class AGIResponse:
    content = ''
    verbose = 6

    def __init__(self, status=200, body=b'', message=None, verbose=None):
        self._status = status
        self.body = body or self.content.encode()
        self.message = message
        self.verbose = verbose or self.verbose

    @property
    def status(self):
        return self._status

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, body):
        self._body = body

    @property
    def body_length(self):
        return len(self.body)
