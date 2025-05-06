"""
Módulo de autenticación para proteger rutas en Flask.

Este módulo define el decorador `authentication_required` que verifica si un usuario
está autenticado antes de acceder a una ruta protegida.
"""

from flask import redirect, url_for, flash, session, request
from functools import wraps

def authentication_required(f, session_key='user_id'):
    """
    Decorador que verifica si el usuario está autenticado antes de acceder a una ruta.

    Si el usuario no está autenticado, será redirigido a la página de inicio de sesión
    y luego devuelto a la URL original después de autenticarse.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        """
        Función envoltura que maneja la lógica de autenticación.

        Si el usuario no está autenticado, lo redirige a la página de inicio de sesión con
        la URL original como parámetro `next`, permitiendo regresar después de autenticarse.
        """
        if session_key not in session:
            flash('Necesitas estar autenticado para acceder a esta ruta', 'warning')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return wrapper