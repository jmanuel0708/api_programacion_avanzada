from flask import Flask, render_template, request, redirect, url_for, make_response

from methods import crear_cuenta, iniciar_sesion, encontrar_usuario_por_id

from extensions import jwt

from flask_jwt_extended import decode_token, verify_jwt_in_request, get_jwt_identity

firma = 'c6krTENs82o7pib'

def cargar_rutas(app):
    # Ruta raíz
    @app.route('/')
    def pagina():

        logged = False

        try:
            verify_jwt_in_request()
            logged = True

        except Exception as error:
            logged = False

        return render_template('index.html', logged=logged)

    # Esta es otra ruta
    @app.route('/login')
    def informacion_jose():

        logged = False

        try:
            verify_jwt_in_request()
            logged = True
        except Exception as error:
            logged = False
            print(error)

        resultado = request.args.get('status')
        if logged == True:
            return redirect(url_for('pantalla_usuario'))
        else:
            return render_template('login.html', estado=resultado)

    # Esta es otra ruta
    @app.route('/signup')
    def datos():

        logged = False

        try:
            verify_jwt_in_request()
            logged = True
        except Exception as error:
            logged = False
            print(error)

        resultado = request.args.get('status')
        if logged == True:
            return redirect(url_for('pantalla_usuario'))
        else:
            return render_template('signup.html', estado=resultado)
        
    # Esta ruta va a manejar la información
    # Este método solo funcionará para el inicio de sesión
    @app.route('/manipulacion', methods=['POST'])
    def manipular_datos():
        email = request.form.get('email')
        password = request.form.get('password')

        print(f'''
            Correo: {email}
        ''')

        respuesta_login = iniciar_sesion(email, password)

        if respuesta_login['status'] == 'error':
            return redirect(url_for('informacion_jose', status=respuesta_login['status']))
        
        respuesta = make_response(redirect(url_for('pagina')))

        respuesta.set_cookie('access_token', respuesta_login['token'], secure=True, max_age=3600)

        return respuesta

    # Interceptamos la información del Sign Up del usuario
    @app.route('/datos_crear_cuenta', methods=['POST'])
    def obtener_datos_cuenta():
        nombre = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        print(f'''
        nombre: {nombre}
        correo: {email}
        ''')

        respuesta_signup = crear_cuenta(nombre, email, password)

        print(respuesta_signup)

        if respuesta_signup['status'] == 'error':
            return redirect(url_for('datos', status=respuesta_signup['status']))

        return redirect(url_for('pagina', status=respuesta_signup['status']))

    @app.route('/error')
    def pantalla_error():

        return render_template('error.html')
    
    @app.route('/usuario')
    def pantalla_usuario():
        try:
            verify_jwt_in_request()
            nombre_de_usuario = get_jwt_identity()
            id_del_usuario = request.args.get('user_id')
            datos_usuario = encontrar_usuario_por_id(id_del_usuario)
            datos_usuario = [datos_usuario.id, datos_usuario.name, datos_usuario.email]

            print(datos_usuario)

            return render_template('user.html', user_data=datos_usuario)
        except Exception as error:
            print('La cookie no existe o está mal')
            print(f'La razón es: {error}')

            return redirect(url_for('informacion_jose'))
        
    @app.route('/logout')
    def cerrar_sesion():
        respuesta = make_response(redirect(url_for('pagina')))
        respuesta.set_cookie('access_token', '')

        return respuesta
    
    @app.route('/user_info')
    def obtener_info_usuario():
        try:
            verify_jwt_in_request()
            user_token = request.cookies.get('access_token')
            token_info = decode_token(user_token)
            id_usuario = token_info['user_id']

            return redirect(url_for('pantalla_usuario', user_id=id_usuario))

        except Exception as error:
            print(error)
            return redirect(url_for('pagina'))