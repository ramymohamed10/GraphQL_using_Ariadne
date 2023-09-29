# Importing necessary modules for setting up GraphQL with Flask
from ariadne import QueryType, MutationType, make_executable_schema, load_schema_from_path
from graphql_server.flask import GraphQLView
from flask import Flask

# Initializing the Flask app
app = Flask(__name__)

# Sample data: this represents a list of tasks stored in memory
tasks = [
    {'id': 1, 'title': 'Learn Flask', 'done': False},
    {'id': 2, 'title': 'Develop REST API', 'done': False}
]

# Loading the GraphQL schema from a file
type_defs = load_schema_from_path("schema.graphql")

# Defining query and mutation types for the GraphQL schema
query = QueryType()
mutation = MutationType()

# Resolver function to fetch all tasks
@query.field("tasks")
def resolve_tasks(*_):
    return tasks

# Resolver function to fetch a specific task based on its ID
@query.field("task")
def resolve_task(_, info, id):
    for task in tasks:
        if task["id"] == id:
            return task
    return None

# Resolver function to add a new task
@mutation.field("addTask")
def resolve_add_task(_, info, title, done=False):
    new_task = {
        'id': len(tasks) + 1,
        'title': title,
        'done': done
    }
    tasks.append(new_task)
    return new_task

# Resolver function to update an existing task
@mutation.field("updateTask")
def resolve_update_task(_, info, id, title=None, done=None):
    for task in tasks:
        if task["id"] == id:
            if title is not None:
                task["title"] = title
            if done is not None:
                task["done"] = done
            return task
    return None

# Resolver function to delete a task based on its ID
@mutation.field("deleteTask")
def resolve_delete_task(_, info, id):
    global tasks
    for task in tasks:
        if task["id"] == id:
            tasks.remove(task)
            return True
    return False

# Creating an executable GraphQL schema using type definitions and resolvers
schema = make_executable_schema(type_defs, query, mutation)

# Adding a URL rule to set up the GraphQL endpoint with the Flask app
# We're also enabling the GraphiQL interface for easier testing and exploration
app.add_url_rule("/graphql", view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True))

# Running the Flask app when this script is executed directly
if __name__ == '__main__':
    app.run(debug=True)
