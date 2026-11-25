"""Todos os textos do xogo (en galego): diálogos, retos e preguntas.

Nivel 1 — O tempo e o clima (libro, Unidade 2, páx. 26-39). Unha misión por apartado:
  1. A atmosfera e os fenómenos atmosféricos (páx. 26-27)
  2. Elementos e factores do clima (páx. 28-29)
  3. Os climas de España (páx. 30-31)
  4. Os climogramas (páx. 32-33)
  5. As paisaxes e os incendios (páx. 34-35)
  6. O clima de Galicia e a estación meteorolóxica (páx. 36-37)
  7. Como está cambiando o clima (páx. 38-39)
Para cambiar ou engadir preguntas, edita só este ficheiro.
"""

PERSONAJES = {
    "brisa": ("Dra. Brisa", (48, 112, 200)),
    "nubi": ("Nubi", (72, 100, 150)),
    "baron": ("Barón Feluxe", (124, 48, 156)),
    "tubito": ("Tubiño", (88, 96, 120)),
}

# ================================================================ DIÁLOGOS

INTRO = [
    ("brisa", "Ola! Son a Doutora Brisa, meteoróloga do Val Verde. E esta é Nubi, unha nube moi valente."),
    ("nubi", "Ola a todos! Hoxe imos aprender como funcionan o tempo e o clima."),
    ("baron", "Ja, ja, jaaa! Calor? Seca? Fume? Esas son as miñas palabras favoritas!"),
    ("baron", "Son o Barón Feluxe, xefe da Banda Tisne. Encherei o ceo de fume e o monte de faíscas!"),
    ("tubito", "Fiu-fiu! E eu son Tubiño, o seu robot axudante. Boto fume polas dúas orellas!"),
    ("brisa", "Para pararlles os pés temos que saber moito sobre o tempo e o clima. Axudades a Nubi?"),
]

M1_INTRO = [
    ("brisa", "A atmosfera é a capa de gases que rodea a Terra. Nela pasan os fenómenos atmosféricos: o vento, as nubes, a chuvia..."),
    ("brisa", "Arrastra cada tarxeta ao seu sitio. Tamén podes tocar a tarxeta e despois o destino."),
]
M1_FIN = [
    ("brisa", "Moi ben! Xa sabes por que é tan importante a atmosfera e como se forman as nubes, a chuvia e o arco da vella."),
    ("tubito", "Fiu... O Barón vai enfadarse moito."),
]

M2_INTRO = [
    ("nubi", "Doutora, que diferenza hai entre o tempo e o clima?"),
    ("brisa", "O tempo é o que pasa hoxe. O clima é o que adoita pasar nun lugar, estudado durante varias décadas."),
    ("brisa", "Os ELEMENTOS do clima mídense con instrumentos. Os FACTORES climáticos fan que o clima sexa distinto en cada lugar."),
]
M2_FIN = [
    ("brisa", "Perfecto! A latitude, a altitude, o mar e o relevo cambian a temperatura, a chuvia e o vento de cada lugar."),
]

M3_INTRO = [
    ("brisa", "A Terra divídese en zonas climáticas segundo a latitude. España está na zona temperada."),
    ("baron", "E en España hai sitios moi quentes e secos... Ideais para as miñas faíscas! Ja, ja!"),
    ("brisa", "Non todas as zonas de España teñen o mesmo clima, por iso o risco de incendio non é igual en todas."),
]
M3_FIN = [
    ("brisa", "Xenial! Oceánico, continental, mediterráneo, de montaña e subtropical: España ten moitos climas!"),
]

M4_INTRO = [
    ("brisa", "A climatoloxía estuda o clima a longo prazo. Para representalo usamos os climogramas."),
    ("brisa", "Nun climograma, a liña VERMELLA son as temperaturas e as barras AZUIS, as precipitacións de cada mes."),
]
M4_FIN = [
    ("brisa", "Moi ben! Cun climograma vemos que meses son quentes e secos... e neses meses hai máis risco de incendio."),
    ("nubi", "E lembra: o vento fai que o lume se estenda máis rápido!"),
]

M5_INTRO = [
    ("brisa", "Unha paisaxe é unha zona da Terra que vemos en conxunto: o clima, o relevo, as plantas e os animais."),
    ("baron", "Que bonitas paisaxes... e que ben arderían! Tubiño, prepara as faíscas!"),
    ("brisa", "Primeiro aprende as paisaxes e as súas plantas. Despois, Nubi terá que apagar os lumes!"),
]
M5_FIN = [
    ("brisa", "Lembra: o cambio climático, o mato seco e a mala xestión do monte son causas dos incendios. Previr é fundamental!"),
]

M6_INTRO = [
    ("brisa", "Galicia está no noroeste da Península. Case toda ten clima oceánico, pero hai tres variedades."),
    ("brisa", "Tamén coñeceremos a estación meteorolóxica e o risco de incendio na nosa comunidade."),
]
M6_FIN = [
    ("brisa", "Moi ben! Galicia ten clima oceánico litoral, de interior e de montaña. E desde 2023 hai un dispositivo contra o lume todo o ano."),
]

M7_INTRO = [
    ("brisa", "O cambio climático é un cambio no clima debido á actividade humana. Altera a composición da atmosfera."),
    ("baron", "Ja! Fume, coches e bosques talados: ese é o meu gran plan!"),
    ("brisa", "Descubramos as súas causas, as súas consecuencias e como podemos frealo."),
]
M7_PRE_BATALLA = [
    ("baron", "Grrr! Ninguén estraga os meus plans! Nubi, desafíote a unha batalla final!"),
    ("tubito", "Fiu-fiu! Fará preguntas de TODO o tema!"),
    ("brisa", "Ti podes, Nubi! Cada resposta correcta lanzará un ataque de auga."),
]
M7_FIN = [
    ("baron", "Non pode ser! A miña capa, empapada! Tubiño, ao dirixible!"),
    ("tubito", "Fiu-fiuuu! Volveremos con máis fume!"),
    ("brisa", "Parabéns, gardiáns do clima! Agora sabedes moito sobre o tempo, o clima e como coidar o planeta."),
]

# ================================================================ RETOS

# --- Misión 1
FUNCIONS = {
    "instrucion": "Que fai a atmosfera? Arrastra cada tarxeta á súa caixa.",
    "caixas": [("si", "SI, a atmosfera fai isto", (48, 160, 88)),
               ("non", "NON, a atmosfera non fai isto", (208, 72, 64))],
    "tarxetas": [
        ("Filtra os raios solares prexudiciais", "si", "A atmosfera filtra as radiacións solares que nos fan dano."),
        ("Regula a temperatura do planeta", "si", "A atmosfera regula a temperatura para que a Terra sexa habitable."),
        ("Ten osíxeno para respirar", "si", "A atmosfera contén o osíxeno que respiran os seres vivos."),
        ("Ten dióxido de carbono para a fotosíntese", "si", "As plantas usan o dióxido de carbono da atmosfera."),
        ("Ilumina a Terra pola noite", "non", "A atmosfera non dá luz: de noite non hai luz do sol."),
        ("Está feita de area e pedras", "non", "A atmosfera está feita de gases: nitróxeno, osíxeno e dióxido de carbono."),
    ],
}

