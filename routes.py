from flask import Flask, render_template, request, redirect, url_for

from methods import crear_cuenta, iniciar_sesion, encontrar_todos_los_usuarios

def cargar_rutas(app):
# Este bloque de código es la base para todas rutas
  @app.route('/')
  def pagina():
    lista_usuarios = encontrar_todos_los_usuarios()

    for usuario in lista_usuarios:
      print(f"""
      Usuario: {usuario.name}
      Correo: {usuario.email}
      Password: {usuario.password}
      """)

    return render_template('index.html')

  # Esta es otra ruta
  @app.route('/login')
  def informacion_jose():
    return render_template('login.html')

  # Esta es otra ruta
  @app.route('/signup')
  def datos():
    return render_template('signup.html')

  # Esta ruta va a manejar la información
  # Este método solo funcionará para el inicio de sesión
  @app.route('/manipulacion', methods=['POST'])
  def manipular_datos():
    email = request.form.get('email')
    password = request.form.get('password')

    print(f'''
      Correo: {email}
      Contraseña: {password}
  ''')

    iniciar_sesion()

    return redirect(url_for('pagina'))

  # Interceptamos la información del Sign Up del usuario
  @app.route('/datos_crear_cuenta', methods=['POST'])
  def obtener_datos_cuenta():
    nombre = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    print(f'''
    nombre: {nombre}
    correo: {email}
    passoword: {password}
  ''')

    crear_cuenta(nombre, email, password)



    
    return redirect(url_for('pagina'))