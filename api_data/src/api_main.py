from flask import Flask, request
import pymysql
import os

os.chdir(os.path.dirname(__file__))

app = Flask(__name__)
app.config["DEBUG"] = True

username = "admin"
password_db = "83J%y92vwWgAyvJ%DW%YvXB*"
host = "database-ocult.crt8burntnnh.us-east-1.rds.amazonaws.com"
port = 3306

@app.route('/api/v1/resources/users/all', methods=['GET'])
def get_all_users():
    connection = pymysql.connect(host = host,
                        user = username,
                        password = password_db,
                        cursorclass = pymysql.cursors.DictCursor,
                        database = 'ocult'
    )

    cursor = connection.cursor()
    select_users = "SELECT * FROM user"
    cursor.execute(select_users)
    result = cursor.fetchall()
    connection.close()
    return {'users': result}

@app.route('/api/v1/resources/users/<string:iduser>', methods=['GET'])
def get_one_user(iduser):
    connection = pymysql.connect(host = host,
                        user = username,
                        password = password_db,
                        cursorclass = pymysql.cursors.DictCursor,
                        database = 'ocult'
    )

    cursor = connection.cursor()
    select_user = 'SELECT * FROM user WHERE iduser={iduser}'
    # cursor.execute(select_user, (iduser,))
    cursor.execute(select_user)
    result = cursor.fetchall()
    connection.close()
    return {'user': result}

@app.route('/api/v2/resources/users', methods=['GET'])
def get_one_user_v2():
    connection = pymysql.connect(host = host,
                        user = username,
                        password = password_db,
                        cursorclass = pymysql.cursors.DictCursor,
                        database = 'ocult'
    )

    query_parameters = request.get_json()
    id = query_parameters.get('id')

    cursor = connection.cursor()
    select_user = f'SELECT * FROM user WHERE iduser={id}'
    cursor.execute(select_user)
    result = cursor.fetchall()
    connection.close()
    return {'user': result}


@app.route('/api/v1/new_user', methods=["POST"])
def new_user():
    connection = pymysql.connect(host = host,
                        user = username,
                        password = password_db,
                        cursorclass = pymysql.cursors.DictCursor,
                        database = 'ocult'
    )

    cursor = connection.cursor()
    email= request.args.get("email",None)
    idcompany = request.args.get("idcompany",None)
    iduser = request.args.get("iduser",None)
    image = request.args.get("image",None)
    lastscore = request.args.get("lastscore",None)
    name = request.args.get("name",None)
    password = request.args.get("password",None)
    list_values = [email,idcompany, iduser,image,lastscore,name,password]
    if email is None or idcompany is None or iduser is None or image is None or lastscore is None or name is None or password is None:
        return "Args empty, the data was not stored"
    else:
        cursor.execute('INSERT INTO user (email, idcompany, iduser, image, lastscore, name, password) VALUES (email, idcompany, iduser, image, lastscore, name, password)')

    connection.commit()
    connection.close()

@app.route('/api/v1/resources/company', methods=['GET'])
def get_all_companies():
    connection = pymysql.connect(host = host,
                        user = username,
                        password = password_db,
                        cursorclass = pymysql.cursors.DictCursor,
                        database = 'ocult'
    )

    cursor = connection.cursor()
    select_company = "SELECT * FROM company"
    cursor.execute(select_company)
    result = cursor.fetchall()
    connection.close()
    return {'empresas': result}


@app.route('/api/v1/resources/company/<string:company>', methods=['GET'])
def get_company(idcompany):
    connection = pymysql.connect(host = host,
                        user = username,
                        password = password_db,
                        cursorclass = pymysql.cursors.DictCursor,
                        database = 'ocult'
    )

    cursor = connection.cursor()
    select_company = "SELECT * FROM company WHERE company=?"
    result = cursor.execute(select_company, (idcompany,)).fetchall()
    connection.close()
    return {'empresas': result}

app.run()