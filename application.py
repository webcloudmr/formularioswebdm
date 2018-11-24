from flask import Flask, render_template, jsonify, url_for, redirect 
from flask import request, redirect, make_response, flash
from flask import session as login_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from functools import wraps
from database_setup import Base, SISTEMASIMPRESORAS, RRHHVACACIONES, RRHHSALIDA, RRHHDIAESTUDIO, COMERCIALACTIVIDADES, OPERACIONESEDILICIAS, User
import random
import string
import json
import datetime

app = Flask(__name__)

#BASE DE DATOS 
engine = create_engine('postgresql://sa:ASD123qweAB@localhost/dbformulariosdm')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()
#-------------------------------------------------------------------------------------------------



#1 LOGIN - REGISTRARSE - LOGOUT - PERFIL
#1.1 FORMULARIOS DM: LOGIN

@app.route('/', methods=['GET', 'POST'])	
@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('1_1_LoginUsuario.html')
	else:
		if request.method == 'POST':
			print ("dentro de POST login")
			user = session.query(User).filter_by(
				username = request.form['username'],
				password = request.form['password']).first()
			if not user:
				error = "Usuario no registrado"
				flash('Usuario no registrado')
				return redirect(url_for('login', error = error ) )
			else:
				print ("dentro de user")
				login_session['username'] = request.form['username']
				return redirect(url_for('FormulariosDM', username=login_session['username']))

#1.2 FORMULARIOS DM: REGISTRAR USUARIO				
@app.route('/RegistrarUsuario', methods=['GET', 'POST'])
def RegistrarUsuario():
	if request.method == 'GET':
		return render_template('1_2_RegistrarUsuario.html')
	else:
		if request.method == 'POST':
			nuevoUsuario = User(
					username = request.form['username'],
					password=request.form['password'],
					email = request.form['email']) 
			session.add(nuevoUsuario)
			session.commit()
			login_session['username'] = request.form['username']
			return redirect(url_for('login'))

#1.3 FORMULARIOS DM: PERFIL USUARIO	
@app.route('/PerfilUsuario', methods=['GET'])
def PerfilUsuario():
	user = session.query(User).filter_by()
	if 'username' in login_session:
		username = login_session['username'] 	 
		flash('Debe Iniciar Sesion para acceder al PANEL DE CONSULTAS')
		return render_template('1_3_PerfilUsuario.html', username=login_session['username'])	
	else:
		
		return render_template('1_3_PerfilUsuario.html')
		
#1.4 FORMULARIOS DM: LOGOUT
@app.route('/logout')
def logout():
		del login_session['username']
		return redirect(url_for('login'))

def login_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if 'username' not in login_session:
			return redirect(url_for('login'))
		return f(*args, **kwargs)
	return decorated_function
	

#1.5 FORMULARIOS DM: BIENVENIDA			
@app.route('/FormulariosDM', methods=['GET'])
def FormulariosDM():
	if 'username' in login_session:
		username = login_session['username'] 	 
		flash('Debe Iniciar Sesion para acceder al PANEL DE CONSULTAS')
		return render_template('1_5_Bienvenida.html', username=login_session['username'])	
	else:
		return render_template('1_5_Bienvenida.html')	
	
#1.6 FORMULARIOS DM: NUEVA CONTRASEÑA		
@app.route('/NuevaPass', methods=['GET'])
def NuevaPass(id):
	valores = session.query(User).filter_by(id = id).one()
	username = login_session['username']
	if request.method == 'GET':
		return render_template('1_6_1_NuevaPass.html', valores = valores)
	
			
#1.7 FORMULARIOS DM: NUEVA CONTRASEÑA		
@app.route('/editarNuevaPass/editar/<int:id>', methods=['GET', 'POST'])
def editarNuevaPass(id):
	valores = session.query(User).filter_by(id = id).one()
	username = login_session['username']
	if request.method == 'GET':
		return render_template('1_6_1_NuevaPass.html', valores = valores)
	else:
		if request.method == 'POST':
			
			username = login_session['username']			
			valoresaEditar = session.query(User).filter_by(id = id).one()
			valoresaEditar.password=request.form['password'],
						
			session.commit()
			return redirect(url_for('login'))



	
		
			
		