CICLO = {
    "instrucion": "Ordena os pasos: como nace unha nube e como chove?",
    "pasos": [
        ("EVAPORACIÓN", "O sol quenta a auga e sobe vapor", "evaporacion",
         "Primeiro o sol quenta a auga e esta evapórase."),
        ("CONDENSACIÓN", "O vapor condénsase: nace a nube", "condensacion",
         "Despois o vapor condénsase en gotiñas e forma as nubes."),
        ("PRECIPITACIÓN", "Baixa a temperatura e a auga cae", "chuvia",
         "Ao final, cando baixa a temperatura, a auga cae: chuvia, neve ou sarabia."),
    ],
}

FENOMENOS = {
    "instrucion": "Une cada fenómeno atmosférico coa súa explicación.",
    "parellas": [
        ("Vento", "vento", "O aire móvese polos cambios de temperatura",
         "O vento é o aire que se move polos cambios de temperatura."),
        ("Nubes", "nubrado", "Gotas de auga da evaporación que se condensan",
         "As nubes fórmanse cando se condensan as gotas de auga da evaporación."),
        ("Neve e sarabia", "neve", "Auga en estado sólido que cae das nubes",
         "A neve e a sarabia son auga sólida; a chuvia é auga líquida."),
        ("Arco da vella", "arco", "As gotas de chuvia descompoñen a luz",
         "O arco da vella aparece cando as gotas de chuvia descompoñen a luz."),
        ("Auroras polares", "aurora", "Polos magnéticos da Terra e vento solar",
         "As auroras polares débense aos polos magnéticos e ao vento solar."),
    ],
}

# --- Misión 2
ELEM_FACT = {
    "instrucion": "É un elemento do clima ou un factor climático?",
    "caixas": [("elem", "ELEMENTOS do clima (mídense)", (56, 136, 208)),
               ("fact", "FACTORES climáticos (cambian o clima)", (232, 136, 40))],
    "tarxetas": [
        ("Temperatura", "elem", "A temperatura é un elemento do clima: mídese co termómetro."),
        ("Precipitacións", "elem", "As precipitacións son un elemento: mídense co pluviómetro."),
        ("Humidade", "elem", "A humidade é un elemento: mídese co higrómetro."),
        ("Vento", "elem", "O vento é un elemento: anemómetro e viravento."),
        ("Presión atmosférica", "elem", "A presión é un elemento: mídese co barómetro."),
        ("Latitude", "fact", "A latitude é un factor: distancia ao ecuador."),
        ("Altitude", "fact", "A altitude é un factor: altura sobre o nivel do mar."),
        ("Influencia do mar", "fact", "O mar é un factor: suaviza as temperaturas."),
        ("Relevo", "fact", "O relevo é un factor: as montañas frean ventos e nubes."),
    ],
}

INSTRUMENTOS = {
    "instrucion": "Une cada instrumento co que mide.",
    "parellas": [
        ("Termómetro", "termometro", "A temperatura, en graos centígrados (°C)",
         "O termómetro mide a temperatura."),
        ("Pluviómetro", "pluviometro", "As precipitacións, en litros por m²",
         "O pluviómetro recolle e mide a auga que cae."),
        ("Higrómetro", "higrometro", "A humidade: o vapor de auga do aire",
         "O higrómetro mide a humidade."),
        ("Anemómetro", "anemometro", "A velocidade do vento, en m/s",
         "O anemómetro xira co vento e mide a súa velocidade."),
        ("Viravento", "viravento", "A dirección do vento",
         "O viravento indica cara a onde sopra o vento."),
        ("Barómetro", "barometro", "A presión atmosférica, en milibares",
         "O barómetro mide a presión atmosférica."),
    ],
}

ALTITUDE = {
    "instrucion": "Ao subir, a temperatura baixa 1 °C cada 100 m. Que temperatura hai en cada altura?",
    "fondo": "montana_altitude",
    "ocos": [("15", "m500"), ("10", "m1000"), ("5", "m1500"), ("0", "m2000")],
    "tarxetas": [
        ("15 °C", "15", "A 500 m: 500 m son 5 veces 100 m, así que 5 °C menos que a 0 m."),
        ("10 °C", "10", "A 1000 m: son 10 °C menos que a nivel do mar."),
        ("5 °C", "5", "A 1500 m: son 15 °C menos que a nivel do mar."),
        ("0 °C", "0", "A 2000 m: son 20 °C menos que a nivel do mar."),
        ("25 °C", "x", "Ao subir a temperatura BAIXA, non sobe."),
        ("30 °C", "x", "Ao subir a temperatura BAIXA, non sobe."),
    ],
}

# --- Misión 3
ZONAS = {
    "instrucion": "Coloca as zonas climáticas da Terra e sinala onde está España.",
    "fondo": "globo_zonas",
    "ocos": [("fria", "fria_n"), ("temp", "temp_n"), ("calida", "calida"), ("temp", "temp_s"),
             ("fria", "fria_s"), ("espana", "espana")],
    "tarxetas": [
        ("Zona fría", "fria", "As zonas frías están preto dos polos."),
        ("Zona fría", "fria", "As zonas frías están preto dos polos."),
        ("Zona temperada", "temp", "As zonas temperadas están entre os trópicos e os círculos polares."),
        ("Zona temperada", "temp", "As zonas temperadas están entre os trópicos e os círculos polares."),
        ("Zona cálida", "calida", "A zona cálida está arredor do ecuador, entre os trópicos."),
        ("España", "espana", "España está no hemisferio norte, na zona temperada."),
    ],
}

CLIMAS_ESPANA = {
    "instrucion": "Arrastra cada clima ao seu lugar no mapa de España.",
    "fondo": "mapa_espana",
    "ocos": [("oceanico", "oceanico"), ("continental", "continental"), ("contmed", "contmed"),
             ("mediterraneo", "mediterraneo"), ("montana", "montana"), ("subtropical", "subtropical")],
    "tarxetas": [
        ("Oceánico", "oceanico", "O clima oceánico está no norte da Península (verde no mapa)."),
        ("Continental", "continental", "O continental ocupa a maior parte do interior (amarelo)."),
        ("Continental-mediterráneo", "contmed", "Está na submeseta sur e en boa parte de Andalucía (amarelo claro)."),
        ("Mediterráneo", "mediterraneo", "O mediterráneo está nas costas do sur e do leste (laranxa)."),
        ("De montaña", "montana", "O clima de montaña está nas montañas altas, como os Pireneos (morado)."),
        ("Subtropical", "subtropical", "O subtropical está nas illas Canarias (rosa)."),
    ],
}

