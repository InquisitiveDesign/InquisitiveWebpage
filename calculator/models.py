from calculator import db


class Infoform(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    beamlength = db.Column(db.Float, nullable=False)
    supportnum = db.Column(db.Integer, nullable=False)
    loadnum = db.Column(db.Integer, nullable=False)

    def __init__(self, beamlength, supportnum, loadnum):
        self.beamlength = beamlength
        self.supportnum = supportnum
        self.loadnum = loadnum

    def __repr__(self):
        return f'Beam length {self.beamlength}, number of supports {self.supportnum},number of loads {self.loadnum} saved to database'

class Dtform(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    supportloc = db.Column(db.Float, nullable=False)
    supporttype = db.Column(db.String, nullable=False)
    supportdirec = db.Column(db.String, nullable=False)
    loadloc = db.Column(db.Float, nullable=False)
    loadtype = db.Column(db.String, nullable=False)
    loaddirec = db.Column(db.String, nullable=False)
    loadvalue = db.Column(db.Float, nullable=False)

    def __init__(self, 
                 supportloc, supporttype, supportdirec,
                 loadloc, loadtype, loaddirec, loadvalue):
        self.supportloc = supportloc
        self.supporttype = supporttype
        self.supportdirec = supportdirec
        self.loadloc = loadloc
        self.loadtype = loadtype
        self.loaddirec = loaddirec
        self.loadvalue = loadvalue

    def __repr__(self):
        return f'Support location {self.supportloc}, support type {self.supporttype},support direction {self.supportdirec} with load location {self.loadloc}, load type {self.loadtype}, load direction {self.loaddirec}, loadvalue {self.loadvalue}  saved to database'
