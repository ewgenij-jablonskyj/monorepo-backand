import os
from flask import Flask
import graphene
from flask_graphql import GraphQLView
from dotenv import load_dotenv
import pymysql
from pymysql.cursors import DictCursor

class Query(graphene.ObjectType):
    hello = graphene.String(name=graphene.String(default_value="default"))

    def resolve_hello(self, info, name):
        return f"Witaj, {name}!"

schema = graphene.Schema(query=Query)

app = Flask(__name__)

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True
    )
)

load_dotenv()

def get_db_connection():
    return pymysql.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        port=int(os.getenv('DB_PORT', 3306)),
        cursorclass=DictCursor
    )


@app.route('/test-db')
def test_db():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION();")
            db_version = cursor.fetchone()
        connection.close()
        return {"status": "Sukces!", "wersja_bazy": db_version}
    except Exception as e:
        return {"status": "Błąd połączenia", "szczegóły": str(e)}, 500


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5001)