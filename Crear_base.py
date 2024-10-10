import sqlite3

# Conectar a la base de datos (se creará si no existe)
conn = sqlite3.connect('formularioPOP.db')
cursor = conn.cursor()

# Crear la tabla 'controles'
cursor.execute('''
CREATE TABLE IF NOT EXISTS controles (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    COD_DOCUMENTACION INTEGER,
    FASE VARCHAR(50),
    DETALLE TEXT,
    CONTROL TEXT,
    REQUERIDO VARCHAR(1),
    RESPUESTA TEXT
);
''')

# Insertar datos de ejemplo
datos = [
    (2, 'DOCUMENTAL', 'HABILITACION SANITARIA SERVICIOS OBJETO DE REGISTRO', '¿Está disponible el archivo con la póliza? ¿Está vigente?',1, 'Falta habilitación sanitaria expedida por el MSAL u ente con competencia suficiente (dependiendo de cada jurisdicción: Colegios Médicos, Consejos Médicos, Ministerio de Salud de la Provincia o alguna dependencia de éste) o la misma NO se encuentra vigente.'),
    (2, 'DOCUMENTAL', 'HABILITACION SANITARIA SERVICIOS OBJETO DE REGISTRO', '¿Coincide la dirección de la boca de atención ofrecida con la habilitación subida?',1, 'La dirección declarada en la habilitación sanitaria, NO coincide con la declarada en la boca de atención.'),
    (2, 'DOCUMENTAL', 'HABILITACION SANITARIA SERVICIOS OBJETO DE REGISTRO', '¿La persona declarada coincide con la declarada en la habilitación?',1, 'La persona declarada en la habilitación sanitaria, NO coincide con la del oferente del servicio'),
    (2, 'DOCUMENTAL', 'HABILITACION SANITARIA SERVICIOS OBJETO DE REGISTRO', '¿La dirección de la habilitación sanitaria coincide con la UGL ofertada?',1, 'La dirección de la habilitación sanitaria NO se corresponde con la UGL de la boca de atención ofertada.'),
    (2, 'DOCUMENTAL', 'HABILITACION SANITARIA SERVICIOS OBJETO DE REGISTRO', '¿La habilitación cubre los requerimientos  de servicio del módulo?',1, 'La habilitación sanitaria NO cubre los requerimientos asociados con el/los modulo/s ofertado/s'),
    (3, 'DOCUMENTAL', 'CONSTANCIA REGISTRO NACIONAL DE PRESTADORES - SUPERINTENDENCIA DE SERVICIOS DE LA SALUD (SSSALUD)', '¿Está disponible el certificado? ',1, 'Falta constancia del Registro Nacional de Prestadores expedido por la Superintendencia de Salud (alternativamente se permite el trámite de inscripción en dicho registro)'),
    (4, 'DOCUMENTAL', 'DECLARACION JURADA NO PROHIBICIONES INSSJP (cfr. Art. 21 Res. 124/DE/18)', '¿La declaración jurada cumple con las formas establecidas en el formulario?',1, 'Falta Declaración Jurada de NO Prohibiciones (disponible en el sitio web de PAMI) o la misma contiene errores formales.'),
    (28, 'IMPOSITIVA', 'TITULO UNIVERSITARIO Y MATRICULA PROFESIONAL', '¿Está cargado el título universitario?',1, 'Título Universitario vinculado al ofrecimiento'),
    (28, 'IMPOSITIVA', 'TITULO UNIVERSITARIO Y MATRICULA PROFESIONAL', '¿Se encuentra disponible la matrícula profesional ? ¿Se encuentra vigente?',1, 'Falta presentar matrícula profesional vigente'),
    (31, 'DOCUMENTAL', 'CURRICULUM VITAE', '¿Se encuentra cargado el curriculum profesional?',1, 'Debe cargar el curriculum profesional'),
    (40, 'DOCUMENTAL', 'SEGURO (RESP. CIVIL + MALA PRAXIS + INCENDIO) + INTEGRAL DE COMERCIO EN CASO DE CORRESPONDER', '¿Está cargado el seguro contra incendio correspondiente?',1, 'Falta Poliza vigente del Seguro contra Incedios de la consultorio asociado al ofrecimiento'),
    (40, 'DOCUMENTAL', 'SEGURO (RESP. CIVIL + MALA PRAXIS + INCENDIO) + INTEGRAL DE COMERCIO EN CASO DE CORRESPONDER', 'El seguro contra incendio ¿Se encuentra vigente?',1, 'Falta póliza de seguro contra incendios o la misma NO se encuentra vigente.'),
    (40, 'DOCUMENTAL', 'SEGURO (RESP. CIVIL + MALA PRAXIS + INCENDIO) + INTEGRAL DE COMERCIO EN CASO DE CORRESPONDER', 'El seguro contra incendio ¿Está asociado al consultorio?',1, 'La póliza de seguro contra incendios NO se corresponde a la dirección definida en la boca de atención ofertada.'),
    (40, 'DOCUMENTAL', 'SEGURO (RESP. CIVIL + MALA PRAXIS + INCENDIO) + INTEGRAL DE COMERCIO EN CASO DE CORRESPONDER', 'El seguro de responsabilidad civil ¿Se encuentra vigente?',1, 'Falta póliza del seguro de responsabilidad civil o la misma NO se encuentra vigente.'),
    (40, 'DOCUMENTAL', 'SEGURO (RESP. CIVIL + MALA PRAXIS + INCENDIO) + INTEGRAL DE COMERCIO EN CASO DE CORRESPONDER', 'El seguro de responsabilidad civil ¿Se encuentra asociada al oferente?',1, 'La póliza del seguro de responsabilidad civil NO esta asociada al oferente.'),
    (77, 'DOCUMENTAL', 'ACTO ADMINISTRATIVO DE LA JURISDICCION AUTORIZANDO A EJERCER EN EL LUGAR DE ATENCION', '¿El oferente es titular del lugar de atención?',0, 'Falta presentar acto administrativo autorizando a ejercer actividades en el lugar de atención'),
    (86, 'DOCUMENTAL', 'CERTIFICADO DE ETICA PROFESIONAL', 'El certificado de ética profesional ¿Cumple con las formas establecidas en el formulario?',1, 'Falta presentar el certificado de ética profesional o el mismo NO cumple con las formalidades requeridas (en tal caso, revisar el mismo).'),
    (92, 'DOCUMENTAL', 'CONSTANCIA DE RESIDUOS PATOGENICOS O DDJJ DE EXCEPCION Y ULTIMO PAGO', '¿Se encuentra cargado el certificado de generador de residuos patogénicos o la DDJJ de excepción?',1, 'Falta contancia de residudos patogénicos (adjuntar último pago).  De NO ser generador de residuos: DDJJ de excepción'),
    (92, 'DOCUMENTAL', 'CONSTANCIA DE RESIDUOS PATOGENICOS O DDJJ DE EXCEPCION Y ULTIMO PAGO', 'La dirección de la constancia de residuos patogénicos ¿Coincide con la dirección de la boca de atención?',1, 'Falta contancia de residudos patogénicos (adjuntar último pago) o la dirección de la constancia de residuos patogénicos, NO coincide con la dirección del establecimiento declarado como BATE'),
    (114, 'DOCUMENTAL', 'SUSCRIPCION DDJJ ACCESIBILIDAD FISICA', '¿Está disponible la declaración jurada de accesibilidad física?',1, 'Falta la Declaración Jurada de Accesibilidad Física o la misma NO cumple con todas las formalidades fijadas en el mismo.'),
    (128, 'DOCUMENTAL', 'ANTECEDENTES PENALES', '¿Se encuentra disponible el certificado de antecedentes penales emitido por el Registro Nacional de Reincidencia? ¿Es de emisión reciente?',1, 'Falta el certificado de antecedentes penales emitido  por el Registro Nacional de Reincidencia.  El certificado debe haber sido emitido en los últimos 6 meses.'),
    (212, 'DOCUMENTAL', 'CERTIFICADO DE CAPACIDAD PRESTACIONAL', '¿Se encuentra disponible el certificado de capacidad prestacional?',1, 'Falta el certificado de capacidad prestacional o el mismo NO detalla la capacidad para todos los módulos ofrecidos.'),
    (37, 'DOCUMENTAL', 'ACTA ASAMBLEA DESIGNACION AUTORIDADES', '¿Se encuentra disponible el acta de asamblea de designación de autoridades?',1, 'Acta de asamblea de designación de autoridades'),
    (115, 'DOCUMENTAL', 'AMPLIACIONES ESTATUTARIAS Y/O ACTUALIZACIONES', 'De corresponder ¿Se encuentran cargadas las ampliaciones estatutarias y/o actualizaciones de la misma?',0, 'Debe cargar las ampliaciones estatutarias y/o actualizaciones de la misma'),
    (116, 'DOCUMENTAL', 'DOCUMENTO DONDE CONSTE EL ULTIMO DOMICILIO REAL INSCRIPTO EN IGJ', '¿Se encuentra disponible el documento donde conste el último domicilio real inscripto en IGJ?',0, 'Cargar documento legal en donde conste el último domicilio real inscripto en la IGJ'),

]

cursor.executemany('''
INSERT INTO controles (COD_DOCUMENTACION, FASE, DETALLE, CONTROL, REQUERIDO, RESPUESTA)
VALUES (?, ?, ?, ?, ?, ?);
''', datos)

# Guardar los cambios y cerrar la conexión
conn.commit()
conn.close()

print("Base de datos 'formularioPOP.db' creada exitosamente con la tabla 'controles' y datos de ejemplo.")
