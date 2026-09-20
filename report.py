"""
report.py

Generador de informe técnico académico para el análisis
de estabilidad de una cuña de falla planar.

Proyecto: Programación II - Ingeniería Civil
Autor: Jeison Steven Perez
Universidad Distrital Francisco José de Caldas
Facultad Tecnológica
Bogotá D.C. - 2026
"""

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle,
    PageBreak,
    KeepTogether
)

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.units import cm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics


# ==========================================================
# CONFIGURACIÓN DE FUENTE
# ==========================================================

# Se intenta utilizar Times New Roman si está disponible.
# Si no está disponible, se utiliza Times-Roman de ReportLab.

try:
    pdfmetrics.registerFont(
        TTFont(
            "TimesNewRoman",
            "C:/Windows/Fonts/times.ttf"
        )
    )

    pdfmetrics.registerFont(
        TTFont(
            "TimesNewRoman-Bold",
            "C:/Windows/Fonts/timesbd.ttf"
        )
    )

    FUENTE = "TimesNewRoman"
    FUENTE_NEGRITA = "TimesNewRoman-Bold"

except Exception:

    FUENTE = "Times-Roman"
    FUENTE_NEGRITA = "Times-Bold"


# ==========================================================
# FUNCIÓN PARA CREAR TABLAS
# ==========================================================

def crear_tabla(datos, anchos=None):

    tabla = Table(
        datos,
        colWidths=anchos,
        repeatRows=1,
        hAlign="CENTER"
    )

    tabla.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (-1, -1), FUENTE),
                ("FONTNAME", (0, 0), (-1, 0), FUENTE_NEGRITA),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("LEADING", (0, 0), (-1, -1), 14),

                ("GRID", (0, 0), (-1, -1), 0.5, None),

                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),

                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    return tabla


# ==========================================================
# PIE DE PÁGINA
# ==========================================================

def agregar_pie_pagina(canvas, documento):

    canvas.saveState()

    ancho, alto = A4

    canvas.setFont(FUENTE, 9)

    canvas.drawCentredString(
        ancho / 2,
        1.3 * cm,
        f"{documento.page}"
    )

    canvas.restoreState()


# ==========================================================
# GENERACIÓN DEL INFORME
# ==========================================================

