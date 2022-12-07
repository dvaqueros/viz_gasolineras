
# Definimos los colores de cada compañía para las visualizaciones
name_colors = {"OTROS"     : '#%02x%02x%02x' % (89,90,94),
               "BALLENOIL" : '#%02x%02x%02x' % (0,147,203),
               "BP"        : '#%02x%02x%02x' % (17,138,40),
               "CARREFOUR" : '#%02x%02x%02x' % (20,73,146),
               "CEPSA"     : '#%02x%02x%02x' % (199,37,27),
               "GALP"      : '#%02x%02x%02x' % (176,42,12),
               "NATURGY "  : '#%02x%02x%02x' % (210,28,1),
               "PLENOIL"   : '#%02x%02x%02x' % (0,42,104),
               "REPSOL"    : '#%02x%02x%02x' % (253,137,6),
               "SHELL"     : '#%02x%02x%02x' % (251, 199, 11)}

# Definimos unos colores para cada producto
palette =["#f44336",
          "#e81e63",
          "#9c27b0",
          "#673ab7",
          "#3f51b5",
          "#2196f3",
          "#03a9f4",
          "#00bcd4",
          "#009688",
          "#4caf50",
          "#8bc34a",
          "#cddc39",
          "#ffeb3b"]
          #"#ffc107",
          #"#ff9800",
          #"#ff5722",
          #"#795548",
          #"#9e9e9e",
          #"#607d8b",
          #"#000000"]

# Seleccionamos los nombres de las columnas de los precios de las columnas
products = ["gasoline_95E5",
            "gasoline_95E5_premium",
            "gasoline_98E5",
            #"gasoline_98E10",
            "diesel_A",
            "diesel_B",
            "diesel_premium",
            #"bioetanol",
            "biodiesel",
            "lpg",
            "cng",
            "lng"]
            #"hydrogen"]

# Nombres de las columnas de los precios ajustados de las columnas
products_adj = [x + '_adj' for x in products]

# Creamos un diccionario para tipificar los distintos tipos de horario.
schedule_dict = {
    "L-D: 05:00-23:00": "L-D",
    "L-D: 05:59-23:59": "L-D",
    "L-D: 06:00-00:00": "L-D",
    "L-D: 06:00-01:30": "L-D",
    "L-D: 06:00-22:00": "L-D",
    "L-D: 06:00-23:00": "L-D",
    "L-D: 06:00-23:59": "L-D",
    "L-D: 06:30-22:30": "L-D",
    "L-D: 07:00-21:30": "L-D",
    "L-D: 07:00-23:00": "L-D",
    "L-D: 12:00-20:00": "L-D",
    "L-D: 24H": "24H",
    "L-J: 06:30-23:00; V: 06:45-22:45; S: 06:45-14:45": "L-D",
    "L-S: 00:00-14:00": "L-S",
    "L-S: 06:00-22:00": "L-S",
    "L-S: 06:30-21:30; D: 08:00-14:00": "L-D",
    "L-S: 07:00-19:00": "L-S",
    "L-S: 07:00-21:00": "L-S",
    "L-S: 07:00-21:00; D: 09:00-14:00": "L-D",
    "L-S: 07:00-21:00; D: 9:00-14:00": "L-D",
    "L-V: 06:00-21:00": "L-V",
    "L-V: 06:00-21:00; S: 08:00-20:00; D: 09:00-15:00": "L-D",
    "L-V: 06:00-22:00; S-D: 08:00-20:00": "L-D",
    "L-V: 06:00-22:00; S-D: 10:00-19:00": "L-D",
    "L-V: 06:00-22:00; S: 07:00-15:00": "L-S",
    "L-V: 06:00-22:00; S: 07:00-15:00; D: 08:00-16:00": "L-D",
    "L-V: 06:00-23:45; S-D: 07:00-23:00": "L-D",
    "L-V: 07:00-21:00; S: 08:00-14:00": "L-S",
    "L-V: 07:00-21:00; S: 08:00-14:30; D: 09:00-15:00": "L-D",
    "L-V: 07:00-21:00; S: 09:00-14:00": "L-S",
    "L-V: 07:00-21:00; S: 09:00-15:00": "L-S",
    "L-V: 07:00-21:00; S: 09:30-14:30": "L-S",
    "L-V: 07:00-21:30; S: 07:00-14:00": "L-S",
    "L-V: 07:00-21:30; S: 08:00-15:00": "L-S",
    "L-V: 07:00-21:30; S: 08:00-15:30": "L-S",
    "L-V: 07:00-21:30; S: 09:00-14:00": "L-S",
    "L-V: 07:00-21:45; S: 08:15-13:45": "L-S",
    "L-V: 07:00-22:00; S-D: 09:00-21:00": "L-D",
    "L-V: 07:00-22:00; S: 08:00-15:00": "L-S",
    "L-V: 07:00-22:00; S: 08:00-21:00": "L-S",
    "L-V: 07:00-22:00; S: 09:00-14:00": "L-S",
    "L-V: 07:00-22:00; S: 09:00-15:00": "L-S",
    "L-V: 07:30-20:30; S: 08:00-14:00": "L-S",
    "L-V: 07:30-21:00; S: 07:30-14:30; D: 09:00-14:00": "L-D",
    "L-V: 07:30-21:00; S: 08:00-14:30": "L-S",
    "L-V: 07:30-21:00; S: 08:00-15:00; D: 09:00-15:00": "L-D",
    "L-V: 07:30-21:00; S: 08:30-14:45": "L-S",
    "L-V: 07:30-21:00; S: 09:30-14:30": "L-S",
    "L-V: 07:30-21:30; S: 08:00-15:00": "L-S",
    "L-X: 07:00-23:00; J: 07:00-23:59; V-S: 00:00-23:59; D: 00:00-23:00": "L-D",
    "L: 24H": "L",
    "S: 08:00-15:00": "S"
}