# -------------------------------------------------------------------------------------------------------	

#2 OPERACIONES: MANTENIMIENTO E INFRAESTRUCTURA
#2.1 OPERACIONES HOME
@app.route('/OperacionesHome', methods=['GET'])
def OperacionesHome():
	valores = session.query(OPERACIONESEDILICIAS).all()
	if 'username' in login_session:
		username = login_session['username']
		return render_template('2_1_Operaciones_Home.html', valores = valores, username=username)	
	else:
		return render_template('2_1_Operaciones_Home.html', valores = valores)

#2.2 OPERACIONES EDILICIAS: FORMULARIO PARA AGREGAR Y GUARDAR EN DB		
@app.route('/OperacionesEdilicias', methods=['GET', 'POST'])
def OperacionesEdilicias():
	valores = session.query(OPERACIONESEDILICIAS).all()
	if request.method == 'GET':
		username = login_session['username']
		return render_template('2_2_Operaciones_Edilicias.html', valores = valores, username=username)	
	else:
		if request.method == 'POST':
			username = login_session['username']
			operacionesedilicias = OPERACIONESEDILICIAS(
					nombreyapellido = request.form['nombreyapellido'],
					sede = request.form['sede'],
					piso = request.form['piso'],
					inconveniente = request.form['inconveniente'],
					estado = 'Abierto',
					autor = username,
					mantenimiento = 'Asignado',
					fecha_solicitud = datetime.datetime.now())
			session.add(operacionesedilicias)
			session.commit()
			return redirect(url_for('OperacionesHome'))
#2.3 OPERACIONES EDILICIAS: REPORTES DE SOLICITUDES AGREGADAS			
@app.route('/OperacionesEdiliciasReportes', methods=['GET'])
def OperacionesEdiliciasReportes():
	valores = session.query(OPERACIONESEDILICIAS).all()
	if 'username' in login_session:
		username = login_session['username']
		return render_template('2_3_Operaciones_EdiliciasReportes.html', valores = valores, username=username)	
	else:
		return render_template('2_3_Operaciones_EdiliciasReportes.html', valores = valores)

#2.4 OPERACIONES EDILICIAS: ELIMINAR SOLICITUD		
@app.route('/OperacionesEdiliciasEliminar/eliminar/<int:id>', methods=['GET', 'POST'])
def OperacionesEdiliciasEliminar(id):
	valores = session.query(OPERACIONESEDILICIAS).filter_by(id = id).one()
				
	username = login_session['username']
	if request.method == 'GET' and valores.autor == username:
		return render_template('2_4_Operaciones_ConfirmacionElimiarSolicitud.html', valores = valores)
	else:
		if request.method == 'POST':
			session.delete(valores)
			# delete blog set id=2
			session.commit()
			flash('Eliminado correctamente')
			return redirect(url_for('OperacionesEdiliciasReportes'))
		else:
			
			return redirect(url_for('Operaciones_PermisoDenegado'))
#2.4.1 MANEJO DE ERROR AL ELIMINAR: NO ES PROPIETARIO		
@app.route('/Operaciones_PermisoDenegado', methods=['GET'])
def Operaciones_PermisoDenegado():
	return render_template('2_4_1_Operaciones_PermisoDenegado.html')	
	
#2.5 EDITAR / MODIFICAR SOLICITUD AGREGADA