CARACT_ESPANA = {
    "instrucion": "Une cada clima de España coas súas características.",
    "parellas": [
        ("Oceánico", "chuvia", "Temperaturas suaves e chuvia abundante todo o ano",
         "No oceánico os veráns son frescos, os invernos suaves e chove todo o ano."),
        ("Continental", "soleado", "Invernos moi fríos, veráns moi calorosos e pouca chuvia no verán",
         "No continental as temperaturas son extremas porque o mar queda lonxe."),
        ("Mediterráneo", "sol_nubes", "Veráns cálidos (máis de 27-30 °C) e chuvias irregulares",
         "No mediterráneo os veráns son cálidos e as chuvias irregulares, ás veces torrenciais."),
        ("De montaña", "neve", "Frío mesmo no verán e neve no inverno",
         "No clima de montaña as temperaturas baixan de cero no inverno e neva."),
        ("Subtropical", "palmeira", "Cálido todo o ano e poucas precipitacións",
         "No subtropical case non hai diferenza entre o verán e o inverno."),
    ],
}

# --- Misión 4: datos dos climogramas
CLIMOGRAMAS = {
    # Datos do libro (páx. 32)
    "ciudad_real": {"nome": "Ciudad Real", "altitude": 628, "tmedia": 14.7, "total": 396,
                    "clima": "Continental-mediterráneo",
                    "temp": [5.7, 7.7, 10.4, 12.3, 16.4, 21.3, 25.4, 25.0, 20.8, 14.9, 9.5, 6.7],
                    "prec": [36, 34, 28, 44, 43, 29, 9, 7, 22, 47, 42, 55]},
    # Santander (clima oceánico): datos aproximados
    "santander": {"nome": "Santander", "altitude": 5, "tmedia": 14.5, "total": 1104,
                  "clima": "Oceánico",
                  "temp": [9.7, 9.8, 11.3, 12.4, 14.9, 17.6, 19.8, 20.2, 18.6, 16.1, 12.6, 10.6],
                  "prec": [106, 92, 84, 99, 80, 58, 49, 70, 82, 117, 147, 120]},
}
MESES = ["Xaneiro", "Febreiro", "Marzo", "Abril", "Maio", "Xuño", "Xullo", "Agosto", "Setembro",
         "Outubro", "Novembro", "Decembro"]
MESES_CURTOS = ["X", "F", "M", "A", "M", "X", "X", "A", "S", "O", "N", "D"]

LER_CLIMOGRAMA = [
    {"tipo": "test", "p": "Que mes foi o máis caloroso en Ciudad Real?",
     "ops": ["Xullo", "Xaneiro", "Outubro"], "ok": 0,
     "exp": "Xullo, con 25,4 °C: é o punto máis alto da liña vermella."},
    {"tipo": "test", "p": "En que mes choveu menos?",
     "ops": ["Agosto", "Decembro", "Abril"], "ok": 0,
     "exp": "En agosto só caeron 7 mm: é a barra azul máis baixa."},
    {"tipo": "test", "p": "En que mes choveu máis?",
     "ops": ["Decembro", "Xullo", "Marzo"], "ok": 0,
     "exp": "En decembro caeron 55 mm: é a barra azul máis alta."},
    {"tipo": "test", "p": "Como son as precipitacións nos meses de verán?",
     "ops": ["Moi escasas", "Moi abundantes", "Iguais que no inverno"], "ok": 0,
     "exp": "En xullo e agosto case non chove: 9 e 7 mm."},
    {"tipo": "test", "p": "Cantos meses superaron os 20 °C?",
     "ops": ["4", "2", "8"], "ok": 0,
     "exp": "Xuño, xullo, agosto e setembro superaron os 20 °C."},
    {"tipo": "test", "p": "Cal é a temperatura media anual de Ciudad Real?",
     "ops": ["14,7 °C", "25,4 °C", "396 °C"], "ok": 0,
     "exp": "A temperatura media anual é 14,7 °C (396 son os mm de chuvia do ano)."},
]
CONSTRUIR = {"cidade": "ciudad_real", "barras": [6, 9, 11], "puntos": [3, 7]}
COMPARAR = [
    {"p": "Cal destes climogramas é dun clima OCEÁNICO?", "ok": "santander",
     "exp": "Santander: chove moito todo o ano e as temperaturas son suaves."},
    {"p": "En cal chove máis no verán?", "ok": "santander",
     "exp": "Santander ten barras azuis altas mesmo no verán; Ciudad Real case non ten chuvia."},
    {"p": "Cal ten os veráns máis calorosos?", "ok": "ciudad_real",
     "exp": "Ciudad Real chega a 25 °C en xullo; Santander non pasa de 20 °C."},
    {"p": "Onde haberá máis risco de incendio no verán?", "ok": "ciudad_real",
     "exp": "En Ciudad Real o verán é moi quente e moi seco: o risco de incendio é maior."},
]

# --- Misión 5
PAISAXES = {
    "instrucion": "Une cada paisaxe coa súa descrición.",
    "parellas": [
        ("", "paisaxe_oceanica", "Oceánica: árbores altas de folla caduca. A España verde",
         "A paisaxe oceánica é moi verde polas chuvias, con carballos e faias."),
        ("", "paisaxe_montana", "De montaña: pouca vexetación, musgos e matogueiras",
         "Na alta montaña fai frío e hai pouca vexetación."),
        ("", "paisaxe_mediterranea", "Mediterránea: piñeiros e aciñeiras de folla perenne",
         "A paisaxe mediterránea é seca e quente, con piñeiros e aciñeiras."),
        ("", "paisaxe_canaria", "Canaria: laurisilva, drago e palmeira canaria",
         "A paisaxe canaria ten volcáns, dragos e palmeiras."),
        ("", "paisaxe_transicion", "De transición: mestura de folla caduca e perenne",
         "A paisaxe de transición está no clima continental e mestura árbores."),
    ],
}

VEXETACION = {
    "instrucion": "En que paisaxe vive cada planta? Arrastra cada tarxeta.",
    "caixas": [("oc", "Paisaxe oceánica", (64, 160, 88)),
               ("med", "Paisaxe mediterránea", (216, 140, 48)),
               ("can", "Paisaxe canaria", (208, 88, 150)),
               ("mont", "Paisaxe de montaña", (130, 100, 190))],
    "tarxetas": [
        ("Carballo", "oc", "O carballo é de folla caduca e vive na paisaxe oceánica.", "carballo"),
        ("Faia", "oc", "A faia perde as follas no outono: paisaxe oceánica.", "faia"),
        ("Piñeiro", "med", "O piñeiro, de folla perenne, é típico da paisaxe mediterránea.", "pineiro"),
        ("Aciñeira", "med", "A aciñeira é de folla perenne: paisaxe mediterránea.", "acineira"),
        ("Drago", "can", "O drago é unha árbore típica das illas Canarias.", "drago"),
        ("Palmeira canaria", "can", "A palmeira canaria vive nas zonas máis áridas das Canarias.", "palmeira"),
        ("Musgo", "mont", "Na alta montaña só medran musgos e plantas pequenas.", "musgo"),
        ("Matogueiras pequenas", "mont", "Na alta montaña a vexetación é escasa: pequenas matogueiras.", "matogueira"),
    ],
}