# Creamos nueva columna con el nombre tipificado
name_dict = {
    'ALCAMPO'           :"OTROS",
    'ALHAMBRA-BLANCA '  :"OTROS",
    'ALIARA ENERGIA'    :"OTROS",
    'BALLENOIL'         :"BALLENOIL" ,
    'BEROIL LAS ROSAS'  :"OTROS",
    'BP '               :"BP",
    'BP A42 CHEYPER'    :"BP",
    'BP CARABANCHEL'    :"BP",
    'BP E.S. NAVALCARRO':"BP",
    'BP FERMIN FERNANDEZ':"BP",
    'BP GUADALCANAL 365' :"BP",
    'BP ISLA AZUL'      :"BP",
    'BP MADRID - AV DAROCA' :"BP",
    'BP MAYORAZGO 365'  :"BP",
    'BP SAN PEDRO MD'   :"BP",
    'BP SAN PEDRO MI'   :"BP",
    'BP'                :"BP",
    'CAMPSA'            :"OTROS",
    'CARREFOUR'         :"CARREFOUR" ,
    'CEPSA VALLECAS-LA ATALAYUELA 365':"CEPSA" ,
    'CEPSA-ELF'         :"CEPSA" ,
    'CEPSA'             :"CEPSA" ,
    'COMERCIAL SAMA'    :"OTROS",
    'DST '              :"OTROS",
    'DST'               :"OTROS",
    'E.LECLERC'         :"OTROS",
    'GALP'              :"GALP" ,
    'GALP&GO'           :"GALP",
    'GHC'               :"OTROS",
    'HAM TRES CANTOS'   :"OTROS",
    'HUSCO S.L.'        :"OTROS",
    'ION +'             :"OTROS",
    'LOW COST REPOST'   :"OTROS",
    'MADRID WETAXI GLP' :"OTROS",
    'NATURGY '          : "NATURGY" ,
    'NATURGY'           :"NATURGY" ,
    'OIL A42 A-42 KM 9,8  DIR. MADRID' :"OTROS",
    'PADRE-BLANCA'      :"OTROS",
    'PLENOIL'           :"PLENOIL",
    'POWER3OIL'         :"OTROS",
    'Q8'                :"OTROS",
    'REPSOL BUTANO'     :"REPSOL" ,
    'REPSOL'            :"REPSOL" ,
    'REPSOL. ESTACIÓN SUR DE AUTOBUSES DE MADRID' :"REPSOL" ,
    'SHELL'             :"SHELL" ,
    'SHELL ATALAYUELA 365':"SHELL",
    'SIOMN GRUP'        :"OTROS",
    'STAR PETROLEUM'    :"OTROS",
    'SUPECO'            :"OTROS",
    'VIRGEN-BLANCA '    :"OTROS"
}

# Nombres bonitos de los productos
products_titles = {
    "gasoline_95E5"         : "gasolina 95 E5",
    "gasoline_95E5_premium" : "gasolina 95 E5 premium",
    "gasoline_98E5"         : "gasolina 98 E5",
    "gasoline_98E10"        : "gasolina 98 E10",
    "diesel_A"              : "diesel A",
    "diesel_B"              : "diesel B",
    "diesel_premium"        : "diesel premium",
    "bioetanol"             : "bioetanol",
    "biodiesel"             : "biodiesel",
    "lpg"                   : "LPG",
    "cng"                   : "CNG",
    "lng"                   : "LNG",
    "hydrogen"              : "hidrógeno"}

products_titles_r = {
    '95E5': 'gasoline_95E5',
    '95E5 Premium': 'gasoline_95E5_premium',
    '98E5': 'gasoline_98E5',
    '98E10': 'gasoline_98E10',
    'Diesel A': 'diesel_A',
    'Diesel B': 'diesel_B',
    'Diesel Premium': 'diesel_premium',
    'Bioetanol': 'bioetanol',
    'Biodiesel': 'biodiesel',
    'LPG': 'lpg',
    'CNG': 'cng',
    'LNG': 'lng',
    'Hidrógeno': 'hydrogen'}