@app.route('/OperacionesEdiliciasEditar/editar/<int:id>', methods=['GET', 'POST'])
def OperacionesEdiliciasEditar(id):
	valores = session.query(OPERACIONESEDILICIAS).filter_by(id = id).one()
	username = login_session['username']
	if request.method == 'GET' and valores.autor == username:
		return render_template('2_5_Operaciones_EditarSolicitud.html', valores = valores)
	else:
		if request.method == 'POST':
			
			username = login_session['username']			
			valoresaEditar = session.query(OPERACIONESEDILICIAS).filter_by(id = id).one()
			valoresaEditar.nombreyapellido = request.form["nombreyapellido"]
			valoresaEditar.sede = request.form["sede"]
			valoresaEditar.piso = request.form["piso"]
			valoresaEditar.inconveniente = request.form["inconveniente"]
			valoresaEditar.estado = request.form["estado"]
			valoresaEditar.mantenimiento = request.form["mantenimiento"]			
			session.commit()
			return redirect(url_for('OperacionesEdiliciasReportes'))
			


		
# OPERACIONES FIN
# --------------------------------------------------------------------------------------

#4	RECURSOS HUMANOS: FORMULARIOS

#-------------------------------------------------------------------------------------------------
#4.1 Home RRHH
#-------------------------------------------------------------------------------------------------
@app.route('/RRHHHome', methods=['GET'])
def RRHHHome():
	valores = session.query(RRHHDIAESTUDIO).all()
	if 'username' in login_session:
		username = login_session['username']
		return render_template('4_1_RRHH_Home.html', valores = valores, username=username)	
	else:
		return render_template('4_1_RRHH_Home.html', valores = valores)

#4.2 RRHH - FORMULARIO PARA AGREGAR Y GUARDAR EN DB
@app.route('/RRHHDiaDeEstudio', methods=['GET', 'POST'])
def RRHHDiaDeEstudio():
	valores = session.query(RRHHDIAESTUDIO).all()
	if request.method == 'GET':
		username = login_session['username']
		return render_template('4_2_RRHH_DiaDeEstudio.html', valores = valores, username=username)	
	else:
		if request.method == 'POST':
			username = login_session['username']
			rrhhdiaestudio = RRHHDIAESTUDIO(
					nombreyapellido = request.form['nombreyapellido'],
					legajo = request.form['legajo'],
					materia = request.form['materia'],
					fecha = request.form['fecha'],
					autor = username,
					nombreyapellidosup = request.form['nombreyapellidosup'],
					cargosup = 'Supervisor',
					estado = 'Abierto',
					fecha_solicitud = datetime.datetime.now()
					)
			session.add(rrhhdiaestudio)
			session.commit()
			return redirect(url_for('RRHHHome'))

#4.3 RRHH - REPORTES SOLICITUDES AGREGADAS
@app.route('/RRHHReportesDiaDeEstudio', methods=['GET'])
def RRHHReportesDiaDeEstudio():
	valores = session.query(RRHHDIAESTUDIO).all()
	if 'username' in login_session:
		username = login_session['username']
		return render_template('4_3_RRHH_ReportesDiaDeEstudio.html', valores = valores, username=username)	
	else:
		return render_template('4_3_RRHH_ReportesDiaDeEstudio.html', valores = valores)
		
#4.4 RRHH - ELIMINAR SOLICITUD DE DIA DE ESTUDIO
@app.route('/rrhhdiaestudio/eliminar/<int:id>', methods=['GET', 'POST'])
def eliminarRRHHDIAESTUDIO(id):
	valores = session.query(RRHHDIAESTUDIO).filter_by(id = id).one()
	username = login_session['username']
	if request.method == 'GET' and valores.autor == username:
		return render_template('4_4_RRHH_ConfirmacionElimiarSolicitud.html', valores = valores)
	else:
		if request.method == 'POST':
			session.delete(valores)
			# delete blog set id=2
			session.commit()
			return redirect(url_for('RRHHReportesDiaDeEstudio'))
		else:
			return redirect(url_for('RRHHPermisoDenegado'))

#4.4.1 RRHH - PERMISO DENEGADO PARA ELIMINAR -- NO GENERO ESTA SOLICITUD --
@app.route('/RRHHPermisoDenegadodiadeestudio', methods=['GET'])
def RRHHPermisoDenegadodiadeestudio():
	return render_template('4_4_1_RRHH_PermisoDenegado.html')

#4.5 EDITAR / MODIFICAR SOLICITUD AGREGADA

