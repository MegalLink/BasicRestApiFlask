from flask import Flask, render_template,request,jsonify
from flask_mysqldb import MySQL
import json

app=Flask(__name__)

#mysql Connection
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='MegalLink'
app.config['MYSQL_PASSWORD']='29837077'
app.config['MYSQL_DB']='flaskcontactos'
mysql=MySQL(app)
#Sesion
app.secret_key='mysecretkey'

@app.route('/')
def contactos():
    try:
        cur=mysql.connection.cursor()
        cur.execute('SELECT * from contactos')
        data=cur.fetchall()
        lista=[]
        for dato in data:
            lista.append(dict(id=dato[0],nombre=dato[1],telefono=dato[2],email=dato[3]))
        return {'message':'Exito al obtener los datos','contactos':lista}
    except:
         return {'message':'No se pudo obtener los contactos de la base de datos'}
#@app.route('/contaco/<id>') def contacto(id):
@app.route('/contacto')
def contacto():
    id = request.args.get('id',type=int)
    if id:
        print(id)
        try:            
            cur=mysql.connection.cursor()
            cur.execute('SELECT * FROM contactos WHERE id=%d'%id)
            dato=cur.fetchall()
            contacto={'id':dato[0][0],'nombre':dato[0][1],'telefono':dato[0][2],'email':dato[0][3]}
            return {'message':'Consulta realizada ','contacto':contacto}
        except:
            return  {'message':'No se pudo obtener acceso a la base de dato o no se encontro el contacto con ese id'}
    else:
        return {'message':'Error al ingresar el id /contacto?id=<id> ejemplo /contacto?id=10'}

    
@app.route('/agregar_contacto',methods=['POST'])
def agregar_contacto():
    try:
        nombre=request.json['nombre']
        telefono=request.json['telefono']
        email=request.json['email']
        
    except:
        return "No se obtuvieron todos los campos"
         
    contacto={'nombre':nombre,'telefono':telefono,'email':email}
    cur=mysql.connection.cursor()
    cur.execute('INSERT INTO contactos (nombre,telefono,email) VALUES(%s,%s,%s)',(nombre,telefono,email))
    try:
        mysql.connection.commit()
        return {'message':'Agregado con exito','contacto':contacto}
    except:
        return {'message':'Error al agregar a la base de datos','contacto':contacto}

@app.route('/editar_contacto',methods=['POST'])
def editar_contacto():
    try:
        id=request.json['id']
        nombre=request.json['nombre']
        telefono=request.json['telefono']
        email=request.json['email']
        
        try:
            contacto={'id':id,'nombre':nombre,'telefono':telefono,'email':email}
            sql='UPDATE contactos SET nombre="%s",telefono="%s", email="%s" where id=%d'%(nombre,telefono,email,id)
            cur=mysql.connection.cursor()
            cur.execute(sql)
            try: 
                mysql.connection.commit()
                print(cur.rowcount,"Records affected")
                return {'message':'Modificado con exito ','contacto':contacto}
            except:
                return {'message':'No se tiene acceso a la base de datos'}
        except:
            return {'message':'No existe el contacto a editar ','contacto':contacto}
    except:
        return {'message':'Envie todos los campos del contacto a editar'}
@app.route('/borrar_contacto',methods=['POST'])
def borrar_contacto():
    try:
        id=request.json['id']
        nombre=request.json['nombre']
        telefono=request.json['telefono']
        email=request.json['email']
        
        try:
            contacto={'id':id,'nombre':nombre,'telefono':telefono,'email':email}
            sql='DELETE from contactos where id=%d'%(id)
            cur=mysql.connection.cursor()
            cur.execute(sql)
            try: 
                mysql.connection.commit()
                print(cur.rowcount,"Records affected")
                return {'message':'Contacto eliminado con Exito ','contacto':contacto}
            except:
                return {'message':'No se tiene acceso a la base de datos'}
        except:
            return {'message':'No existe el contacto a eliminar ','contacto':contacto}
    except:
        return {'message':'Envie todos los campos del contacto a editar'}
        

    
 
@app.errorhandler(404)
def no_encontrado(error=None):

    response=jsonify({'message':'Recurso no encontrado: '+request.url,'status':404})
    response.status_code=404
    return response
if __name__ == '__main__':
    app.run(port =3000, debug=True)
