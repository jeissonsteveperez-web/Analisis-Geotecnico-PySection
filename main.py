"""
main.py

Aplicación interactiva para análisis geotécnico de una cuña de falla planar.

Integra:
- PySection para cálculo de área y centroide.
- Modelo SlopeWedge para análisis de estabilidad.
- Generación gráfica de resultados.
- Generación automática de informe PDF.
"""

from slope_wedge import SlopeWedge
from report import generar_reporte


def solicitar_dato(mensaje, minimo=None):
    """
    Solicita un dato numérico al usuario y valida valores negativos.
    """

    while True:
        try:
            valor = float(input(mensaje))

            if minimo is not None and valor < minimo:
                print(f"Error: el valor debe ser mayor o igual a {minimo}.")
                continue

            return valor

        except ValueError:
            print("Ingrese un valor numérico válido.")



def ingresar_parametros():
    """
    Solicita los parámetros geométricos y geotécnicos.
    """

    print("\n" + "=" * 70)
    print(" INGRESO DE PARÁMETROS DEL TALUD")
    print("=" * 70)


    print("\n--- GEOMETRÍA DEL TALUD ---")

    H = solicitar_dato(
        "Altura del talud H [m]: ",
        0
    )

    beta = solicitar_dato(
        "Ángulo de inclinación del talud β [°]: ",
        0
    )

    theta = solicitar_dato(
        "Ángulo del plano de falla θ [°]: ",
        0
    )

    alpha = solicitar_dato(
        "Pendiente del terreno superior α [°]: ",
        0
    )

    zc = solicitar_dato(
        "Profundidad de grieta de tracción zc [m]: ",
        0
    )


    print("\n--- PROPIEDADES DEL MATERIAL ---")

    gamma = solicitar_dato(
        "Peso unitario del suelo γ [kN/m³]: ",
        0
    )

    c_prime = solicitar_dato(
        "Cohesión efectiva c' [kPa]: ",
        0
    )

    phi = solicitar_dato(
        "Ángulo de fricción interna φ [°]: ",
        0
    )


    print("\n--- CONDICIÓN DE AGUA ---")

    zw = solicitar_dato(
        "Altura de agua en grieta zw [m]: ",
        0
    )


    if theta >= beta:
        print("\nAdvertencia:")
        print(
            "El ángulo del plano de falla debe ser menor "
            "que el ángulo del talud."
        )


    return {
        "H": H,
        "beta_deg": beta,
        "theta_deg": theta,
        "alpha_deg": alpha,
        "zc": zc,
        "gamma": gamma,
        "c_prime": c_prime,
        "phi_deg": phi,
        "zw": zw
    }



def mostrar_resultados(wedge):

    print("\n" + "=" * 70)
    print(" RESULTADOS DEL ANÁLISIS")
    print("=" * 70)


    print("\n1. PROPIEDADES GEOMÉTRICAS")
    print("-" * 70)

    print(f"Área de la cuña:              {wedge.area:.3f} m²")
    print(f"Centroide XG:                 {wedge.xG:.3f} m")
    print(f"Centroide YG:                 {wedge.yG:.3f} m")
    print(f"Longitud plano falla:         {wedge.Lp:.3f} m")


    print("\n2. COMPONENTES DE FUERZA")
    print("-" * 70)

    print(f"Peso de la cuña W:            {wedge.W:.3f} kN/m")
    print(f"Componente normal N:          {wedge.Nw:.3f} kN/m")
    print(f"Componente tangencial T:      {wedge.Tw:.3f} kN/m")
    print(f"Resistencia cohesión C:       {wedge.C_force:.3f} kN/m")
    print(f"Resistencia fricción Fφ:      {wedge.F_fric:.3f} kN/m")
    print(f"Resistencia total R:          {wedge.R_total:.3f} kN/m")


    print("\n3. ESTABILIDAD")
    print("-" * 70)

    print(f"Factor de Seguridad FS:       {wedge.FS:.3f}")


    if wedge.FS >= 1:
        print("Condición: ESTABLE")
    else:
        print("Condición: INESTABLE")



def main():

    print("=" * 70)
    print(" PYSECTION APLICADO AL ANÁLISIS DE ESTABILIDAD DE TALUDES")
    print("=" * 70)

    print(
        "\nEste programa integra cálculo geométrico mediante PySection "
        "con un modelo geotécnico de estabilidad de taludes."
    )


    params = ingresar_parametros()


    print("\nCalculando análisis...")


    wedge = SlopeWedge(**params)


    mostrar_resultados(wedge)


    # Generación de imagen
    archivo_imagen = "cuna_talud.png"

    wedge.plot(archivo_imagen)


    # Generación de informe PDF
    archivo_pdf = "Informe_estabilidad_talud.pdf"

    generar_reporte(
        wedge,
        params,
        archivo_pdf
    )


    print("\n" + "=" * 70)
    print(" ANÁLISIS FINALIZADO CORRECTAMENTE")
    print("=" * 70)

    print(f"Imagen generada: {archivo_imagen}")
    print(f"Informe PDF generado: {archivo_pdf}")



if __name__ == "__main__":
    main()