@app.route('/rrhhdiaestudio/editar/<int:id>', methods=['GET', 'POST'])
def editarRRHHDIAESTUDIO(id):
	valores = session.query(RRHHDIAESTUDIO).filter_by(id = id).one()
	username = login_session['username']
	if request.method == 'GET' and valores.autor == username:
		return render_template('4_5_RRHH_EditarSolicitud.html', valores = valores)
	else:
		if request.method == 'POST':
			
			username = login_session['username']			
			postaEditar = session.query(RRHHDIAESTUDIO).filter_by(id = id).one()
			postaEditar.nombreyapellido = request.form["nombreyapellido"]
			postaEditar.legajo = request.form["legajo"]
			postaEditar.materia = request.form["materia"]
			postaEditar.fecha = request.form["fecha"]
			postaEditar.estado = request.form["estado"]
						
			session.commit()
			return redirect(url_for('RRHHReportesDiaDeEstudio'))
#-------------------------------------------------------------------------------------------------------

#5	RECURSOS HUMANOS: VACACIONES

#-------------------------------------------------------------------------------------------------
#5.1 RRHH - FORMULARIO PARA AGREGAR Y GUARDAR EN DB
#-------------------------------------------------------------------------------------------------
	
@app.route('/RRHHSolicitudVacaciones', methods=['GET', 'POST'])
def RRHHSolicitudVacaciones():
	valores = session.query(RRHHVACACIONES).all()
	if request.method == 'GET':
		username = login_session['username']
		return render_template('5_1_RRHH_SolicitudVacaciones.html', valores = valores, username=username)	
	else:
		if request.method == 'POST':
			username = login_session['username']
			rrhhvacaciones = RRHHVACACIONES(
					tipo = request.form['tipo'],
					nombreyapellido = request.form['nombreyapellido'],
					legajo = request.form['legajo'],
					cantidaddias = request.form['cantidaddias'],
					fechacomienzo = request.form['fechacomienzo'],
					fechafinalizacion = request.form['fechafinalizacion'],
					fechareinicio = request.form['fechareinicio'],
					nombreyapellidosup = request.form['nombreyapellidosup'],
					cargosup = 'Supervisor',
					autor = username,
					estado = 'Abierto',
					fecha_solicitud = request.form['fecha_solicitud'])
			session.add(rrhhvacaciones)
			session.commit()
			return redirect(url_for('RRHHHome'))
			
#5.2 RRHH - REPORTES SOLICITUDES AGREGADAS
@app.route('/RRHHReportesVacaciones', methods=['GET'])
def RRHHReportesVacaciones():
	valores = session.query(RRHHVACACIONES).all()
	if 'username' in login_session:
		username = login_session['username']
		return render_template('5_2_RRHH_ReportesVacaciones.html', valores = valores, username=username)	
	else:
		return render_template('5_2_RRHH_ReportesVacaciones.html', valores = valores)

#5.3 RRHH - ELIMINAR SOLICITUD DE VACACIONES

@app.route('/rrhhvacaciones/eliminar/<int:id>', methods=['GET', 'POST'])
def eliminarRRHHVACACIONES(id):
	valores = session.query(RRHHVACACIONES).filter_by(id = id).one()
	username = login_session['username']
	if request.method == 'GET' and valores.autor == username:
		return render_template('5_3_RRHH_ConfirmacionEliminarSolicitud.html', valores = valores)
	else:
		if request.method == 'POST':
			session.delete(valores)
			# delete blog set id=2
			session.commit()
			return redirect(url_for('RRHHReportesVacaciones'))
		else:
			return redirect(url_for('RRHHPermisoDenegado'))

#5.3.1 RRHH - PERMISO DENEGADO PARA ELIMINAR -- NO GENERO ESTA SOLICITUD --
@app.route('/RRHHPermisoDenegadovacaciones', methods=['GET'])
def RRHHPermisoDenegadovacaciones():
	return render_template('5_3_1_RRHH_PermisoDenegado.html')
	
	
