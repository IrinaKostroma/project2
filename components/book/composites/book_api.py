from wsgiref.simple_server import make_server

from kombu import Connection
from sqlalchemy import create_engine

from classic.messaging_kombu import KombuPublisher
from classic.sql_storage import TransactionContext

from book.application.services import BookService
from book.adapters import database, book_api, message_bus


class Settings:
    db = database.Settings()
    message_bus = message_bus.Settings()
    book_api = book_api.Settings()


class DB:
    engine = create_engine(Settings.db.DB_URL)
    database.metadata.create_all(engine)

    context = TransactionContext(bind=engine)

    books_repo = database.repositories.BooksRepo(context=context)


class MessageBus:
    connection = Connection(Settings.message_bus.BROKER_URL)
    message_bus.broker_scheme.declare(connection)

    publisher = KombuPublisher(
        connection=connection,
        scheme=message_bus.broker_scheme,
    )


class Application:

    book_service = BookService(books_repo=DB.books_repo,
                               publisher=MessageBus.publisher)

    is_dev_mode = Settings.book_api.IS_DEV_MODE
    allow_origins = Settings.book_api.ALLOW_ORIGINS


# class Aspects:
#     services.join_points.join(DB.context)
#     user_api.join_points.join(DB.context)


app = book_api.create_app(
    books=Application.book_service,
)

# with make_server('', 8000, app) as httpd:
#     print(f'Server running on http://localhost:{httpd.server_port} ...')
#     httpd.serve_forever()
