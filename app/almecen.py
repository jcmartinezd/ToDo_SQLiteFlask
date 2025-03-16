# app/almecen.py
from datetime import datetime
from .db import db  # Usa la instancia única

class Pendientes(db.Model):
    __tablename__ = 'pendientes'
    id = db.Column(db.Integer(), primary_key=True)
    id_usuario = db.Column(db.Integer())
    tarea = db.Column(db.String())
    creacion = db.Column(db.DateTime(), default=datetime.now)
    hecho = db.Column(db.Boolean(False))

    def __init__(self, usuario: object, tarea: str) -> None:
        if not tarea:
            return
        try:
            self.id_usuario = usuario.id
            self.tarea = tarea
        except:
            return

    @staticmethod
    def obtenerTareas(lista_id: list) -> list:
        lista = []
        for id in lista_id:
            pendiente = db.session.query(Pendientes).get(id)
            if pendiente:
                lista.append((pendiente.tarea, pendiente.hecho, id))
        return lista

    @staticmethod
    def __crear__(app) -> None:
        # Ya se ha llamado a db.init_app(app) en usuarios.__crear__
        # Así que solo es necesario crear las tablas
        with app.app_context():
            db.create_all()

    @staticmethod
    def agregarPendiente(usuario: object, pendiente: str) -> int or None:
        if type(pendiente) != str:
            return None
        tareaPendiente = Pendientes(usuario, pendiente)
        db.session.add(tareaPendiente)
        db.session.commit()
        return tareaPendiente.id

    @staticmethod
    def eliminar(id: int) -> bool:
        if type(id) != int or id <= 0:
            return False
        db.session.query(Pendientes).filter(Pendientes.id == id).delete()
        db.session.commit()
        return True

    @staticmethod
    def cambiarEstado(usuario: object, id: int) -> None:
        tarea = db.session.query(Pendientes).get(id)
        if tarea and tarea.id_usuario == usuario.id:
            tarea.hecho = not tarea.hecho
            db.session.add(tarea)
            db.session.commit()

    @staticmethod
    def eliminarPorUsuario(usuario: object) -> None:
        usuario.cargarIdsDePendientes()
        for id in usuario.ids_tareas:
            db.session.query(Pendientes).filter(Pendientes.id == id).delete()
        if len(usuario.ids_tareas) > 0:
            db.session.commit()
