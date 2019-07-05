from db_orm import db_orm

class User(db_orm.Model):
    __tablename__ = 'user'
    __table_args__ = {
        'autoload': True,
        'autoload_with': db_orm.engine
    }


class Tickets(db_orm.Model):
    __tablename__ = 'tickets'
    __table_args__ = {
        'autoload': True,
        'autoload_with': db_orm.engine
    }
