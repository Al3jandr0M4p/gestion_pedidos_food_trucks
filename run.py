"""
Modulo principal para ejecutar la clase principal FoodTrucks.

Este script inicializa y ejecuta la app.
"""

from src.backend.python.app import FoodTrucks

if __name__ == "__main__":
    app = FoodTrucks()
    app.run_app()