# --- Misión 6
GALICIA = {
    "instrucion": "Arrastra cada variedade de clima oceánico ao seu lugar no mapa de Galicia.",
    "fondo": "mapa_galicia",
    "ocos": [("litoral", "litoral"), ("interior", "interior"), ("montana", "montana")],
    "tarxetas": [
        ("Oceánico litoral", "litoral", "O oceánico litoral está nas zonas costeiras (verde claro)."),
        ("Oceánico de interior", "interior", "O oceánico de interior está no centro, lonxe da costa (verde escuro)."),
        ("Oceánico de montaña", "montana", "O de montaña está nas serras do leste e do sur (morado)."),
    ],
}

CARACT_GALICIA = {
    "instrucion": "De que variedade do clima galego é cada característica?",
    "caixas": [("lit", "Oceánico litoral", (96, 184, 104)),
               ("int", "Oceánico de interior", (40, 120, 72)),
               ("mont", "Oceánico de montaña", (140, 104, 184))],
    "tarxetas": [
        ("Temperaturas suaves todo o ano", "lit", "Na costa o mar suaviza as temperaturas todo o ano."),
        ("Chove moito, veráns máis secos ao sur", "lit", "No litoral chove todo o ano; máis ao sur, os veráns son máis secos."),
        ("Invernos fríos e veráns calorosos", "int", "No interior faise máis frío no inverno e máis calor no verán."),
        ("Menos chuvia que na costa e algo de neve", "int", "No interior chove menos que no litoral e pode nevar."),
        ("Nevadas frecuentes no inverno", "mont", "Nas montañas neva con frecuencia no inverno."),
        ("Invernos fríos e veráns suaves", "mont", "Na montaña os veráns son suaves e os invernos fríos."),
    ],
}

ESTACION_USOS = {
    "instrucion": "Para que serve unha estación meteorolóxica?",
    "caixas": [("si", "SI, serve para isto", (48, 160, 88)),
               ("non", "NON serve para isto", (208, 72, 64))],
    "tarxetas": [
        ("Predicir o tempo", "si", "Cos datos da estación predise o tempo a curto e medio prazo."),
        ("Crear alertas de fenómenos adversos", "si", "Serve para avisar de fenómenos adversos."),
        ("Axudar á agricultura e á gandería", "si", "Dá información útil para a agricultura e a gandería."),
        ("Medir o cambio climático", "si", "Mide os efectos do cambio climático a longo prazo."),
        ("Apagar os incendios", "non", "A estación mide o tempo; os incendios apáganos as brigadas."),
        ("Facer que chova", "non", "A estación só mide: non pode cambiar o tempo."),
    ],
}

# --- Misión 7
CAUSAS = {
    "instrucion": "É unha causa ou unha consecuencia do cambio climático?",
    "caixas": [("causa", "CAUSAS", (124, 72, 160)),
               ("cons", "CONSECUENCIAS", (208, 96, 56))],
    "tarxetas": [
        ("Gases dos combustibles fósiles (coches, fábricas...)", "causa", "Queimar combustibles fósiles aumenta os gases de efecto invernadoiro."),
        ("Deforestación: talar bosques", "causa", "Sen bosques absórbese menos dióxido de carbono."),
        ("Consumo excesivo", "causa", "O noso estilo de vida ten un grande impacto no planeta."),
        ("Máis calor e máis incendios", "cons", "Ao subir as temperaturas, hai máis incendios."),
        ("Secas e inundacións extremas", "cons", "Aumentan os fenómenos meteorolóxicos extremos."),
        ("Sobe o nivel do mar", "cons", "O desxeo e o quentamento da auga fan subir o mar."),
        ("Especies en perigo de extinción", "cons", "Moitas especies non se adaptan aos cambios."),
    ],
}

MEDIDAS = {
    "instrucion": "Estas accións axudan ao planeta ou prexudícano?",
    "caixas": [("ben", "AXUDA ao planeta", (48, 160, 88)),
               ("mal", "PREXUDICA ao planeta", (208, 72, 64))],
    "tarxetas": [
        ("Usar enerxías renovables", "ben", "As enerxías renovables (sol, vento) non queiman combustibles fósiles."),
        ("Reforestar os bosques", "ben", "As árbores absorben dióxido de carbono."),
        ("Ir en bici ou en transporte público", "ben", "A mobilidade sostible reduce os gases."),
        ("Apagar as luces que non usamos", "ben", "Aforrar enerxía axuda ao planeta."),
        ("Usar o coche para todo", "mal", "O coche queima combustibles fósiles."),
        ("Talar bosques", "mal", "A deforestación empeora o cambio climático."),
        ("Deixar a calefacción acesa sen ninguén", "mal", "Malgastar enerxía produce máis gases."),
    ],
}

TIX = {
    "instrucion": "As TIX (tecnoloxías da información xeográfica): une cada unha co que fai.",
    "parellas": [
        ("Teledetección", "satelite", "Observa a Terra desde satélites",
         "A teledetección obtén datos da Terra desde lonxe."),
        ("GPS", "gps", "Indica a posición exacta dun lugar",
         "O GPS é un sistema de posicionamento global."),
        ("SIX", "mapa", "Fai mapas cos datos dun territorio",
         "Os SIX (sistemas de información xeográfica) relacionan datos nun mapa."),
        ("Simulador 3D", "lume", "Predí cara a onde se moverá o lume",
         "O simulador 3D predí o comportamento do lume para tomar mellores decisións."),
    ],
}

# ================================================================ MAPA DO TEMPO (Misión 1)

TEMPO = {
    "soleado": ("Soleado", "fará sol"),
    "sol_nubes": ("Sol e nubes", "haberá sol e nubes"),
    "nubrado": ("Nubrado", "estará nubrado"),
    "chuvia": ("Chuvia", "choverá"),
    "neve": ("Neve", "nevará"),
    "treboada": ("Treboada", "haberá treboada"),
    "vento": ("Vento", "fará moito vento"),
}
# Lugares do mapa: clave -> (nome, preposición, columna, fila)
LUGARES = {
    "montana": ("MONTAÑA", "Na montaña", 27, 2),
    "lago": ("LAGO", "No lago", 10, 8),
    "aldea": ("ALDEA", "Na aldea", 19, 8),
    "bosque": ("BOSQUE", "No bosque", 26, 12),
}

# ================================================================ LUMES (Misión 5)

TIPS = {
    "inicio": "Toca un lume para que Nubi voe ata el e responde a pregunta.",
    "apagado": "Lume apagado! A chuvia molla a vexetación e arrefría as chamas.",
    "vento": "Cambia o VENTO! A frecha da VELETA indica cara a onde sopra. O vento estende o lume.",
    "globo": "O dirixible da Banda Tisne! Tócao para mollalo.",
    "raio": "Un raio de sol! Tócao e responde para crear un arco da vella.",
    "arco": "ARCO DA VELLA! As gotas de chuvia descompoñen a luz do sol.",
    "medrou": "O lume medrou! Tócao de novo para outra pregunta.",
}
QUIPS_CHISPA = ["Faíscas para todos!", "Ja, ja! Que mato tan seco!", "Tubiño, máis fume!"]
QUIPS_HUIDA = ["O meu sombreiro de copa! Empapado!", "Retirada, Tubiño!", "Volveremos con máis fume!"]

