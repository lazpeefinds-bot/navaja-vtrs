from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Position(db.Model):
    __tablename__ = 'positions'

    posID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    posName = db.Column(db.String(100), nullable=False)
    numOfPositions = db.Column(db.Integer, nullable=False, default=1)
    posStat = db.Column(db.String(10), nullable=False, default='open')

    # Relationships
    candidates = db.relationship('Candidate', backref='position', lazy=True, cascade='all, delete-orphan')
    votes = db.relationship('Vote', backref='position', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Position {self.posName}>'


class Voter(db.Model):
    __tablename__ = 'voters'

    voterID = db.Column(db.String(50), primary_key=True)
    voterPass = db.Column(db.String(255), nullable=False)
    voterFName = db.Column(db.String(100), nullable=False)
    voterMName = db.Column(db.String(100))
    voterLName = db.Column(db.String(100), nullable=False)
    voterStat = db.Column(db.String(10), nullable=False, default='active')
    voted = db.Column(db.String(1), nullable=False, default='N')

    # Relationships
    votes = db.relationship('Vote', backref='voter', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Voter {self.voterID}>'


class Candidate(db.Model):
    __tablename__ = 'candidates'

    candID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    candFName = db.Column(db.String(100), nullable=False)
    candLName = db.Column(db.String(100), nullable=False)
    posID = db.Column(db.Integer, db.ForeignKey('positions.posID'), nullable=False)
    candStat = db.Column(db.String(10), nullable=False, default='active')

    # Relationships
    votes = db.relationship('Vote', backref='candidate', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Candidate {self.candFName} {self.candLName}>'


class Vote(db.Model):
    __tablename__ = 'votes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    posID = db.Column(db.Integer, db.ForeignKey('positions.posID'), nullable=False)
    voterID = db.Column(db.String(50), db.ForeignKey('voters.voterID'), nullable=False)
    candID = db.Column(db.Integer, db.ForeignKey('candidates.candID'), nullable=False)

    def __repr__(self):
        return f'<Vote voter:{self.voterID} candidate:{self.candID}>'






