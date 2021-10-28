from flask import *
from flask_login import login_required, current_user, login_user, logout_user
from .models import Proveedor, Ciudad, Producto, Unidad, Rol, User
from . import db

main = Blueprint('main', __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/dashboard", methods=['GET'])
@login_required
def dashboard():
    rol_user = Rol.query.filter_by(id=current_user.rol_id).first()
    return render_template("dashboard.html", name=current_user.nombre, rol=current_user.rol_id,rol_name=rol_user.rol)

# ------------ USUARIO ------------
@main.route("/usuario")
@login_required
def usuario():
    result = db.session.query(User.id, User.nombre, User.email, User.direccion, User.telefono, User.rol_id, User.estado,
                                Rol.rol).join(Rol, User.rol_id == Rol.id).all()
    rol_user = Rol.query.filter_by(id=current_user.rol_id).first()                            
    rol = db.session.query(Rol.id, Rol.rol).all()
    return render_template("usuario.html", name=current_user.nombre, rol=current_user.rol_id, result=result, rol_result= rol, rol_name=rol_user.rol)

@main.route("/usuario/delete/<id>", methods=['PACTH'])
@login_required
def usuario_delete(id):
    print(id)
    update_user = User.query.filter_by(id=id).update(
        dict(estado='I'))
    db.session.commit()
    return jsonify(msg='Inactivación exitosa.', status=200, icon='success')

@main.route("/usuario/update/<id>", methods=['PUT'])
@login_required
def usuario_update(id):
    u_email = request.form.get('u_email')
    u_nombre = request.form.get('u_nombre')
    u_direccion = request.form.get('u_direccion')
    u_telefono = request.form.get('u_telefono')
    u_rol_id = request.form.get('u_rol')
    update_usuario = User.query.filter_by(id=id).update(
        dict(email=u_email,nombre=u_nombre,direccion=u_direccion,telefono=u_telefono,rol_id=u_rol_id))
    db.session.commit()
    return jsonify(msg='Grabación exitosa.', status=200, icon='success')


# ------------ PROVEEDORES ------------
@main.route("/proveedor")
@login_required
def proveedor():
    result = db.session.query(Proveedor.id, Proveedor.nit,
                              Proveedor.razonsocial, Proveedor.direccion,
                              Proveedor.telefono, Proveedor.ciudad_id, Proveedor.contacto,
                              Proveedor.estado, Ciudad.descripcion).join(Ciudad, Proveedor.ciudad_id == Ciudad.id).all()
    rol_user = Rol.query.filter_by(id=current_user.rol_id).first()
    ciudad = db.session.query(Ciudad.id, Ciudad.descripcion).filter(
        Ciudad.tipo == 3).all()

    return render_template("proveedor.html", name=current_user.nombre, rol=current_user.rol_id, result=result, ciudad=ciudad, rol_name=rol_user.rol)


@main.route("/proveedor/update/<id>", methods=['PUT'])
@login_required
def proveedor_update(id):
    u_nit = request.form.get('u_nit')
    u_nombre = request.form.get('u_nombre')
    u_direccion = request.form.get('u_direccion')
    u_telefono = request.form.get('u_telefono')
    u_ciudad = request.form.get('u_ciudad')
    u_contacto = request.form.get('u_contacto')

    update_proveedor = Proveedor.query.filter_by(id=id).update(
        dict(nit=u_nit, razonsocial=u_nombre, direccion=u_direccion, telefono=u_telefono, ciudad_id=u_ciudad, contacto=u_contacto, user_id_updated=current_user.id))
    db.session.commit()

    return jsonify(msg='Grabación exitosa.', status=200, icon='success')


@main.route("/proveedor/create", methods=['POST'])
@login_required
def proveedor_create():
    c_nit = request.form.get('c_nit')
    c_nombre = request.form.get('c_nombre')
    c_direccion = request.form.get('c_direccion')
    c_telefono = request.form.get('c_telefono')
    c_ciudad = request.form.get('c_ciudad')
    c_contacto = request.form.get('c_contacto')

    new_proveedor = Proveedor(nit=c_nit, razonsocial=c_nombre, direccion=c_direccion,
                              telefono=c_telefono, ciudad_id=c_ciudad, contacto=c_contacto, estado='A',
                              user_id_created=current_user.id, user_id_updated=current_user.id)

    db.session.add(new_proveedor)
    db.session.commit()

    return jsonify(msg='Grabación exitosa.', status=200, icon='success')


@main.route("/proveedor/delete/<id>", methods=['PACTH'])
@login_required
def proveedor_delete(id):
    print(id)
    update_proveedor = Proveedor.query.filter_by(id=id).update(
        dict(estado='I', user_id_updated=current_user.id))
    db.session.commit()

    return jsonify(msg='Inactivación exitosa.', status=200, icon='success')

# ------------ PRODUCTOS ------------


@main.route("/producto")
@login_required
def producto():
    result = db.session.query(Producto.id, Producto.nombre, Producto.unidad_id,Producto.precio,
                Producto.cantidad_min,Producto.cantidad_disp,Producto.proveedor_id,Producto.estado,
                Proveedor.razonsocial,Unidad.und,Unidad.unidad).join(Proveedor, Producto.proveedor_id == Proveedor.id).join(Unidad, Producto.unidad_id == Unidad.id).all()

    unidad = db.session.query(Unidad.id, Unidad.unidad).all()
    proveedor = db.session.query(Proveedor.id, Proveedor.razonsocial).all()
    rol_user = Rol.query.filter_by(id=current_user.rol_id).first()

    return render_template("producto.html", name=current_user.nombre, rol=current_user.rol_id, result=result, proveedor=proveedor, unidad=unidad, rol_name=rol_user.rol)


@main.route("/producto/update/<id>", methods=['PUT'])
@login_required
def producto_update(id):
    u_id = request.form.get('u_id')
    u_nombre = request.form.get('u_nombre')
    u_unidad_id = request.form.get('u_unidad_id')
    u_precio = request.form.get('u_precio')
    u_cantidad_min = request.form.get('u_cantidad_min')
    u_cantidad_disp = request.form.get('u_cantidad_disp')
    u_proveedor_id = request.form.get('u_proveedor_id')

    update_producto = Producto.query.filter_by(id=id).update(
        dict(nombre=u_nombre, unidad_id=u_unidad_id, precio=u_precio, cantidad_min=u_cantidad_min, 
        cantidad_disp=u_cantidad_disp, proveedor_id=u_proveedor_id, user_id_updated=current_user.id))
    db.session.commit()

    return jsonify(msg='Grabación exitosa.', status=200, icon='success')


@main.route("/producto/create", methods=['POST'])
@login_required
def producto_create():
    c_id = request.form.get('c_id')
    c_nombre = request.form.get('c_nombre')
    c_unidad_id = request.form.get('c_unidad_id')
    c_precio = request.form.get('c_precio')
    c_cantidad_min = request.form.get('c_cantidad_min')
    c_cantidad_disp = request.form.get('c_cantidad_disp')
    c_proveedor_id = request.form.get('c_proveedor_id')

    new_producto = Producto(nombre=c_nombre, unidad_id=c_unidad_id, precio=c_precio, cantidad_min=c_cantidad_min,
                            cantidad_disp=c_cantidad_disp, proveedor_id=c_proveedor_id, estado='A', user_id_created=current_user.id, user_id_updated=current_user.id)
    db.session.add(new_producto)
    db.session.commit()

    return jsonify(msg='Grabación exitosa.', status=200, icon='success')


@main.route("/producto/delete/<id>", methods=['PACTH'])
@login_required
def producto_delete(id):
    print(id)
    update_producto = Producto.query.filter_by(id=id).update(
        dict(estado='I', user_id_updated=current_user.id))
    db.session.commit()

    return jsonify(msg='Inactivación exitosa.', status=200, icon='success')