ATAQUES_BARON = ["NUBE DE FUME", "FAÍSCA SECA", "VAGA DE CALOR", "VENTO ARDENTE", "TALA DE BOSQUES"]
ATAQUES_NUBI = ["CHUVIA FORTE", "NEVARADA", "REFACHO DE VENTO", "SARABIA", "ARCO DA VELLA"]

# ================================================================ MISIÓNS

MISIONS = [
    {"titulo": "A atmosfera e o tempo", "icona": "terra", "paxinas": "26-27",
     "pasos": [("dialogo", "M1_INTRO"), ("clasificar", "FUNCIONS"), ("ordenar", "CICLO"),
               ("unir", "FENOMENOS"), ("mapatempo", None), ("dialogo", "M1_FIN")]},
    {"titulo": "Elementos e factores", "icona": "termometro", "paxinas": "28-29",
     "pasos": [("dialogo", "M2_INTRO"), ("clasificar", "ELEM_FACT"), ("unir", "INSTRUMENTOS"),
               ("colocar", "ALTITUDE"), ("quiz", "P2"), ("dialogo", "M2_FIN")]},
    {"titulo": "Os climas de España", "icona": "mapa_espana", "paxinas": "30-31",
     "pasos": [("dialogo", "M3_INTRO"), ("colocar", "ZONAS"), ("colocar", "CLIMAS_ESPANA"),
               ("unir", "CARACT_ESPANA"), ("quiz", "P3"), ("dialogo", "M3_FIN")]},
    {"titulo": "Os climogramas", "icona": "climograma", "paxinas": "32-33",
     "pasos": [("dialogo", "M4_INTRO"), ("climograma", "ler"), ("climograma", "construir"),
               ("climograma", "comparar"), ("dialogo", "M4_FIN")]},
    {"titulo": "As paisaxes", "icona": "paisaxe_oceanica", "paxinas": "34-35",
     "pasos": [("dialogo", "M5_INTRO"), ("unir", "PAISAXES"), ("clasificar", "VEXETACION"),
               ("lumes", "P5"), ("dialogo", "M5_FIN")]},
    {"titulo": "O clima de Galicia", "icona": "mapa_galicia", "paxinas": "36-37",
     "pasos": [("dialogo", "M6_INTRO"), ("colocar", "GALICIA"), ("clasificar", "CARACT_GALICIA"),
               ("clasificar", "ESTACION_USOS"), ("quiz", "P6"), ("dialogo", "M6_FIN")]},
    {"titulo": "O clima está cambiando", "icona": "fabrica", "paxinas": "38-39",
     "pasos": [("dialogo", "M7_INTRO"), ("clasificar", "CAUSAS"), ("clasificar", "MEDIDAS"),
               ("unir", "TIX"), ("dialogo", "M7_PRE_BATALLA"), ("batalla", "TODAS"), ("dialogo", "M7_FIN")]},
]
PREGUNTAS_QUIZ = 5   # preguntas por cada repaso ("quiz")

# ================================================================ PREGUNTAS
# tipo: "test" (escoller), "vf" (verdadeiro/falso), "oco" (completar a frase)
# img: ilustración opcional. En "test"/"oco" a correcta é a de índice "ok" (bárallanse ao xogar).

P1 = [
    {"tipo": "test", "p": "Que é a atmosfera?",
     "ops": ["A capa de gases que rodea a Terra", "A auga dos mares e océanos", "O chan onde medran as plantas"], "ok": 0,
     "exp": "A atmosfera é a capa de gases que rodea a Terra: sobre todo nitróxeno, osíxeno e dióxido de carbono."},
    {"tipo": "test", "img": "terra", "p": "Como se chama a capa azul que rodea a Terra na imaxe?",
     "ops": ["A atmosfera", "O océano", "A Lúa"], "ok": 0,
     "exp": "É a atmosfera, a capa de gases imprescindible para a vida."},
    {"tipo": "test", "p": "Que gas necesitamos para respirar?",
     "ops": ["O osíxeno", "O fume", "O vapor das fábricas"], "ok": 0,
     "exp": "Respiramos osíxeno. A atmosfera contén os gases que necesitan os seres vivos."},
    {"tipo": "test", "p": "Que fai a atmosfera coas radiacións solares prexudiciais?",
     "ops": ["Fíltraas", "Multiplícaas", "Gárdaas para a noite"], "ok": 0,
     "exp": "A atmosfera filtra as radiacións solares que nos poden facer dano."},
    {"tipo": "test", "p": "Como se produce o vento?",
     "ops": ["O aire móvese polos cambios de temperatura", "As árbores moven as follas", "A auga do mar empurra o aire"], "ok": 0,
     "exp": "O aire da atmosfera móvese polos cambios de temperatura e así se produce o vento."},
    {"tipo": "test", "img": "vento", "p": "Que fenómeno atmosférico move as follas na imaxe?",
     "ops": ["O vento", "A chuvia", "A neve"], "ok": 0,
     "exp": "É o vento: o aire en movemento."},
    {"tipo": "oco", "p": "As nubes fórmanse cando se ___ as gotas de auga presentes na atmosfera.",
     "ops": ["condensan", "queiman", "esconden"], "ok": 0,
     "exp": "As gotas de auga condénsanse e forman as nubes."},
    {"tipo": "test", "img": "nubes", "p": "Que lle pasa á auga do lago cando a quenta o sol?",
     "ops": ["Evapórase e sobe", "Conxélase", "Convértese en area"], "ok": 0,
     "exp": "Coa calor do sol, a auga evapórase e sobe en forma de vapor."},
    {"tipo": "test", "p": "Cando cae a auga das nubes cara á superficie?",
     "ops": ["Cando baixan as temperaturas", "Cando fai moita calor", "Cando non hai nubes"], "ok": 0,
     "exp": "Cando descenden as temperaturas, a auga das nubes cae en forma de chuvia, neve ou sarabia."},
    {"tipo": "oco", "p": "A chuvia é auga en estado ___.",
     "ops": ["líquido", "sólido", "gasoso"], "ok": 0,
     "exp": "A chuvia é auga líquida."},
    {"tipo": "test", "img": "sarabia", "p": "Que tipo de precipitación ves na imaxe?",
     "ops": ["Sarabia", "Chuvia", "Vento"], "ok": 0,
     "exp": "Son bolas de xeo: sarabia, auga en estado sólido."},
    {"tipo": "test", "img": "neve", "p": "En que estado está a auga que cae na imaxe?",
     "ops": ["Sólido", "Líquido", "Gasoso"], "ok": 0,
     "exp": "É neve: auga en estado sólido."},
    {"tipo": "test", "img": "arco", "p": "Por que aparece o arco da vella?",
     "ops": ["As gotas de chuvia descompoñen a luz", "O vento pinta as nubes", "O sol queima o ceo"], "ok": 0,
     "exp": "Cando chove, as gotas actúan como espellos que dispersan e descompoñen a luz."},
    {"tipo": "test", "img": "aurora", "p": "Que fenómeno atmosférico ves na imaxe?",
     "ops": ["Auroras polares", "Arco da vella", "Treboada"], "ok": 0,
     "exp": "Son auroras polares: só se ven nalgúns puntos concretos do planeta."},
    {"tipo": "vf", "p": "As auroras polares pódense ver en calquera lugar do planeta.", "ok": False,
     "exp": "Falso. Só se poden ver en puntos concretos do planeta."},
    {"tipo": "test", "p": "Que é o tempo atmosférico?",
     "ops": ["O estado da atmosfera nun momento e lugar", "O que pasa durante moitos anos", "A hora que marca o reloxo"], "ok": 0,
     "exp": "O tempo atmosférico é o estado da atmosfera nun momento e lugar determinado."},
    {"tipo": "test", "p": "Que ciencia estuda o tempo atmosférico e fai predicións?",
     "ops": ["A meteoroloxía", "A xeoloxía", "A astronomía"], "ok": 0,
     "exp": "A meteoroloxía estuda o tempo e prognostica o das próximas 24 ou 48 horas."},
    {"tipo": "test", "icona": "treboada", "p": "Que significa este símbolo do mapa do tempo?",
     "ops": ["Treboada", "Neve", "Sol e nubes"], "ok": 0,
     "exp": "A nube escura cun lóstrego é o símbolo de treboada."},
    {"tipo": "test", "p": "Por que consultamos a previsión do tempo cada día?",
     "ops": ["Para saber que roupa poñer", "Para saber que hora é", "Para saber cantos anos temos"], "ok": 0,
     "exp": "O tempo condiciona o noso día: que roupa usar, se levar paraugas, lentes de sol..."},
    {"tipo": "test", "p": "Que fenómenos aumentaron nos últimos anos?",
     "ops": ["Os extremos: vagas de calor, chuvias torrenciais...", "Os arcos da vella", "As auroras polares"], "ok": 0,
     "exp": "Aumentaron os fenómenos extremos: nevadas, vagas de calor, chuvias torrenciais, tornados..."},
]

