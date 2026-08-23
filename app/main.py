from aiohttp import web
from app.routes.transactions import routes as transaction_routes


def create_app() -> web.Application:
    app = web.Application()
    app.add_routes(transaction_routes)
    
    return app


if __name__ == '__main__':
    app = create_app()
    web.run_app(app, host='0.0.0.0', port=8080)