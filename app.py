from flask import Flask
import graphene
from flask_graphql import GraphQLView

class Query(graphene.ObjectType):
    hello = graphene.String(name=graphene.String(default_value="default"))

    def resolve_hello(self, info, name):
        return f"Witaj, {name}!"

schema = graphene.Schema(query=Query)

app = Flask(__name__)

app.add_url_rule(
    '/',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True
    )
)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5001)