P2 = [
    {"tipo": "test", "p": "Que diferenza hai entre o tempo e o clima?",
     "ops": ["O tempo é o de hoxe; o clima, o habitual en moitos anos", "Son o mesmo", "O clima cambia cada hora"], "ok": 0,
     "exp": "O clima é o conxunto de condicións frecuentes nun lugar, estudadas durante varias décadas."},
    {"tipo": "test", "img": "termometro", "p": "Que instrumento é este?",
     "ops": ["Termómetro", "Pluviómetro", "Barómetro"], "ok": 0,
     "exp": "O termómetro mide a temperatura en graos centígrados (°C)."},
    {"tipo": "test", "img": "pluviometro", "p": "Para que serve este instrumento?",
     "ops": ["Para medir as precipitacións", "Para medir o vento", "Para medir a temperatura"], "ok": 0,
     "exp": "O pluviómetro mide a auga que cae, en litros por m²."},
    {"tipo": "test", "img": "anemometro", "p": "Que mide o anemómetro?",
     "ops": ["A velocidade do vento", "A dirección do vento", "A humidade"], "ok": 0,
     "exp": "O anemómetro mide a velocidade do vento en metros por segundo (m/s)."},
    {"tipo": "test", "img": "viravento", "p": "Que nos indica o viravento?",
     "ops": ["A dirección do vento", "A temperatura", "A presión"], "ok": 0,
     "exp": "O viravento indica cara a onde sopra o vento."},
    {"tipo": "test", "img": "barometro", "p": "Que mide o barómetro?",
     "ops": ["A presión atmosférica", "A chuvia", "As nubes"], "ok": 0,
     "exp": "O barómetro mide a presión atmosférica en milibares."},
    {"tipo": "test", "p": "Que é a nebulosidade?",
     "ops": ["A cantidade de nubes", "A cantidade de chuvia", "O peso do aire"], "ok": 0,
     "exp": "A nebulosidade é a cantidade de nubes."},
    {"tipo": "test", "p": "Que é a presión atmosférica?",
     "ops": ["O peso do aire sobre a superficie", "A forza da chuvia", "A velocidade do vento"], "ok": 0,
     "exp": "É o peso que exerce unha masa de aire sobre a superficie terrestre."},
    {"tipo": "test", "img": "latitude", "p": "Onde fai máis calor segundo a latitude?",
     "ops": ["Preto do ecuador", "Preto dos polos", "Igual en todas partes"], "ok": 0,
     "exp": "Canto máis preto do ecuador, máis cálido; canto máis lonxe, máis frío."},
    {"tipo": "test", "p": "Que é a latitude?",
     "ops": ["A distancia dun lugar ao ecuador", "A altura sobre o nivel do mar", "A distancia ao mar"], "ok": 0,
     "exp": "A latitude é a distancia desde calquera punto da Terra ao ecuador (paralelo 0°)."},
    {"tipo": "test", "img": "altitude", "p": "Que pasa coa temperatura cando subimos unha montaña?",
     "ops": ["Baixa", "Sobe", "Non cambia"], "ok": 0,
     "exp": "A maior altitude, menor temperatura: baixa 1 °C cada 100 metros."},
    {"tipo": "test", "img": "mar", "p": "Onde é o clima máis suave?",
     "ops": ["Preto do mar", "No interior, lonxe do mar", "No alto dunha montaña"], "ok": 0,
     "exp": "A auga do mar quéntase máis devagar que a terra e suaviza as temperaturas da costa."},
    {"tipo": "test", "img": "relevo", "p": "Que fan as montañas co vento e as nubes?",
     "ops": ["Frean o seu paso", "Fanos máis rápidos", "Fanos desaparecer"], "ok": 0,
     "exp": "As montañas frean o paso dos ventos e das nubes."},
    {"tipo": "vf", "p": "A latitude, a altitude, o mar e o relevo son factores climáticos.", "ok": True,
     "exp": "Verdadeiro. Son os condicionantes que fan que o clima sexa distinto en cada zona."},
]

