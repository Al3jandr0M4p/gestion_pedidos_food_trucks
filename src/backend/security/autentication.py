"""
Módulo de autenticación para proteger rutas en Flask.

Este módulo define el decorador `authentication_required` que verifica si un usuario
está autenticado antes de acceder a una ruta protegida.

Ejemplo
-------
>>> from flask import Flask
>>> from src.backend.python.security.autenticacion import authentication_required
>>> @app.route('/protected')
>>> @authentication_required
>>> def protected():
>>>     return "Esta es una ruta protegida"
"""

from flask import redirect, url_for, flash, session, request
from functools import wraps

def authentication_required(f, session_key='user_id'):
    """
    Decorador que verifica si el usuario está autenticado antes de acceder a una ruta.

    Si el usuario no está autenticado, será redirigido a la página de inicio de sesión
    y luego devuelto a la URL original después de autenticarse.

    Parámetros
    ----------
    f : function
        Función de vista que se desea proteger.
    session_key : str, opcional
        Clave en la sesión que indica si el usuario ha iniciado sesión (por defecto, 'user_id').

    Returns
    -------
    function
        Función de vista protegida.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        """
        Función envoltura que maneja la lógica de autenticación.

        Si el usuario no está autenticado, lo redirige a la página de inicio de sesión con
        la URL original como parámetro `next`, permitiendo regresar después de autenticarse.

        Parámetros
        ----------
        *args : cualquier
            Argumentos posicionales para la función original.
        **kwargs : cualquier
            Argumentos keyword para la función original.

        Returns
        -------
        Response
            Redirección a la página de login si no está autenticado, o ejecución de la función original.
        """
        if session_key not in session:
            flash('Necesitas estar autenticado para acceder a esta ruta', 'warning')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return wrapper