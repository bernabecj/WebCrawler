from website import create_app, routes

app = create_app(debug=True)
routes.register_routes_views.register_routes(app)

if __name__ == "__main__":
    """
    Corremos el servidor en el puerto 5200 y debug = True para que el servidor
    se reinicie cuando se hagan cambios

    All hosts: host="0.0.0.0", port=5200
    Open your browser and type: 127.0.0.1:5200
    """
    app.run(debug=True, host="0.0.0.0", port=5200)