def generar_reporte(
        wedge,
        datos,
        nombre_archivo="Informe_estabilidad_talud.pdf"
):

    # ------------------------------------------------------
    # DOCUMENTO
    # ------------------------------------------------------

    documento = SimpleDocTemplate(
        nombre_archivo,
        pagesize=A4,

        rightMargin=2.54 * cm,
        leftMargin=2.54 * cm,
        topMargin=2.54 * cm,
        bottomMargin=2.54 * cm,

        title="Análisis de estabilidad de talud mediante cuña de falla planar",
        author="Jeison Steven Perez"
    )


    estilos_base = getSampleStyleSheet()


    # ------------------------------------------------------
    # ESTILO DEL TEXTO PRINCIPAL
    # ------------------------------------------------------

    estilo_texto = ParagraphStyle(
        "TextoAcademico",

        parent=estilos_base["BodyText"],

        fontName=FUENTE,
        fontSize=12,

        leading=18,

        alignment=TA_JUSTIFY,

        firstLineIndent=1.27 * cm,

        spaceAfter=8,

        allowWidows=0,
        allowOrphans=0
    )


    # ------------------------------------------------------
    # ESTILO PARA TEXTO SIN SANGRÍA
    # ------------------------------------------------------

    estilo_texto_sin_sangria = ParagraphStyle(
        "TextoSinSangria",

        parent=estilo_texto,

        firstLineIndent=0,

        alignment=TA_JUSTIFY
    )


    # ------------------------------------------------------
    # TÍTULO PRINCIPAL
    # ------------------------------------------------------

    estilo_titulo = ParagraphStyle(
        "TituloSeccion",

        parent=estilos_base["Heading1"],

        fontName=FUENTE_NEGRITA,

        fontSize=14,

        leading=18,

        alignment=TA_LEFT,

        spaceBefore=12,

        spaceAfter=10,

        keepWithNext=True
    )


    # ------------------------------------------------------
    # SUBTÍTULO
    # ------------------------------------------------------

    estilo_subtitulo = ParagraphStyle(
        "Subtitulo",

        parent=estilos_base["Heading2"],

        fontName=FUENTE_NEGRITA,

        fontSize=12,

        leading=16,

        alignment=TA_LEFT,

        spaceBefore=10,

        spaceAfter=8,

        keepWithNext=True
    )


    # ------------------------------------------------------
    # PORTADA
    # ------------------------------------------------------

    estilo_portada = ParagraphStyle(
        "Portada",

        parent=estilos_base["Title"],

        fontName=FUENTE_NEGRITA,

        fontSize=18,

        leading=24,

        alignment=TA_CENTER,

        spaceAfter=15
    )


    estilo_portada_normal = ParagraphStyle(
        "PortadaNormal",

        parent=estilos_base["BodyText"],

        fontName=FUENTE,

        fontSize=12,

        leading=18,

        alignment=TA_CENTER
    )


    contenido = []


    # ======================================================
    # PORTADA
    # ======================================================

    contenido.append(
        Spacer(1, 1.2 * cm)
    )

    contenido.append(
        Paragraph(
            "UNIVERSIDAD DISTRITAL<br/>"
            "FRANCISCO JOSÉ DE CALDAS",
            estilo_portada
        )
    )

    contenido.append(
        Paragraph(
            "FACULTAD TECNOLÓGICA<br/>"
            "PROGRAMA DE INGENIERÍA CIVIL",
            estilo_portada_normal
        )
    )

    contenido.append(
        Spacer(1, 2.0 * cm)
    )

    contenido.append(
        Paragraph(
            "PROYECTO DE PROGRAMACIÓN II",
            estilo_portada
        )
    )

    contenido.append(
        Spacer(1, 0.8 * cm)
    )

    contenido.append(
        Paragraph(
            "DESARROLLO DE UNA HERRAMIENTA "
            "COMPUTACIONAL PARA EL ANÁLISIS DE "
            "ESTABILIDAD DE TALUDES MEDIANTE "
            "CUÑA DE FALLA PLANAR",
            estilo_portada
        )
    )

    contenido.append(
        Spacer(1, 0.8 * cm)
    )

    contenido.append(
        Paragraph(
            "Integración del cálculo de propiedades "
            "geométricas mediante PySection y análisis "
            "geotécnico basado en equilibrio límite.",
            estilo_portada_normal
        )
    )

    contenido.append(
        Spacer(1, 2.0 * cm)
    )

    contenido.append(
        Paragraph(
            "<b>Autor</b><br/>"
            "Jeison Steven Perez",
            estilo_portada_normal
        )
    )

    contenido.append(
        Spacer(1, 1.0 * cm)
    )

    contenido.append(
        Paragraph(
            "<b>Asignatura</b><br/>"
            "Programación II",
            estilo_portada_normal
        )
    )

    contenido.append(
        Spacer(1, 1.0 * cm)
    )

    contenido.append(
        Paragraph(
            "Bogotá D.C.<br/>"
            "2026",
            estilo_portada_normal
        )
    )

    contenido.append(
        PageBreak()
    )


    # ======================================================
    # 1. INFORMACIÓN GENERAL
    # ======================================================

    contenido.append(
        Paragraph(
            "Información general del proyecto",
            estilo_titulo
        )
    )

    informacion = [
        ["Elemento", "Descripción"],

        [
            "Institución",
            "Universidad Distrital Francisco José de Caldas"
        ],

        [
            "Facultad",
            "Facultad Tecnológica"
        ],

        [
            "Programa",
            "Ingeniería Civil"
        ],

        [
            "Asignatura",
            "Programación II"
        ],

        [
            "Autor",
            "Jeison Steven Perez"
        ],

        [
            "Lenguaje",
            "Python"
        ],

        [
            "Aplicación",
            "Análisis computacional de estabilidad de taludes"
        ],

        [
            "Ciudad",
            "Bogotá D.C."
        ],

        [
            "Año",
            "2026"
        ]
    ]

    contenido.append(
        crear_tabla(
            informacion,
            [5 * cm, 10 * cm]
        )
    )

    contenido.append(
        Spacer(1, 0.5 * cm)
    )


    # ======================================================
    # 2. RESUMEN EJECUTIVO
    # ======================================================

    contenido.append(
        Paragraph(
            "1. Resumen ejecutivo",
            estilo_titulo
        )
    )

    resumen_1 = """
    El presente proyecto corresponde al desarrollo de una herramienta
    computacional aplicada a la ingeniería civil, específicamente al
    campo de la ingeniería geotécnica, cuyo propósito es automatizar
    el análisis básico de una cuña de falla planar en un talud. La
    aplicación fue desarrollada en lenguaje Python y estructurada
    mediante programación orientada a objetos, buscando integrar
    conceptos de geometría computacional, propiedades geométricas de
    secciones y fundamentos de estabilidad de taludes.
    """

    resumen_2 = f"""
    La herramienta permite al usuario ingresar parámetros relacionados
    con la geometría del talud y las propiedades del material, a partir
    de los cuales se construye la geometría de la masa potencialmente
    movilizable. Posteriormente, el programa determina el área de la
    cuña y la ubicación de su centroide mediante la integración del
    módulo PySection. Estas propiedades son utilizadas posteriormente
    para determinar el peso de la cuña, las componentes de fuerza y el
    factor de seguridad asociado al mecanismo de falla considerado.
    """

    resumen_3 = f"""
    Para el caso analizado se obtuvo un área de cuña de
    <b>{wedge.area:.3f} m²</b>, con un centroide localizado en
    XG = <b>{wedge.xG:.3f} m</b> y YG = <b>{wedge.yG:.3f} m</b>.
    El factor de seguridad calculado fue de
    <b>{wedge.FS:.3f}</b>. Estos resultados corresponden a las
    condiciones geométricas y geotécnicas introducidas por el usuario
    y deben interpretarse dentro de las hipótesis y simplificaciones
    propias del modelo implementado.
    """

    contenido.append(Paragraph(resumen_1, estilo_texto))
    contenido.append(Paragraph(resumen_2, estilo_texto))
    contenido.append(Paragraph(resumen_3, estilo_texto))


    # ======================================================
    # 3. INTRODUCCIÓN
    # ======================================================

    contenido.append(
        Paragraph(
            "2. Introducción",
            estilo_titulo
        )
    )

    introduccion_1 = """
    La estabilidad de taludes constituye uno de los problemas de mayor
    importancia dentro de la ingeniería geotécnica, debido a que las
    condiciones de inestabilidad pueden generar movimientos de masa
    capaces de afectar infraestructura, vías, edificaciones,
    excavaciones y diferentes tipos de obras civiles. El comportamiento
    de un talud depende de múltiples factores, entre los que se
    encuentran su geometría, las características resistentes del suelo,
    las condiciones de drenaje, la presencia de agua y las cargas
    aplicadas sobre el terreno.
    """

    introduccion_2 = """
    El análisis de estabilidad busca establecer si las condiciones
    existentes permiten mantener el equilibrio de la masa de suelo o,
    por el contrario, existe una condición en la que las fuerzas
    movilizantes pueden superar la resistencia disponible. Para ello,
    los métodos de equilibrio límite constituyen una aproximación
    ampliamente utilizada en la ingeniería geotécnica, debido a que
    permiten establecer relaciones entre las fuerzas resistentes y las
    fuerzas que favorecen el movimiento.
    """

    introduccion_3 = """
    Paralelamente, el desarrollo de herramientas computacionales ha
    transformado la manera en que se realizan cálculos de ingeniería.
    La programación permite automatizar operaciones repetitivas,
    desarrollar modelos específicos y obtener resultados de manera
    organizada y reproducible. En este contexto, Python ofrece
    herramientas adecuadas para integrar formulaciones matemáticas,
    estructuras de datos, programación orientada a objetos y
    representación gráfica.
    """

    introduccion_4 = """
    El presente proyecto integra estos dos campos mediante el desarrollo
    de una aplicación orientada al análisis de una cuña de falla planar.
    La herramienta combina el cálculo geométrico de una sección
    poligonal con un modelo geotécnico simplificado, permitiendo que el
    usuario modifique las condiciones del problema y obtenga
    automáticamente los resultados correspondientes.
    """

    contenido.append(Paragraph(introduccion_1, estilo_texto))
    contenido.append(Paragraph(introduccion_2, estilo_texto))
    contenido.append(Paragraph(introduccion_3, estilo_texto))
    contenido.append(Paragraph(introduccion_4, estilo_texto))


    # ======================================================
    # 4. ANTECEDENTES
    # ======================================================

    contenido.append(
        Paragraph(
            "3. Antecedentes",
            estilo_titulo
        )
    )

    antecedentes_1 = """
    El análisis de estabilidad de taludes ha sido abordado mediante
    diferentes metodologías desarrolladas a partir de principios de
    equilibrio, resistencia al corte y comportamiento mecánico de los
    materiales geológicos. La evolución de estas metodologías ha
    permitido representar diferentes mecanismos potenciales de falla
    y establecer condiciones de seguridad para proyectos de ingeniería.
    """

    antecedentes_2 = """
    En paralelo con el desarrollo de los métodos de análisis, la
    incorporación de herramientas computacionales ha permitido
    automatizar procedimientos que anteriormente requerían una gran
    cantidad de operaciones manuales. La programación aplicada a la
    ingeniería permite estructurar algoritmos capaces de recibir datos,
    procesarlos mediante formulaciones matemáticas y presentar los
    resultados de forma organizada.
    """

    antecedentes_3 = """
    En el ámbito académico, la integración entre programación e
    ingeniería civil permite comprender que un problema de ingeniería
    puede ser expresado mediante variables, relaciones matemáticas y
    algoritmos. El presente proyecto parte de esta premisa para
    desarrollar una aplicación que vincula el cálculo de centroides
    con un problema específico de ingeniería geotécnica.
    """

    contenido.append(Paragraph(antecedentes_1, estilo_texto))
    contenido.append(Paragraph(antecedentes_2, estilo_texto))
    contenido.append(Paragraph(antecedentes_3, estilo_texto))


    # ======================================================
    # 5. MARCO TEÓRICO
    # ======================================================

    contenido.append(
        Paragraph(
            "4. Marco teórico",
            estilo_titulo
        )
    )

    contenido.append(
        Paragraph(
            "4.1 Estabilidad de taludes",
            estilo_subtitulo
        )
    )

    texto = """
    Un talud puede definirse como una superficie inclinada de terreno
    natural o artificial cuya estabilidad depende de la relación entre
    las acciones que tienden a producir el movimiento y la resistencia
    disponible del material. El análisis de esta condición requiere
    considerar tanto factores geométricos como las propiedades
    mecánicas del suelo y las condiciones hidráulicas existentes.
    """

    contenido.append(
        Paragraph(texto, estilo_texto)
    )


    contenido.append(
        Paragraph(
            "4.2 Falla planar",
            estilo_subtitulo
        )
    )

    texto = """
    La falla planar representa un mecanismo mediante el cual una masa
    de suelo o roca puede desplazarse sobre una superficie de
    deslizamiento aproximadamente plana. Para efectos del presente
    proyecto, la masa potencialmente movilizada se representa mediante
    una cuña definida por la geometría del talud, el terreno superior y
    el plano potencial de falla.
    """

    contenido.append(
        Paragraph(texto, estilo_texto)
    )


    contenido.append(
        Paragraph(
            "4.3 Centroide de una sección poligonal",
            estilo_subtitulo
        )
    )

    texto = """
    El centroide constituye una propiedad geométrica fundamental para
    determinar la posición representativa de un área. En una aplicación
    geotécnica, conocer la ubicación del centroide de la cuña permite
    establecer el punto de referencia asociado a la distribución
    geométrica de la masa y facilita la representación del peso propio
    dentro del modelo.
    """

    contenido.append(
        Paragraph(texto, estilo_texto)
    )


    contenido.append(
        Paragraph(
            "4.4 Equilibrio límite y factor de seguridad",
            estilo_subtitulo
        )
    )

    texto = """
    El enfoque de equilibrio límite empleado en esta aplicación compara
    la resistencia disponible frente a las fuerzas que favorecen el
    movimiento de la cuña. De manera general, el factor de seguridad se
    expresa mediante la relación entre la resistencia disponible y la
    solicitación movilizante:
    """

    contenido.append(
        Paragraph(texto, estilo_texto)
    )

    contenido.append(
        Spacer(1, 0.2 * cm)
    )

    contenido.append(
        Paragraph(
            "<b>FS = R / T</b>",
            ParagraphStyle(
                "Ecuacion",
                parent=estilo_texto_sin_sangria,
                alignment=TA_CENTER,
                fontName=FUENTE_NEGRITA
            )
        )
    )

    contenido.append(
        Spacer(1, 0.2 * cm)
    )

    texto = """
    donde R corresponde a la resistencia total considerada y T
    representa la componente movilizante. La interpretación del valor
    obtenido debe realizarse teniendo en cuenta las hipótesis del
    modelo y las condiciones de entrada utilizadas.
    """

    contenido.append(
        Paragraph(texto, estilo_texto)
    )


    # ======================================================
    # 6. METODOLOGÍA COMPUTACIONAL
    # ======================================================

    contenido.append(
        Paragraph(
            "5. Metodología computacional",
            estilo_titulo
        )
    )

    metodologia_1 = """
    El desarrollo de la herramienta se realizó mediante una estructura
    modular basada en programación orientada a objetos. Esta
    organización permite separar las funciones relacionadas con la
    geometría, el análisis geotécnico, la interacción con el usuario y
    la generación del informe.
    """

    metodologia_2 = """
    El módulo <b>sections.py</b> constituye el componente geométrico
    utilizado para determinar las propiedades de la sección. A partir
    de los vértices que representan la cuña, se obtiene el área y la
    ubicación del centroide.
    """

    metodologia_3 = """
    El módulo <b>slope_wedge.py</b> utiliza estas propiedades
    geométricas dentro de un modelo específico de cuña de falla planar.
    A partir de los parámetros suministrados se determinan el peso de
    la cuña, las componentes de fuerza, las fuerzas resistentes y el
    factor de seguridad.
    """

    metodologia_4 = """
    El archivo <b>main.py</b> constituye el punto de interacción con el
    usuario. Su función es solicitar los parámetros del análisis,
    construir el objeto correspondiente y presentar los resultados.
    Finalmente, el módulo <b>report.py</b> utiliza los resultados
    calculados para construir automáticamente el presente informe en
    formato PDF.
    """

    contenido.append(Paragraph(metodologia_1, estilo_texto))
    contenido.append(Paragraph(metodologia_2, estilo_texto))
    contenido.append(Paragraph(metodologia_3, estilo_texto))
    contenido.append(Paragraph(metodologia_4, estilo_texto))


    # ======================================================
    # 7. PARÁMETROS
    # ======================================================

    contenido.append(
        Paragraph(
            "6. Parámetros de entrada",
            estilo_titulo
        )
    )

    contenido.append(
        Paragraph(
            """
            Los siguientes parámetros corresponden a los valores
            suministrados por el usuario durante la ejecución del
            programa.
            """,
            estilo_texto
        )
    )

    parametros = [
        ["Parámetro", "Valor"],

        ["Altura del talud H",
         f"{datos['H']:.2f} m"],

        ["Ángulo del talud β",
         f"{datos['beta_deg']:.2f}°"],

        ["Ángulo del plano de falla θ",
         f"{datos['theta_deg']:.2f}°"],

        ["Pendiente superior α",
         f"{datos['alpha_deg']:.2f}°"],

        ["Grieta de tracción zc",
         f"{datos['zc']:.2f} m"],

        ["Peso unitario γ",
         f"{datos['gamma']:.2f} kN/m³"],

        ["Cohesión efectiva c'",
         f"{datos['c_prime']:.2f} kPa"],

        ["Ángulo de fricción φ",
         f"{datos['phi_deg']:.2f}°"],

        ["Altura de agua zw",
         f"{datos['zw']:.2f} m"]
    ]

    contenido.append(
        crear_tabla(
            parametros,
            [9 * cm, 6 * cm]
        )
    )


    # ======================================================
    # 8. GEOMETRÍA
    # ======================================================

    contenido.append(
        Paragraph(
            "7. Construcción geométrica de la cuña",
            estilo_titulo
        )
    )

    texto = """
    La geometría de la masa potencialmente movilizada se representa
    mediante un conjunto ordenado de vértices. Estos puntos constituyen
    el polígono utilizado por el módulo geométrico para determinar el
    área y las coordenadas del centroide.
    """

    contenido.append(
        Paragraph(texto, estilo_texto)
    )

    puntos = [
        [
            "Punto",
            "Coordenada X",
            "Coordenada Y"
        ]
    ]

    for i, punto in enumerate(wedge.points, 1):

        puntos.append(
            [
                f"P{i}",
                f"{punto[0]:.3f} m",
                f"{punto[1]:.3f} m"
            ]
        )

    contenido.append(
        crear_tabla(
            puntos,
            [4 * cm, 5.5 * cm, 5.5 * cm]
        )
    )


    # ======================================================
    # 9. RESULTADOS
    # ======================================================

    contenido.append(
        Paragraph(
            "8. Resultados del análisis",
            estilo_titulo
        )
    )

    resultados = [
        ["Variable", "Resultado"],

        ["Área de la cuña",
         f"{wedge.area:.3f} m²"],

        ["Centroide XG",
         f"{wedge.xG:.3f} m"],

        ["Centroide YG",
         f"{wedge.yG:.3f} m"],

        ["Longitud del plano de falla",
         f"{wedge.Lp:.3f} m"],

        ["Peso de la cuña W",
         f"{wedge.W:.3f} kN/m"],

        ["Componente normal N",
         f"{wedge.Nw:.3f} kN/m"],

        ["Componente tangencial T",
         f"{wedge.Tw:.3f} kN/m"],

        ["Resistencia por cohesión C",
         f"{wedge.C_force:.3f} kN/m"],

        ["Resistencia por fricción Fφ",
         f"{wedge.F_fric:.3f} kN/m"],

        ["Resistencia total R",
         f"{wedge.R_total:.3f} kN/m"],

        ["Factor de seguridad FS",
         f"{wedge.FS:.3f}"]
    ]

    contenido.append(
        crear_tabla(
            resultados,
            [9 * cm, 6 * cm]
        )
    )


    # ======================================================
    # 10. ANÁLISIS DE RESULTADOS
    # ======================================================

    contenido.append(
        Paragraph(
            "9. Análisis y discusión de resultados",
            estilo_titulo
        )
    )

    analisis_1 = f"""
    El análisis realizado permitió determinar las principales
    propiedades geométricas y mecánicas de la cuña considerada. El área
    calculada corresponde a <b>{wedge.area:.3f} m²</b>, mientras que
    el centroide se encuentra localizado en las coordenadas
    XG = <b>{wedge.xG:.3f} m</b> y
    YG = <b>{wedge.yG:.3f} m</b>. Estas propiedades constituyen la
    base geométrica para determinar el peso de la masa potencialmente
    movilizada.
    """

    analisis_2 = f"""
    A partir del área obtenida y del peso unitario introducido,
    el programa determina un peso de la cuña de
    <b>{wedge.W:.3f} kN/m</b>. Este valor representa la acción
    asociada al peso propio de la masa analizada. Posteriormente, el
    peso es descompuesto en una componente normal al plano de falla,
    correspondiente a <b>{wedge.Nw:.3f} kN/m</b>, y una componente
    tangencial de <b>{wedge.Tw:.3f} kN/m</b>, relacionada con la
    tendencia de movimiento de la cuña.
    """

    analisis_3 = f"""
    La resistencia considerada dentro del modelo está constituida por
    la contribución asociada a la cohesión y por la resistencia
    friccional. La resistencia por cohesión calculada es de
    <b>{wedge.C_force:.3f} kN/m</b>, mientras que la contribución
    asociada a la fricción corresponde a
    <b>{wedge.F_fric:.3f} kN/m</b>. La combinación de estas
    contribuciones genera una resistencia total de
    <b>{wedge.R_total:.3f} kN/m</b>.
    """

    if wedge.FS >= 1:

        analisis_4 = f"""
        Finalmente, el factor de seguridad obtenido es
        <b>FS = {wedge.FS:.3f}</b>. Bajo las hipótesis del modelo
        implementado, este valor indica que la resistencia calculada
        supera la solicitación movilizante considerada, por lo que el
        caso evaluado presenta una condición favorable dentro del
        análisis simplificado desarrollado.
        """

    else:

        analisis_4 = f"""
        Finalmente, el factor de seguridad obtenido es
        <b>FS = {wedge.FS:.3f}</b>. Bajo las hipótesis del modelo
        implementado, este valor indica que la solicitación movilizante
        supera la resistencia calculada, por lo que el caso evaluado
        presenta una condición desfavorable dentro del análisis
        simplificado desarrollado.
        """


    analisis_5 = """
    No obstante, el factor de seguridad obtenido mediante esta
    herramienta debe interpretarse de acuerdo con el alcance del
    proyecto. El programa constituye una aplicación académica y emplea
    un modelo simplificado para representar el comportamiento de la
    cuña. Un estudio geotécnico destinado a diseño o toma de decisiones
    de ingeniería requiere información adicional, incluyendo
    investigación del subsuelo, caracterización estratigráfica,
    resultados de ensayos de laboratorio y campo, condiciones de agua,
    cargas externas, geometría real del terreno y selección de una
    metodología de análisis acorde con el mecanismo de falla esperado.
    """

    contenido.append(Paragraph(analisis_1, estilo_texto))
    contenido.append(Paragraph(analisis_2, estilo_texto))
    contenido.append(Paragraph(analisis_3, estilo_texto))
    contenido.append(Paragraph(analisis_4, estilo_texto))
    contenido.append(Paragraph(analisis_5, estilo_texto))


    # ======================================================
    # 11. CONCLUSIONES
    # ======================================================

    contenido.append(
        Paragraph(
            "10. Conclusiones",
            estilo_titulo
        )
    )

    conclusiones = [
        """
        El desarrollo permitió integrar conceptos de programación
        orientada a objetos con un problema aplicado de ingeniería civil,
        demostrando la utilidad de Python como herramienta para
        automatizar procesos de cálculo.
        """,

        """
        La integración del módulo PySection permitió utilizar el cálculo
        de propiedades geométricas de una sección poligonal dentro de un
        modelo geotécnico, estableciendo una conexión directa entre el
        cálculo de centroides y el análisis de la cuña de falla.
        """,

        """
        La estructura modular del proyecto facilita la comprensión,
        mantenimiento y ampliación del código, al separar las funciones
        geométricas, geotécnicas, de interacción con el usuario y de
        generación del informe.
        """,

        """
        La posibilidad de modificar los parámetros de entrada permite
        utilizar la herramienta para analizar diferentes condiciones
        geométricas y propiedades del material sin modificar directamente
        el código fuente.
        """,

        """
        La generación automática del informe técnico permite documentar
        los datos introducidos, los resultados obtenidos y la
        representación gráfica del análisis, fortaleciendo la utilidad
        académica de la aplicación.
        """,

        """
        Finalmente, los resultados obtenidos deben entenderse dentro
        del alcance y las hipótesis del modelo implementado. La
        herramienta constituye un ejercicio académico de integración
        entre programación e ingeniería y no sustituye un estudio
        geotécnico completo para proyectos reales.
        """
    ]

    for conclusion in conclusiones:

        contenido.append(
            Paragraph(
                conclusion,
                estilo_texto
            )
        )


    # ======================================================
    # 12. REPRESENTACIÓN GRÁFICA
    # ======================================================

    contenido.append(
        PageBreak()
    )

    contenido.append(
        Paragraph(
            "11. Representación gráfica del análisis",
            estilo_titulo
        )
    )

    contenido.append(
        Paragraph(
            """
            La siguiente figura corresponde a la representación gráfica
            generada automáticamente por el programa a partir de los
            parámetros introducidos por el usuario.
            """,
            estilo_texto
        )
    )

    try:

        imagen = Image(
            "cuna_talud.png",
            width=16 * cm,
            height=6.5 * cm
        )

        imagen.hAlign = "CENTER"

        contenido.append(
            Spacer(1, 0.5 * cm)
        )

        contenido.append(
            imagen
        )

    except Exception:

        contenido.append(
            Paragraph(
                "No fue posible incorporar la representación gráfica.",
                estilo_texto
            )
        )


    # ======================================================
    # GENERACIÓN DEL PDF
    # ======================================================

    documento.build(
        contenido,
        onFirstPage=agregar_pie_pagina,
        onLaterPages=agregar_pie_pagina
    )

    print(
        f"Informe académico generado correctamente: "
        f"{nombre_archivo}"
    )