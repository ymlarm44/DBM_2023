import pandas as pd

tabla_produccion = pd.read_csv('../datos/produccin-de-pozos-de-gas-y-petrleo-2022.csv')

tabla_pozos = pd.read_csv('../datos/listado-de-pozos-cargados-por-empresas-operadoras.csv')

tabla_produccion.drop(
    [
        'prod_agua', 'iny_agua', 'iny_gas', 'iny_co2', 'iny_otro', 'tef',
        'vida_util', 'tipoextraccion', 'tipoestado', 'tipopozo',
        'observaciones', 'fechaingreso', 'rectificado', 'habilitado',
        'idusuario', 'sigla', 'formprod', 'profundidad', 'formacion',
        'idareapermisoconcesion', 'areapermisoconcesion', 'idareayacimiento',
        'areayacimiento', 'cuenca', 'proyecto', 'clasificacion', 'subclasificacion',
        'sub_tipo_recurso', 'fecha_data'
    ], axis=1, inplace=True)

tabla_pozos.drop(
    ['sigla', 'formprod', 'idempresa', 'idareapermisoconcesion',
       'idareayacimiento', 'idcuenca', 'idprovincia', 'codigopropio',
       'nombrepropio', 'cota', 'profundidad',
       'pet_inicial', 'gas_inicial', 'agua_inicial', 'iny_agua_inicial',
       'iny_gas_inicial', 'iny_otros_inicial', 'iny_co2_inicial',
       'vida_util_inicial', 'adjiv_fecha_inicio', 'adjiv_equipo_utilizar',
       'adjiv_capacidad_perf', 'adjiv_tipo_reservorio',
       'adjiv_subtipo_reservorio', 'adjiv_fecha_fin',
       'adjiv_fecha_inicio_term', 'adjiv_fecha_fin_term',
       'adjiv_fecha_abandono', 'adjiv_clasificacion', 'adjiv_subclasificacion',
       'fechadeingreso', 'adjiv_comp_perf', 'unique_sigla_formprod',
       'areapermisoconcesion', 'areayacimiento', 'cuenca', 'provincia',
       'petroleo', 'gas', 'agua', 'periodo', 'clasificacion',
       'subclasificacion', 'tipo_reservorio', 'subtipo_reservorio',
       'comp_perf', 'gasplus', 'fecha_data'], axis=1, inplace=True)

tabla_combinada = pd.merge(tabla_produccion, tabla_pozos, on='idpozo')

tabla_combinada.to_csv('../datos/produccion.csv', index=False)