#5.4 EDITAR / MODIFICAR SOLICITUD AGREGADA

@app.route('/rrhhvacaciones/editar/<int:id>', methods=['GET', 'POST'])
def editarRRHHVACACIONES(id):
	valores = session.query(RRHHVACACIONES).filter_by(id = id).one()
	username = login_session['username']
	if request.method == 'GET' and valores.autor == username:
		return render_template('5_4_RRHH_EditarSolicitud.html', valores = valores)
	else:
		if request.method == 'POST':
			
			username = login_session['username']			
			postaEditar = session.query(RRHHVACACIONES).filter_by(id = id).one()
			postaEditar.tipo = request.form["tipo"]
			postaEditar.nombreyapellido = request.form["nombreyapellido"]
			postaEditar.legajo = request.form["legajo"]
			postaEditar.fechacomienzo = request.form["fechacomienzo"]
			postaEditar.fechafinalizacion = request.form["fechafinalizacion"]
			postaEditar.fechareinicio = request.form["fechareinicio"]
			postaEditar.nombreyapellidosup = request.form["nombreyapellidosup"]
			postaEditar.estado = request.form["estado"]
													
			session.commit()
			return redirect(url_for('RRHHReportesVacaciones'))
#-------------------------------------------------------------------------------------------------------	


#6	COMERCIAL: FORMULARIOS
#-------------------------------------------------------------------------------------------------
#6.1 Home COMERCIAL
#-------------------------------------------------------------------------------------------------
			
@app.route('/ComercialHome', methods=['GET'])
def ComercialHome():
	valores = session.query(COMERCIALACTIVIDADES).all()
	if 'username' in login_session:
		username = login_session['username']
		return render_template('6_1_Comercial_Home.html', valores = valores, username=username)	
	else:
		return render_template('6_1_Comercial_Home.html', valores = valores)

#-------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------
#6.2 COMERCIAL: Inscripcion Actividades
#-------------------------------------------------------------------------------------------------
		
@app.route('/ComercialInscripcionActividades', methods=['GET', 'POST'])
def ComercialInscripcionActividades():
	valores = session.query(COMERCIALACTIVIDADES).all()
	if request.method == 'GET':
		username = login_session['username']
		return render_template('6_2_Comercial_InscripcionActividades.html', valores = valores, username=username)	
	else:
		if request.method == 'POST':
			username = login_session['username']
			comercialactividades = COMERCIALACTIVIDADES(
					fecha_solicitud = request.form['fecha_solicitud'],
					
					nombreyapellido = request.form['nombreyapellido'],
					dni = request.form['dni'],
					correo = request.form['correo'],
					telefono = request.form['telefono'],
					evento = request.form['evento'],
					autor = username,
					estado = 'Abierto',
					)
			session.add(comercialactividades)
			session.commit()
			return redirect(url_for('ComercialHome'))

#6.3 COMERCIAL - REPORTES INSCRIPCIONES AGREGADAS
@app.route('/COMERCIALReportesInscripciones', methods=['GET'])
def COMERCIALReportesInscripciones():
	valores = session.query(COMERCIALACTIVIDADES).all()
	if 'username' in login_session:
		username = login_session['username']
		return render_template('6_3_Comercial_ReportesInscripciones.html', valores = valores, username=username)	
	else:
		return render_template('6_3_Comercial_ReportesInscripciones.html', valores = valores)
#-------------------------------------------------------------------------------------------------------
#6.4 COMERCIAL: ELIMINAR INSCRIPCION

@app.route('/comercialactividades/eliminar/<int:id>', methods=['GET', 'POST'])
def eliminarCOMERCIALACTIVIDADES(id):
	valores = session.query(COMERCIALACTIVIDADES).filter_by(id = id).one()
	username = login_session['username']
	if request.method == 'GET' and valores.autor == username:
		return render_template('6_4_Comercial_ConfirmarEliminarInscripcion.html', valores = valores)
	else:
		if request.method == 'POST':
			session.delete(valores)
			# delete blog set id=2
			session.commit()
			return redirect(url_for('COMERCIALReportesInscripciones'))
		else:
			return redirect(url_for('COMERCIALPermisoDenegadoinscripciones'))

