from website.main import views  # Import views from your main blueprint


def register_routes(app):
    # Register the class-based view 'Index' at the root URL '/'
    app.add_url_rule("/", view_func=views.Index.as_view("index"))