P3 = [
    {"tipo": "test", "img": "globo", "p": "En que zona climática da Terra está España?",
     "ops": ["Na zona temperada", "Na zona cálida", "Na zona fría"], "ok": 0,
     "exp": "España está na zona temperada debido á súa latitude."},
    {"tipo": "test", "p": "Que clima ocupa a maior parte da Península?",
     "ops": ["Continental", "Oceánico", "De montaña"], "ok": 0,
     "exp": "O clima continental ocupa a maior parte da superficie peninsular."},
    {"tipo": "test", "p": "Por que no clima continental as temperaturas son extremas?",
     "ops": ["Porque o mar queda lonxe", "Porque hai moitas praias", "Porque chove moito"], "ok": 0,
     "exp": "Hai pouca influencia do mar: invernos moi fríos e veráns moi calorosos."},
    {"tipo": "test", "p": "Onde se dá o clima mediterráneo?",
     "ops": ["Nas costas do sur e do leste", "No norte", "Nas montañas altas"], "ok": 0,
     "exp": "O clima mediterráneo localízase nas zonas de costa do sur e do leste peninsular."},
    {"tipo": "test", "p": "Onde hai clima subtropical en España?",
     "ops": ["Nas illas Canarias", "En Galicia", "Nos Pireneos"], "ok": 0,
     "exp": "O clima subtropical dáse no arquipélago canario, máis próximo á zona cálida."},
    {"tipo": "test", "p": "Como é o clima de montaña no inverno?",
     "ops": ["Moi frío, baixo cero e con neve", "Caloroso e seco", "Suave e sen neve"], "ok": 0,
     "exp": "As temperaturas baixan de cero no inverno e as precipitacións son de neve."},
    {"tipo": "vf", "p": "No clima oceánico chove moito durante todo o ano.", "ok": True,
     "exp": "Verdadeiro. As precipitacións son abundantes todo o ano, aínda que menores no verán."},
    {"tipo": "vf", "p": "No clima mediterráneo os veráns son frescos.", "ok": False,
     "exp": "Falso. Os veráns son cálidos e superan os 27-30 °C."},
    {"tipo": "test", "p": "En que climas hai máis risco de incendio no verán?",
     "ops": ["Nos de veráns quentes e secos", "Nos de montaña nevada", "Onde chove todo o ano"], "ok": 0,
     "exp": "A calor e a seca fan que a vexetación arda con facilidade."},
    {"tipo": "test", "p": "Segundo Greenpeace, que é necesario contra os incendios forestais?",
     "ops": ["Investir en prevención", "Plantar máis mato seco", "Facer máis fogueiras"], "ok": 0,
     "exp": "España é un dos países europeos máis afectados polos incendios: hai que investir en prevención."},
]

P4 = [
    {"tipo": "test", "p": "Que estuda a climatoloxía?",
     "ops": ["O clima e os seus cambios a longo prazo", "O tempo de mañá", "As rochas"], "ok": 0,
     "exp": "A climatoloxía estuda o clima ao longo do tempo; non fai previsións inmediatas."},
    {"tipo": "test", "p": "Que dous elementos do clima representa un climograma?",
     "ops": ["Temperaturas e precipitacións", "Vento e presión", "Nubes e humidade"], "ok": 0,
     "exp": "Os climogramas representan as temperaturas e as precipitacións de todo un ano."},
    {"tipo": "test", "p": "Como se debuxan as precipitacións nun climograma?",
     "ops": ["Con barras azuis", "Cunha liña vermella", "Con estrelas"], "ok": 0,
     "exp": "As precipitacións represéntanse con barras azuis."},
    {"tipo": "test", "p": "Que instrumentos necesitamos para facer un climograma?",
     "ops": ["Termómetro e pluviómetro", "Barómetro e viravento", "Higrómetro e anemómetro"], "ok": 0,
     "exp": "As temperaturas mídense co termómetro e as precipitacións co pluviómetro."},
    {"tipo": "vf", "p": "O vento axuda a apagar os incendios.", "ok": False,
     "exp": "Falso. O vento dificulta moito a extinción porque fai que o lume se estenda máis rápido."},
]

P5 = [
    {"tipo": "test", "p": "Que é unha paisaxe?",
     "ops": ["Unha zona da Terra que vemos en conxunto", "Só o ceo", "Un mapa do tempo"], "ok": 0,
     "exp": "É unha área da superficie terrestre froito do clima, a flora, a fauna e o relevo."},
    {"tipo": "test", "img": "paisaxe_oceanica", "p": "Que paisaxe é esta?",
     "ops": ["Oceánica", "Mediterránea", "Canaria"], "ok": 0,
     "exp": "Paisaxe oceánica: verde, con árbores altas de folla caduca. É a España verde."},
    {"tipo": "test", "img": "paisaxe_mediterranea", "p": "Que paisaxe é esta?",
     "ops": ["Mediterránea", "Oceánica", "De montaña"], "ok": 0,
     "exp": "Paisaxe mediterránea: piñeiros e aciñeiras de folla perenne, adaptados á calor."},
    {"tipo": "test", "img": "paisaxe_canaria", "p": "Que paisaxe é esta?",
     "ops": ["Canaria", "De transición", "Oceánica"], "ok": 0,
     "exp": "Paisaxe canaria: drago, palmeira canaria e laurisilva."},
    {"tipo": "test", "img": "paisaxe_montana", "p": "Como é a vexetación da alta montaña?",
     "ops": ["Escasa: musgos e matogueiras", "Unha selva moi densa", "Palmeiras"], "ok": 0,
     "exp": "Na alta montaña a vexetación é escasa: musgos e pequenas matogueiras."},
    {"tipo": "test", "p": "Por que o norte de España se chama «a España verde»?",
     "ops": ["Chove moito e hai moita vexetación", "As casas son verdes", "Non hai montañas"], "ok": 0,
     "exp": "A abundancia de precipitacións fai que a vexetación sexa abundante."},
    {"tipo": "test", "p": "Que árbores teñen folla caduca?",
     "ops": ["O carballo e a faia", "O piñeiro e a aciñeira", "O drago e a palmeira"], "ok": 0,
     "exp": "O carballo e a faia perden as follas no outono: son de folla caduca."},
    {"tipo": "vf", "p": "As árbores de folla perenne perden as follas no outono.", "ok": False,
     "exp": "Falso. Conservan as follas todo o ano, como o piñeiro e a aciñeira."},
    {"tipo": "test", "img": "drago", "p": "Onde vive esta árbore, o drago?",
     "ops": ["Nas illas Canarias", "En Galicia", "Nos Pireneos"], "ok": 0,
     "exp": "O drago é típico da paisaxe canaria."},
    {"tipo": "test", "p": "Como é a paisaxe de transición?",
     "ops": ["Mestura folla caduca e perenne", "Só ten musgo", "Só ten palmeiras"], "ok": 0,
     "exp": "Combina folla caduca e perenne e adáptase ás secas do clima continental."},
    {"tipo": "test", "p": "Cal é unha das principais causas dos incendios?",
     "ops": ["A abundancia de matogueiras", "A chuvia", "A neve"], "ok": 0,
     "exp": "Destacan o cambio climático, a abundancia de matogueiras e a mala xestión da urbanización do monte."},
    {"tipo": "test", "p": "Que podes facer para previr os incendios forestais?",
     "ops": ["Non facer lume no monte", "Tirar vidros no monte", "Queimar lixo no bosque"], "ok": 0,
     "exp": "Nunca se debe facer lume nin tirar lixo ou vidros no monte."},
    {"tipo": "test", "p": "Se ves un incendio, a que número debes chamar?",
     "ops": ["Ao 112", "Ao 010", "A ningún"], "ok": 0,
     "exp": "O 112 é o teléfono de emerxencias."},
    {"tipo": "vf", "p": "Limpar o monte de mato seco axuda a previr incendios.", "ok": True,
     "exp": "Verdadeiro. O mato seco arde con moita facilidade."},
    {"tipo": "test", "p": "Que árbores atopamos na paisaxe mediterránea?",
     "ops": ["Piñeiros e aciñeiras", "Carballos e faias", "Dragos e palmeiras"], "ok": 0,
     "exp": "Na paisaxe mediterránea hai árbores de folla perenne como piñeiros e aciñeiras."},
]