dict_district_neigh = {
    'Arganzuela'            : ['Todos', 'Acacias','Chopera','Embajadores','Imperial','Palacio','Palos de Moguer'],
    'Barajas'               : ['Todos', 'Aeropuerto','Casco Histórico de Barajas','Corralejos'],
    'Carabanchel'           : ['Todos', 'Abrantes','Buenavista','Comillas','Opañel','San Isidro','Zofío'],
    'Centro'                : ['Todos', 'Arapiles','Universidad'],
    'Chamartin'             : ['Todos', 'Castilla','Ciudad Jardín','El Viso','Hispanoamérica','Nueva España','Prosperidad'],
    'Chamberi'              : ['Todos', 'Almagro','Rios Rosas','Trafalgar','Vallehermoso'],
    'Ciudad Lineal'         : ['Todos', 'Apostol Santiago','Colina','Concepción','Pueblo Nuevo','Quintana','San Juan Bautista','San Pascual','Simancas','Ventas'],
    'Fuencarral-El Pardo'   : ['Todos', 'El Goloso','El Pardo','La Paz','Mirasierra','Peñagrande','Valverde'],
    'Hortaleza'             : ['Todos', 'Canillas','Corralejos','Pinar del Rey','Piovera','Timón','Valdefuentes'],
    'Latina'                : ['Todos', 'Aguilas','Aluche','Cuatro Vientos','Lucero'],
    'Moncloa-Aravaca'       : ['Todos', 'Aluche','Argüelles','Berruguete','Ciudad Universitaria','El Plantío','Valdezarza'],
    'Moratalaz'             : ['Todos', 'Marroquina','Media Legua','Vinateros'],
    'Puente de Vallecas'    : ['Todos', 'Entrevías','Numancia','Palomeras Bajas','Palomeras Sureste','San Diego','Valdebernardo'],
    'Retiro'                : ['Todos', 'Estrella','Pacífico'],
    'Salamanca'             : ['Todos', 'El Viso','Fuente del Berro','Guindalera','Prosperidad','Recoletos'],
    'San Blas'              : ['Todos', 'Amposta','Arcos','Rejas','Rosas','Simancas'],
    'Tetuan'                : ['Todos', 'Almenara','Berruguete','Castilla','Castillejos'],
    'Usera'                 : ['Todos', 'Almendrales','Orcasitas','Orcasur','Pradolongo','San Fermín'],
    'Vicalvaro'             : ['Todos', 'Casco histórico de Vicálvaro','Valdebernardo'],
    'Villa de Vallecas'     : ['Todos', 'Casco Histórico de Vallecas','Casco histórico de Vicálvaro','Ensanche de Vallecas'],
    'Villaverde'            : ['Todos', 'Butarque','Los Angeles','Los Rosales','San Fermín','Villaverde Alto', 'Casco Histórico de Villaverde']
}

list_distritos =['Arganzuela', 'Barajas', 'Carabanchel', 'Centro', 'Chamartin', 'Chamberi', 'Ciudad Lineal', 'Fuencarral-El Pardo', 'Hortaleza', 'Latina', 'Moncloa-Aravaca', 'Moratalaz', 'Puente de Vallecas', 'Retiro', 'Salamanca', 'San Blas', 'Tetuan', 'Usera', 'Vicalvaro', 'Villa de Vallecas', 'Villaverde']


dict_products_clusters = {
    'gasoline_95E5'         : ['Cluster 0', 'Cluster 1', 'Cluster 2', 'Cluster 3', 'Cluster 4', 'Cluster 5', 'Cluster 6', 'Cluster 7', 'Cluster 8', 'Cluster 9', 'Cluster 10', 'Cluster 11', 'Cluster 12', 'Cluster 13', 'Cluster 14'],
    'gasoline_95E5_premium' : ['Cluster 0', 'Cluster 1', 'Cluster 2', 'Cluster 3', 'Cluster 4', 'Cluster 5'],
    'gasoline_98E5'         : ['Cluster 0', 'Cluster 1', 'Cluster 2', 'Cluster 3', 'Cluster 4', 'Cluster 5', 'Cluster 6', 'Cluster 7', 'Cluster 8', 'Cluster 9', 'Cluster 10', 'Cluster 11'],
    'diesel_A'              : ['Cluster 0', 'Cluster 1', 'Cluster 2', 'Cluster 3', 'Cluster 4', 'Cluster 5', 'Cluster 6', 'Cluster 7', 'Cluster 8', 'Cluster 9', 'Cluster 10', 'Cluster 11', 'Cluster 12', 'Cluster 13', 'Cluster 14'],
    'diesel_B'              : ['Cluster 0', 'Cluster 1', 'Cluster 2'],
    'diesel_premium'        : ['Cluster 0', 'Cluster 1', 'Cluster 2', 'Cluster 3', 'Cluster 4', 'Cluster 5', 'Cluster 6', 'Cluster 7', 'Cluster 8', 'Cluster 9', 'Cluster 10', 'Cluster 11', 'Cluster 12', 'Cluster 13'],
    'biodiesel'             : ['Cluster 0'],
    'lpg'                   : ['Cluster 0', 'Cluster 1', 'Cluster 2', 'Cluster 3', 'Cluster 4', 'Cluster 5', 'Cluster 6'],
    'cng'                   : ['Cluster 0', 'Cluster 1', 'Cluster 2', 'Cluster 3'],
    'lng'                   : ['Cluster 0']
}

