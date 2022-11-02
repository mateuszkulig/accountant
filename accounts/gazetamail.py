from acc import Browser

class GazetaMail(Browser):
    """Mail account for poczta.gazeta.pl"""
    def __init__(self):
        super(GazetaMail, self).__init__(adp=False)

    def __str__(self):
        return "gazeta mail account"