P6 = [
    {"tipo": "test", "p": "Que clima ten case toda Galicia?",
     "ops": ["Oceánico", "Mediterráneo", "Subtropical"], "ok": 0,
     "exp": "Galicia está no noroeste da Península e case todo o territorio ten clima oceánico."},
    {"tipo": "test", "img": "mapa_galicia", "p": "Que tres variedades de clima hai en Galicia?",
     "ops": ["Oceánico litoral, de interior e de montaña", "Mediterráneo, continental e canario", "Só unha"], "ok": 0,
     "exp": "Litoral na costa, de interior no centro e de montaña nas serras."},
    {"tipo": "test", "p": "Como son as temperaturas no clima oceánico litoral?",
     "ops": ["Suaves todo o ano", "Moi frías todo o ano", "Moi quentes todo o ano"], "ok": 0,
     "exp": "Na costa as temperaturas son suaves durante todo o ano."},
    {"tipo": "test", "p": "Onde poden caer nevadas en Galicia?",
     "ops": ["No interior e nas montañas", "Só na praia", "Nunca neva"], "ok": 0,
     "exp": "No interior pode nevar no inverno e na montaña as nevadas son frecuentes."},
    {"tipo": "test", "p": "Que árbores son autóctonas de Galicia?",
     "ops": ["Carballo, castiñeiro e bidueiro", "O eucalipto", "A palmeira e o drago"], "ok": 0,
     "exp": "Carballo, bidueiro, castiñeiro, freixo, ameneiro e salgueiro: árbores de folla caduca."},
    {"tipo": "vf", "p": "Os eucaliptos son unha especie autóctona de Galicia.", "ok": False,
     "exp": "Falso. Hai plantacións de eucaliptos e piñeiros, pero non son especies autóctonas."},
    {"tipo": "test", "img": "estacion", "p": "Que é unha estación meteorolóxica?",
     "ops": ["Instrumentos que miden e rexistran o tempo", "Unha estación de tren", "Un parque de bombeiros"], "ok": 0,
     "exp": "É unha instalación con instrumentos que miden e rexistran datos meteorolóxicos."},
    {"tipo": "test", "p": "Hai 35 °C, a humidade é moi baixa e sopra vento forte. Que risco de incendio hai?",
     "ops": ["Alto", "Baixo", "Ningún"], "ok": 0,
     "exp": "Calor, sequidade e vento fan que o risco de incendio sexa alto."},
    {"tipo": "test", "p": "Chove, fai fresco e non hai vento. Que risco de incendio hai?",
     "ops": ["Baixo", "Alto", "Extremo"], "ok": 0,
     "exp": "Coa chuvia e o fresco, a vexetación está mollada e o risco é baixo."},
    {"tipo": "test", "p": "Que ten Galicia desde 2023 contra os incendios?",
     "ops": ["Un dispositivo contra o lume todo o ano", "Bombeiros só no verán", "Nada"], "ok": 0,
     "exp": "Desde 2023 Galicia conta cun dispositivo público de loita contra o lume activo todo o ano."},
    {"tipo": "test", "p": "Onde se consulta o índice de risco diario de incendio en Galicia?",
     "ops": ["Na web da Xunta de Galicia", "Nun libro de contos", "No mapa de estradas"], "ok": 0,
     "exp": "A Xunta de Galicia publica cada día o índice de risco de incendio forestal."},
]

P7 = [
    {"tipo": "test", "p": "Que é o cambio climático?",
     "ops": ["Un cambio no clima pola actividade humana", "O cambio do tempo de hoxe a mañá", "O paso do verán ao inverno"], "ok": 0,
     "exp": "É un cambio no clima debido á actividade humana, que altera a composición da atmosfera."},
    {"tipo": "test", "img": "fabrica", "p": "Que actividades producen gases de efecto invernadoiro?",
     "ops": ["As que queiman combustibles fósiles", "Plantar árbores", "Ir en bicicleta"], "ok": 0,
     "exp": "O transporte, a calefacción e as fábricas queiman combustibles fósiles."},
    {"tipo": "test", "p": "Por que a deforestación empeora o cambio climático?",
     "ops": ["Hai menos árbores para absorber CO₂", "Fai que chova máis", "Arrefría o planeta"], "ok": 0,
     "exp": "Sen bosques, a natureza absorbe menos dióxido de carbono."},
    {"tipo": "test", "p": "Cal é unha consecuencia do cambio climático?",
     "ops": ["Máis temperaturas e máis incendios", "Máis xeo nos polos", "Menos secas"], "ok": 0,
     "exp": "Aumentan as temperaturas, os incendios e os fenómenos extremos."},
    {"tipo": "test", "p": "Por que sobe o nivel do mar?",
     "ops": ["Polo desxeo e o quentamento da auga", "Porque chove no mar", "Polos peixes"], "ok": 0,
     "exp": "O desxeo e o quentamento da auga fan subir o nivel do mar."},
    {"tipo": "test", "p": "Que medida axuda contra o cambio climático?",
     "ops": ["Usar enerxías renovables", "Talar bosques", "Usar o coche para todo"], "ok": 0,
     "exp": "Enerxías renovables, reforestar, transporte público e mobilidade sostible."},
    {"tipo": "test", "p": "Canto aumentaron as temperaturas medias na nosa comunidade?",
     "ops": ["Case dous graos", "Vinte graos", "Nada"], "ok": 0,
     "exp": "As temperaturas medias aumentaron case dous graos nos últimos anos."},
    {"tipo": "vf", "p": "Nos últimos anos as chuvias torrenciais son máis frecuentes.", "ok": True,
     "exp": "Verdadeiro. E os períodos de seca acentuáronse nos últimos cinco anos."},
    {"tipo": "test", "p": "Que significa TIX?",
     "ops": ["Tecnoloxías da información xeográfica", "Televisión internacional", "Tren interurbano"], "ok": 0,
     "exp": "As TIX recollen e analizan datos ambientais: teledetección, GPS e SIX."},
    {"tipo": "test", "img": "satelite", "p": "Que fai a teledetección?",
     "ops": ["Observa a Terra desde satélites", "Mide a chuvia nun xardín", "Apaga lumes"], "ok": 0,
     "exp": "A teledetección obtén datos da Terra desde lonxe, por exemplo desde satélites."},
    {"tipo": "test", "p": "Para que se usou un simulador 3D feito coas TIX?",
     "ops": ["Para predicir cara a onde vai o lume", "Para xogar ao fútbol", "Para medir a temperatura"], "ok": 0,
     "exp": "Predí como se comportará o lume e cara a onde irá, para tomar mellores decisións."},
    {"tipo": "test", "p": "Como axudan as TIX cos furacáns e as chuvias torrenciais?",
     "ops": ["Permiten identificalos e previlos", "Fanos máis fortes", "Non serven para nada"], "ok": 0,
     "exp": "Coas TIX pódense identificar e previr fenómenos meteorolóxicos extremos."},
]

POOLS = {"P1": P1, "P2": P2, "P3": P3, "P4": P4, "P5": P5, "P6": P6, "P7": P7}
POOLS["TODAS"] = P1 + P2 + P3 + P4 + P5 + P6 + P7
