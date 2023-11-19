import pandas as pd
from sqlalchemy import create_engine

def actualizarTablaDimension(engine, table, data, pk="id"):
    """
    Esta función actualiza una tabla de dimensión de un DW con los datos nuevos. Si los datos
    ya existen en la tabla, no se agregan. Devuelve la tabla actualizada con los pk tal cual esta
    en la base de datos.

    La tabla de dimensión debe estar creada y las columnas deben llamarse igual que en el df.

    Parametros:
        engine: engine de la base de datos
        table: nombre de la tabla
        data: datafarme de datos nuevos a agregar, sin incluir la PK
        pk: nombre de la PK. Por defecto es "ID"

    Retorno:
        dimension_df: datafarme con la tabla según está en la DB con los datos nuevos agregados.

    """
    with engine.connect() as conn, conn.begin():
        old_data = pd.read_sql_table(table, conn)

        # Borro la columna pk
        old_data.drop(pk, axis=1, inplace=True)

        # new_data es el datafarme de datos diferencia de conjunto con old_data
        new_data = data[~data.stack().isin(old_data.stack().values).unstack()].dropna()

        # insertar new_data
        new_data.to_sql(table, conn, if_exists='append', index=False)

        # buscar como quedó la tabla
        dimension_df = pd.read_sql_table(table, conn)

    return dimension_df

# Creo el engine de la base de datos
engine_cubo = create_engine('postgresql+psycopg2://postgres:data2@localhost:5432/produccion_hc', echo=False)

# Obtengo los datos de petroleo y los reviso.
datos_petroleo = pd.read_csv('../datos/produccion.csv')


# Dimension Empresas
dimension_empresas = pd.DataFrame({'nombre': datos_petroleo['empresa'].unique()})
dimension_empresas = actualizarTablaDimension(engine_cubo, 'empresas', dimension_empresas, pk='id')
print(dimension_empresas)

# Dimension Pozos
dimension_pozos = datos_petroleo.groupby(['idpozo', 'coordenadax', 'coordenaday']).size().reset_index(name='count')
dimension_pozos = dimension_pozos.drop_duplicates(subset=['idpozo'])
dimension_pozos = dimension_pozos.drop(columns=['count'])
dimension_pozos.rename(columns={'idpozo': 'id', 'coordenadax': 'coordenada_x', 'coordenaday': 'coordenada_y'}, inplace=True)
dimension_pozos = actualizarTablaDimension(engine_cubo, 'pozos', dimension_pozos, pk='id')
print(dimension_pozos)

# Dimension Extraccion
dimension_extraccion = pd.DataFrame({'tipo_extraccion': datos_petroleo['tipo_de_recurso'].unique()})
dimension_extraccion = actualizarTablaDimension(engine_cubo, 'extraccion', dimension_extraccion, pk='id')
print(dimension_extraccion)

# Dimension Tiempo
dimension_tiempo = datos_petroleo.groupby(['mes', 'anio']).size().reset_index(name='count')
dimension_tiempo = dimension_tiempo.drop_duplicates(subset=['mes', 'anio'])
dimension_tiempo = dimension_tiempo.drop(columns=['count'])
nombre_meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio','Agosto', 'Septiembre', 'Octubre','Noviembre', 'Diciembre']
dimension_tiempo['nombre_mes'] = dimension_tiempo['mes'].apply(lambda x: nombre_meses[x-1])
meses_a_trimestres = {
    'enero': 1,
    'febrero': 1,
    'marzo': 1,
    'abril': 2,
    'mayo': 2,
    'junio': 2,
    'julio': 3,
    'agosto': 3,
    'septiembre': 3,
    'octubre': 4,
    'noviembre': 4,
    'diciembre': 4
}

# Aplicar la función map para crear la nueva columna 'trimestre'
dimension_tiempo['trimestre'] = dimension_tiempo['nombre_mes'].str.lower().map(meses_a_trimestres)

dimension_tiempo = actualizarTablaDimension(engine_cubo, 'tiempo', dimension_tiempo, pk='mes')
print(dimension_tiempo)

# Dimension Provincias
dimension_provincias = pd.DataFrame({'nombre': datos_petroleo['provincia'].unique()})
dimension_provincias = actualizarTablaDimension(engine_cubo, 'provincias', dimension_provincias, pk='id')
print(dimension_provincias)

# Creo el df de hechos. Para eso voy a agregar el mapeo de los datos de origen a los valores de fk.
hechos_df = pd.DataFrame({
    # Dimensiones
    'empresa': datos_petroleo['empresa'].map(dimension_empresas.set_index('nombre')['id']),
    'pozo': datos_petroleo['idpozo'],
    'provincia': datos_petroleo['provincia'].map(dimension_provincias.set_index('nombre')['id']),
    'extraccion': datos_petroleo['tipo_de_recurso'].map(dimension_extraccion.set_index('tipo_extraccion')['id']),
    'fecha': datos_petroleo['mes'].map(dimension_tiempo.set_index('mes')['id']),

    # Mediciones
    'produccion_petroleo_mes': datos_petroleo['prod_pet'],
    'produccion_gas_mes': datos_petroleo['prod_gas']
})

print(hechos_df)

# Actualizo la tabla de hechos
actualizarTablaDimension(engine_cubo, 'produccion', hechos_df, pk='id')

print('ETL finalizado')