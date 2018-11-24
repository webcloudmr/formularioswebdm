import sys
import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class SISTEMASIMPRESORAS(Base):
	__tablename__ = 'sistemasimpresoras'

	id = Column(Integer, primary_key=True)
	sede = Column(String(50), nullable=False)
	piso = Column(String(50), nullable=False)
	serie = Column(String(50), nullable=False)
	falla = Column(String(250), nullable=False)
	autor = Column(String(50), nullable=False)
	estado = Column(String(50), nullable=False)
	fecha_creacion = Column(DateTime, nullable=False)
	
class RRHHVACACIONES(Base):
	__tablename__ = 'rrhhvacaciones'

	id = Column(Integer, primary_key=True)
	fecha_solicitud = Column(String(30), nullable=False)
	tipo = Column(String(15), nullable=False)
	nombreyapellido = Column(String(40), nullable=False)
	legajo = Column(String(10), nullable=False)
	cantidaddias = Column(String(2), nullable=False)
	fechacomienzo = Column(String(30), nullable=False)
	fechafinalizacion = Column(String(30), nullable=False)
	fechareinicio = Column(String(30), nullable=False)
	nombreyapellidosup = Column(String(30), nullable=False)
	cargosup = Column(String(40), nullable=False)
	autor = Column(String(20), nullable=False)
	estado = Column(String(20), nullable=False)
	
	
class RRHHSALIDA(Base):
	__tablename__ = 'rrhhsalida'

	id = Column(Integer, primary_key=True)
	fecha_solicitud = Column(DateTime, nullable=False)
	nombreyapellido = Column(String(40), nullable=False)
	legajo = Column(String(10), nullable=False)
	motivo = Column(String(100), nullable=False)
	horasalida = Column(String(30), nullable=False)
	horaretorno = Column(String(30), nullable=False)
	nombreyapellidosup = Column(String(30), nullable=False)
	cargosup = Column(String(30), nullable=False)
	autor = Column(String(20), nullable=False)
	estado = Column(String(20), nullable=False)
	
	
class RRHHDIAESTUDIO(Base):
	__tablename__ = 'rrhhdiaestudio'

	id = Column(Integer, primary_key=True)
	fecha_solicitud = Column(DateTime, nullable=False)
	nombreyapellido = Column(String(40), nullable=False)
	legajo = Column(String(10), nullable=False)
	materia = Column(String(50), nullable=False)
	fecha = Column(String(30), nullable=False)
	nombreyapellidosup = Column(String(40), nullable=False)
	cargosup = Column(String(40), nullable=False)
	autor = Column(String(20), nullable=False)
	estado = Column(String(20), nullable=False)
	
	
	
class COMERCIALACTIVIDADES(Base):
	__tablename__ = 'comercialactividades'

	id = Column(Integer, primary_key=True)
	fecha_solicitud = Column(String(30), nullable=False)
	
	nombreyapellido = Column(String(40), nullable=False)
	dni = Column(String(50), nullable=False)
	correo = Column(String(50), nullable=False)
	telefono = Column(String(15), nullable=False)
	evento = Column(String(50), nullable=False)
	autor = Column(String(20), nullable=False)
	estado = Column(String(20), nullable=False)
	
	
class OPERACIONESEDILICIAS(Base):
	__tablename__ = 'operacionesedilicias'

	id = Column(Integer, primary_key=True)
	fecha_solicitud = Column(DateTime, nullable=False)
	nombreyapellido = Column(String(40), nullable=False)
	sede = Column(String(20), nullable=False)
	piso = Column(String(20), nullable=False)
	inconveniente = Column(String(150), nullable=False)
	estado = Column(String(50), nullable=False)
	autor = Column(String(50), nullable=False)
	mantenimiento = Column(String(30), nullable=False)
	
	

	



class User(Base):
	__tablename__ = 'user'

	id = Column(Integer, primary_key=True)
	username = Column(String(50), nullable=False)
	password = Column(String(250), nullable=False)
	email = Column(String(250), nullable=False)
	

	

engine = create_engine('postgresql://sa:ASD123qweAB@localhost/dbformulariosdm')
Base.metadata.create_all(engine)