#6.4.1 COMERCIAL - PERMISO DENEGADO PARA ELIMINAR -- NO GENERO ESTA SOLICITUD --
@app.route('/COMERCIALPermisoDenegadoinscripciones', methods=['GET'])
def COMERCIALPermisoDenegadoinscripciones():
	return render_template('6_4_1_Comercial_PermisoDenegado.html')
#-------------------------------------------------------------------------------------------------------	

#6.5 EDITAR / MODIFICAR SOLICITUD AGREGADA

@app.route('/comercialactividades/editar/<int:id>', methods=['GET', 'POST'])
def editarCOMERCIALACTIVIDADES(id):
	valores = session.query(COMERCIALACTIVIDADES).filter_by(id = id).one()
	username = login_session['username']
	if request.method == 'GET' and valores.autor == username:
		return render_template('6_5_Comercial_EditarInscripcion.html', valores = valores)
	else:
		if request.method == 'POST':
			
			username = login_session['username']			
			postaEditar = session.query(COMERCIALACTIVIDADES).filter_by(id = id).one()
			
			postaEditar.nombreyapellido = request.form["nombreyapellido"]
			postaEditar.dni = request.form["dni"]
			postaEditar.correo = request.form["correo"]
			postaEditar.telefono = request.form["telefono"]
			postaEditar.evento = request.form["evento"]
			postaEditar.estado = request.form["estado"]
				
											
			session.commit()
			return redirect(url_for('COMERCIALReportesInscripciones'))
	




 	


# -------------------------------------------------------------------------------------------------------
			



@app.route('/PanelDeControl', methods=['GET'])
def PanelDeControl():
	username = login_session['username']
	if username == 'adm-mrojas' or username == 'mrojas' :
		flash('Debe Iniciar Sesion para acceder al PANEL DE CONSULTAS')
		return render_template('PanelDeControl.html', username=login_session['username'])	
	else:
		return render_template('1_1_login.html')	
		

		
# -------------------------------------------------------------------------------------------------------
			
# ATENCION AL PACIENTE
			
@app.route('/Atencionalpaciente_Home', methods=['GET'])
def Atencionalpaciente_Home():
	#posts = session.query(OPERACIONES).all()
	# select * from blog
	
	if 'username' in login_session:
		username = login_session['username']
		return render_template('Atencionalpaciente_Home.html', username=username)	
	else:
		return render_template('Atencionalpaciente_Home.html',)

# -------------------------------------------------------------------------------------------------------
			
# CALIDAD
			
@app.route('/Calidad_Home', methods=['GET'])
def Calidad_Home():
	#posts = session.query(OPERACIONES).all()
	# select * from blog
	
	if 'username' in login_session:
		username = login_session['username']
		return render_template('Calidad_Home.html', username=username)	
	else:
		return render_template('Calidad_Home.html',)		
		
# -------------------------------------------------------------------------------------------------------
			
# LABORATORIO
			
@app.route('/Laboratorio_Home', methods=['GET'])
def Laboratorio_Home():
	#posts = session.query(OPERACIONES).all()
	# select * from blog
	
	if 'username' in login_session:
		username = login_session['username']
		return render_template('Laboratorio_Home.html', username=username)	
	else:
		return render_template('Laboratorio_Home.html',)		

# -------------------------------------------------------------------------------------------------------
			
# SISTEMAS
			
@app.route('/Sistemas_Home', methods=['GET'])
def Sistemas_Home():
	#posts = session.query(OPERACIONES).all()
	# select * from blog
	
	if 'username' in login_session:
		username = login_session['username']
		return render_template('Sistemas_Home.html', username=username)	
	else:
		return render_template('Sistemas_Home.html',)		

		
	
	

					

if __name__ == '__main__':
	app.secret_key = "secret key"
	app.debug = True
	app.run(host = '0.0.0.0', port = 8080)
