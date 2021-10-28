from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    nombre = db.Column(db.String(100))
    direccion = db.Column(db.String(100))
    telefono = db.Column(db.String(50))
    rol_id = db.Column(db.Integer)
    estado = db.Column(db.String(1))

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.activate

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

class Rol(UserMixin, db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    rol	= db.Column(db.String(100))

class Proveedor(UserMixin, db.Model):
    __tablename__ = 'proveedores'
    id = db.Column(db.Integer, primary_key=True)
    nit	= db.Column(db.String(20))
    razonsocial	= db.Column(db.String(100))
    ciudad_id = db.Column(db.Integer)
    direccion = db.Column(db.String(100))
    telefono = db.Column(db.String(50))
    contacto = db.Column(db.String(50))
    user_id_updated = db.Column(db.Integer)
    user_id_created = db.Column(db.Integer)
    estado = db.Column(db.String(1))

class Ciudad(UserMixin, db.Model):
    __tablename__ = 'ciudades'
    id = db.Column(db.Integer, primary_key=True)
    padre_id = db.Column(db.Integer)
    tipo = db.Column(db.Integer)
    descripcion	= db.Column(db.String(100))

class Producto(UserMixin, db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    nombre	= db.Column(db.String(100))
    unidad_id = db.Column(db.Integer)
    precio = db.Column(db.Float)
    cantidad_min = db.Column(db.Float)
    cantidad_disp = db.Column(db.Float)
    proveedor_id = db.Column(db.Integer)
    user_id_updated = db.Column(db.Integer)
    user_id_created = db.Column(db.Integer)
    estado = db.Column(db.String(1))

class Unidad(UserMixin, db.Model):
    __tablename__ = 'unidades'
    id = db.Column(db.Integer, primary_key=True)
    unidad = db.Column(db.String(100))
    und = db.Column(db.String(10))