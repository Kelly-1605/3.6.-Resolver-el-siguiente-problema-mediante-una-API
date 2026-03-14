from flask import Flask, request, jsonify # [cite: 157]
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__) # [cite: 163]

# Configuración de la base de datos SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///estudiantes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialización de la base de datos
db = SQLAlchemy(app)

# Definición del Modelo de Estudiante (Equivalente a la tabla en la DB)
class Estudiante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    carrera = db.Column(db.String(100), nullable=False)
    semestre = db.Column(db.Integer, nullable=False)

# Crear la base de datos y la tabla si no existen
with app.app_context():
    db.create_all()

# Endpoint POST: Registrar un nuevo estudiante
@app.route('/estudiantes', methods=['POST']) # [cite: 167, 172]
def agregar_estudiante():
    datos = request.get_json() # [cite: 175]
    
    # Obtener y validar datos [cite: 178, 179]
    nuevo_estudiante = Estudiante(
        nombre=datos['nombre'],
        carrera=datos['carrera'],
        semestre=datos['semestre']
    )
    
    # Guardar en la base de datos
    db.session.add(nuevo_estudiante)
    db.session.commit()
    
    return jsonify({"mensaje": "Estudiante registrado con éxito"}), 201 # [cite: 196]

# Endpoint GET: Consultar todos los estudiantes
@app.route('/estudiantes', methods=['GET'])
def obtener_estudiantes():
    # Consultar todos los registros de la tabla
    estudiantes = Estudiante.query.all()
    
    # Convertir los objetos a una lista de diccionarios JSON [cite: 191]
    resultado = []
    for e in estudiantes:
        resultado.append({
            "id": e.id,
            "nombre": e.nombre,
            "carrera": e.carrera,
            "semestre": e.semestre
        })
    
    return jsonify(resultado), 200

# Ejecución de la aplicación [cite: 210, 213]
if __name__ == '__main__':
    app.run(debug=True)