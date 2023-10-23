from spyne import Application, ServiceBase, rpc, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgicors import CORS
from spyne.model.complex import ComplexModel
from spyne.model.complex import Iterable
from spyne.model.primitive import Integer
import json

# sv

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

db = psycopg2.connect(
    user="postgres",
    password="1234",
    host="localhost",
    port='5432',
    database = "chefencasa"
)
cursor = db.cursor()



class HelloWorldService(ServiceBase):
    @rpc(Unicode, _returns=Unicode)
    def getMassive(ctx, name):
        print(name)
        ctx.transport.resp_headers['Access-Control-Allow-Origin'] = '*'
        ctx.transport.resp_headers['Access-Control-Allow-Headers'] = 'Content-Type'
        ctx.transport.resp_headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'


        if name == '':
            return "No hay recetas".encode()
        if name == '[]':
            return "No hay recetas".encode()
        if name == None:
            return "No hay recetas".encode()
        if name == 'null':
            return "No hay recetas".encode()
        if name == 'undefined':
            return "No hay recetas".encode()

        # get recipes
        cursor.execute("SELECT * FROM recipes as r where r.id_user = {0} and isDraft = 1".format(name))
        recipes = cursor.fetchall()


        # recipes is [(7, 'Sopa de zapallo', 'Perfecta para dias de invierno', 30, 2, 3, None, datetime.datetime(2023, 10, 10, 21, 44, 49, 278550), 1, datetime.datetime(2023, 10, 10, 21, 44, 49, 278550)), (8, 'Nachos con Cheddar', 'Clasico mexicano', 20, 2, 4, None, datetime.datetime(2023, 10, 10, 21, 44, 49, 278973), 1, datetime.datetime(2023, 10, 10, 21, 44, 49, 278973))]
        # convert it to json

        # fix to Object of type datetime is not JSON serializable

        recipes = json.dumps(recipes, default=str)
        print(recipes)
        return recipes.encode()



    
    @rpc(Unicode, _returns=Unicode)
    def createMassive(ctx, name):
        ctx.transport.resp_headers['Access-Control-Allow-Origin'] = '*'
        ctx.transport.resp_headers['Access-Control-Allow-Headers'] = 'Content-Type'
        ctx.transport.resp_headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
        if name == '':
            return "No hay recetas".encode()
        if name == '[]':
            return "No hay recetas".encode()
        if name == None:
            return "No hay recetas".encode()

        formattedRecipes = json.loads(name)
        print(formattedRecipes)
        for recipe in formattedRecipes:
            
            # (recipe['title'], recipe['description'], recipe['category'], recipe['prepatarionTimeMinutes'])
            print("---------------------")
            print(recipe)
            cursor.execute("INSERT INTO recipes (title, description, id_category, preparation_time_minutes, id_user, isDraft) VALUES ('{0}', '{1}', {2}, {3}, {4}, 1)".format(recipe['title'], recipe['description'], recipe['category'], recipe['prepatarionTimeMinutes'], recipe['userId']))
            db.commit()
        return "Crear, wea!".encode()
    

    @rpc(Unicode, _returns=Unicode)
    def createRecipeBook(ctx, name):
        ctx.transport.resp_headers['Access-Control-Allow-Origin'] = '*'
        ctx.transport.resp_headers['Access-Control-Allow-Headers'] = 'Content-Type'
        ctx.transport.resp_headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
        if name == '':
            return "No hay recetas".encode()
        if name == '[]':
            return "No hay recetas".encode()
        if name == '{}':
            return "No hay recetas".encode()
        if name == None:
            return "No hay recetas".encode()

        print("createRecipeBook")
        print(name)

        formattedRequest = json.loads(name)
        userId = formattedRequest['userId']
        title = formattedRequest['title']

        print(userId)
        print(title)
        print("INSERT INTO recetario (id_user, name) VALUES ({0}, '{1}')".format(userId, title))
        print(name)


        cursor.execute("INSERT INTO recetario (id_user, name) VALUES ({0}, '{1}')".format(userId, title))
        db.commit()
        
        return "Crear, wea!".encode()
    

    @rpc(Unicode, _returns=Unicode)
    def createRecipeBookItem(ctx, name):
        ctx.transport.resp_headers['Access-Control-Allow-Origin'] = '*'
        ctx.transport.resp_headers['Access-Control-Allow-Headers'] = 'Content-Type'
        ctx.transport.resp_headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
        if name == '':
            return "No hay recetas".encode()
        if name == '[]':
            return "No hay recetas".encode()
        if name == '{}':
            return "No hay recetas".encode()
        if name == None:
            return "No hay recetas".encode()
        
        print("createRecipeBookItem")
        print(name)

        formattedRecipes = json.loads(name)
        print(formattedRecipes)
        recipeId = formattedRecipes['recipeId']
        recipeBookId = formattedRecipes['recipeBookId']

        cursor.execute("INSERT INTO recetario_recipes (id_recetario, id_recipe) VALUES ({0}, {1})".format(recipeBookId, recipeId))
        db.commit()
        
        return "Crear, wea!".encode()
    
    # works
    @rpc(Unicode, _returns=Unicode)
    def deleteRecipeBook(ctx, name):
        ctx.transport.resp_headers['Access-Control-Allow-Origin'] = '*'
        ctx.transport.resp_headers['Access-Control-Allow-Headers'] = 'Content-Type'
        ctx.transport.resp_headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
        if name == '':
            return "No hay recetas".encode()
        if name == '[]':
            return "No hay recetas".encode()
        if name == '{}':
            return "No hay recetas".encode()
        if name == None:
            return "No hay recetas".encode()

        recipeBookId = name

        print(recipeBookId)
        print("DELETE FROM recetario WHERE id = {0}".format(recipeBookId))

        # fix:
        cursor.execute("DELETE FROM recetario_recipes WHERE id_recetario = {0}".format(recipeBookId))
        cursor.execute("DELETE FROM recetario WHERE id = {0}".format(recipeBookId))


        db.commit()
        
        return "Crear, wea!".encode()    
    
    # works
    @rpc(Unicode, _returns=Unicode)
    def getRecipeBooks(ctx, name):
        ctx.transport.resp_headers['Access-Control-Allow-Origin'] = '*'
        ctx.transport.resp_headers['Access-Control-Allow-Headers'] = 'Content-Type'
        ctx.transport.resp_headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
        if name == '':
            return "No hay recetas".encode()
        if name == '[]':
            return "No hay recetas".encode()
        if name == '{}':
            return "No hay recetas".encode()
        if name == None:
            return "No hay recetas".encode()
        
        print("getRecipeBooks")
        print(name)

        cursor.execute("SELECT * FROM recetario as r where r.id_user = {0}".format(name))
        recipeBooks = cursor.fetchall()


        return json.dumps(recipeBooks, default=str).encode()
    
    @rpc(Unicode, _returns=Unicode)
    def getRecipeBooksItems(ctx, name):
        ctx.transport.resp_headers['Access-Control-Allow-Origin'] = '*'
        ctx.transport.resp_headers['Access-Control-Allow-Headers'] = 'Content-Type'
        ctx.transport.resp_headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
        if name == '':
            return "No hay recetas".encode()
        if name == '[]':
            return "No hay recetas".encode()
        if name == '{}':
            return "No hay recetas".encode()
        if name == None:
            return "No hay recetas".encode()
        
        recipeBookId = name

        print("getRecipeBooksItems")
        print(name)
        
        cursor.execute("SELECT recipes.* FROM recipes JOIN recetario_recipes ON recipes.id = recetario_recipes.id_recipe WHERE recetario_recipes.id_recetario = {0};".format(recipeBookId))   



        
        recipeBooks = cursor.fetchall()


        return json.dumps(recipeBooks, default=str).encode()
    
    

app = Application([HelloWorldService], 'http://localhost:8000/draft',
                  in_protocol=Soap11(validator='lxml'),
                  out_protocol=Soap11())

def soap_handler(environ, start_response):
    print(environ['REQUEST_METHOD'])


    if environ['REQUEST_METHOD'] != 'POST':
        print(1)
        headers = [
            ('Access-Control-Allow-Origin', '*'),
            ('Access-Control-Allow-Headers', 'Content-Type'),
            ('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        ]
        print(2)
        start_response('200 OK', headers)
        return [b'OK']

    else:
        return wsgi_app(environ, start_response)


if __name__ == '__main__':
    try:
        from wsgiref.simple_server import make_server
        wsgi_app = WsgiApplication(app)
        # wrapped_app = CORS(wsgi_app, headers="*", methods="*")
        server = make_server('0.0.0.0', 8000, soap_handler)
        print("SOAP server listening on port 8000...")
        server.serve_forever()
    except ImportError:
        print("Error: example server code requires Python >= 2.5")
    except KeyboardInterrupt:
        print("Interrupted by user")
    except Exception as e:
        print(e)