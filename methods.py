from models import Usuario

def crear_cuenta(nombre, email, password):
    
    usuario_existente = Usuario.query.filter_by(email=email).first()

    if usuario_existente is not None:
        print("El correo ya existe en la base de datos")
        return {'status': 'error', 'error': 'La cuenta ya esta registrada'}
    
    nuevo_usuario = Usuario(name=nombre, email=email)
    nuevo_usuario.hashear_password(password_original = password)
    nuevo_usuario.save()

    return {'status': 'ok', 'email':email}


def iniciar_sesion(email, password):
    usuarios_existentes = Usuario.query.filter_by(email = email).first()

    if usuarios_existentes is None:
        print("La cuenta no existe")
        return {'status': 'error', 'error': 'La cuenta no existe'}

    if usuarios_existentes.verificar_password(password_plano = password):
        pass