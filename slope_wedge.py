"""
slope_wedge.py

Módulo geotécnico para el análisis de estabilidad de taludes mediante cuñas de falla plana
(Coulomb / Hoek & Bray), calculando propiedades geométricas (área, centroide baricéntrico)
utilizando el motor de cálculo de 'sections.py' y descomponiendo las fuerzas actuantes y resistentes.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from sections import Section


class SlopeWedge(Section):
    """
    Modela la cuña de falla de un talud en geotecnia.
    Hereda de Section para reutilizar el cálculo analítico de:
      - Área poligonal (_A)
      - Coordenada horizontal del centroide (_x)
      - Coordenada vertical del centroide (_y)
    """

    def __init__(
        self,
        H=10.0,
        beta_deg=55.0,
        theta_deg=32.0,
        alpha_deg=0.0,
        zc=2.5,
        gamma=19.0,
        c_prime=15.0,
        phi_deg=26.0,
        zw=0.0,
    ):
        """
        Parámetros:
        -----------
        H : float
            Altura total del talud [m].
        beta_deg : float
            Ángulo de inclinación de la cara del talud respecto a la horizontal [grados].
        theta_deg : float
            Ángulo de inclinación del plano de falla planar [grados] (theta < beta).
        alpha_deg : float
            Ángulo de inclinación del terreno superior tras la cresta [grados].
        zc : float
            Profundidad de la grieta de tracción vertical [m] (0 si no existe grieta).
        gamma : float
            Peso unitario del suelo / roca [kN/m³].
        c_prime : float
            Cohesión efectiva del plano de falla [kPa] o [kN/m²].
        phi_deg : float
            Ángulo de fricción interna efectivo del plano de falla [grados].
        zw : float
            Nivel freático o altura de agua acumulada dentro de la grieta de tracción [m].
        """
        super().__init__()
        self.H = float(H)
        self.beta = np.radians(beta_deg)
        self.theta = np.radians(theta_deg)
        self.alpha = np.radians(alpha_deg)
        self.zc = float(zc)
        self.gamma = float(gamma)
        self.c_prime = float(c_prime)
        self.phi = np.radians(phi_deg)
        self.zw = float(zw)
        self.gamma_w = 9.81

        self.beta_deg = beta_deg
        self.theta_deg = theta_deg
        self.alpha_deg = alpha_deg
        self.phi_deg = phi_deg

        self._calc_geometry_and_forces()

    def _calc_geometry_and_forces(self):
        """Calcula los vértices del polígono de la cuña, su centroide y las componentes de fuerza."""
        # 1. Geometría del talud
        self.x_toe = 0.0
        self.y_toe = 0.0

        self.x_crest = self.H / np.tan(self.beta)
        self.y_crest = self.H

        # 2. Vértices de la cuña
        denom = np.tan(self.theta) - np.tan(self.alpha)
        if abs(denom) < 1e-6:
            denom = 1e-6

        if self.zc > 0:
            self.xc = (self.H - self.zc - self.x_crest * np.tan(self.alpha)) / denom
            self.yc_top = self.H + (self.xc - self.x_crest) * np.tan(self.alpha)
            self.yc_bot = self.xc * np.tan(self.theta)

            # Polígono en sentido antihorario (CCW)
            self.points = np.array([
                [self.x_toe, self.y_toe],
                [self.xc, self.yc_bot],
                [self.xc, self.yc_top],
                [self.x_crest, self.y_crest],
            ])
        else:
            self.xc = (self.H - self.x_crest * np.tan(self.alpha)) / denom
            self.yc_top = self.H + (self.xc - self.x_crest) * np.tan(self.alpha)
            self.yc_bot = self.yc_top
            self.zc = 0.0
            self.points = np.array([
                [self.x_toe, self.y_toe],
                [self.xc, self.yc_top],
                [self.x_crest, self.y_crest],
            ])

        # 3. Propiedades geométricas analíticas con Section
        self.area = abs(super()._A(self.points))
        self.xG = super()._x(self.points)
        self.yG = super()._y(self.points)

        # Longitud del plano de deslizamiento
        self.Lp = np.sqrt(self.xc ** 2 + self.yc_bot ** 2)

        # 4. Componentes de fuerzas
        # Peso de la cuña W actuando en el centroide (xG, yG)
        self.W = self.gamma * self.area

        # Descomposición de W respecto al plano de falla
        self.Nw = self.W * np.cos(self.theta)  # Componente normal
        self.Tw = self.W * np.sin(self.theta)  # Componente tangencial desestabilizadora

        # Empuje hidrostático y subpresión si hay agua en la grieta
        if self.zw > 0 and self.zc > 0:
            zw_eff = min(self.zw, self.zc)
            self.Vw = 0.5 * self.gamma_w * (zw_eff ** 2)
            self.U = 0.5 * (self.gamma_w * zw_eff) * self.Lp
        else:
            self.Vw = 0.0
            self.U = 0.0

        # Normal efectiva N' y fuerza cortante desestabilizadora total T_act
        self.N_prime = max(0.0, self.Nw - self.U - self.Vw * np.sin(self.theta))
        self.T_act = self.Tw + self.Vw * np.cos(self.theta)

        # Fuerzas resistentes según criterio Mohr-Coulomb
        self.C_force = self.c_prime * self.Lp
        self.F_fric = self.N_prime * np.tan(self.phi)
        self.R_total = self.C_force + self.F_fric

        # Factor de Seguridad
        self.FS = self.R_total / self.T_act if self.T_act > 0 else float("inf")

    def plot(self, filename="cuna_talud.png"):
        """Genera y guarda una imagen detallada de la cuña, su centroide y las componentes de fuerza."""
        fig, ax = plt.subplots(figsize=(12, 7.5), dpi=150)
        ax.set_aspect("equal", adjustable="box")

        x_max = self.xc + 5.0
        y_max = self.H + (x_max - self.x_crest) * np.tan(self.alpha)
        x_min = -4.0

        # Perfil del terreno
        terrain_x = [x_min, self.x_toe, self.x_crest, x_max]
        terrain_y = [0.0, 0.0, self.H, y_max]
        ax.plot(terrain_x, terrain_y, color="#2c3e50", lw=2.5, label="Perfil del talud")

        # Hachurado de fondo
        ax.fill_between(
            [x_min, self.x_toe, self.xc, x_max],
            [0.0, 0.0, self.yc_bot, y_max],
            -2.0,
            color="#f2f4f4",
            alpha=0.9,
        )

        # Cuña de deslizamiento
        poly_pts = np.vstack([self.points, self.points[0]])
        ax.fill(
            poly_pts[:, 0],
            poly_pts[:, 1],
            color="#f39c12",
            alpha=0.35,
            label="Cuña de deslizamiento",
        )
        ax.plot(poly_pts[:, 0], poly_pts[:, 1], color="#d68910", lw=2, linestyle="-")

        # Plano de falla
        ax.plot(
            [self.x_toe, self.xc],
            [self.y_toe, self.yc_bot],
            color="#c0392b",
            lw=3.2,
            label=f"Plano de falla (θ = {self.theta_deg:.1f}°)",
        )

        # Grieta de tracción
        if self.zc > 0:
            ax.plot(
                [self.xc, self.xc],
                [self.yc_bot, self.yc_top],
                color="#8e44ad",
                lw=2.5,
                linestyle="--",
                label=f"Grieta de tracción (zc = {self.zc:.1f} m)",
            )

        # Centroide G
        ax.scatter([self.xG], [self.yG], color="#c0392b", s=130, zorder=7, edgecolors="black", lw=1.5)
        ax.annotate(
            f"G (Centroide)\n({self.xG:.2f}, {self.yG:.2f}) m",
            xy=(self.xG, self.yG),
            xytext=(self.xG - 2.9, self.yG + 1.2),
            fontsize=10,
            weight="bold",
            color="#922b21",
            arrowprops=dict(arrowstyle="->", lw=1.3, color="#922b21"),
        )

        # Escala visual ajustada para vectores de fuerza
        max_vec_len = 3.0  # metros gráficos
        scale = max_vec_len / self.W

        # Vector Peso W
        W_len = self.W * scale
        ax.annotate(
            "",
            xy=(self.xG, self.yG - W_len),
            xytext=(self.xG, self.yG),
            arrowprops=dict(arrowstyle="-|>", lw=2.6, color="#2980b9", mutation_scale=16),
        )
        ax.text(
            self.xG - 0.35,
            self.yG - W_len * 0.65,
            f"W = {self.W:.1f} kN/m",
            color="#1b4f72",
            weight="bold",
            fontsize=9,
            ha="right",
        )

        # Componente Normal N en el centroide
        Nx = self.Nw * scale * np.sin(self.theta)
        Ny = -self.Nw * scale * np.cos(self.theta)
        ax.annotate(
            "",
            xy=(self.xG + Nx, self.yG + Ny),
            xytext=(self.xG, self.yG),
            arrowprops=dict(arrowstyle="-|>", lw=2, color="#27ae60", linestyle="--", mutation_scale=14),
        )
        ax.text(
            self.xG + Nx + 0.3,
            self.yG + Ny,
            f"N = {self.Nw:.1f} kN/m",
            color="#196f3d",
            weight="bold",
            fontsize=9,
            va="center",
        )

        # Componente Tangencial T en el centroide
        Tx = -self.Tw * scale * np.cos(self.theta)
        Ty = -self.Tw * scale * np.sin(self.theta)
        ax.annotate(
            "",
            xy=(self.xG + Tx, self.yG + Ty),
            xytext=(self.xG, self.yG),
            arrowprops=dict(arrowstyle="-|>", lw=2, color="#e74c3c", linestyle="--", mutation_scale=14),
        )
        ax.text(
            self.xG + Tx - 0.2,
            self.yG + Ty + 0.3,
            f"T = {self.Tw:.1f} kN/m",
            color="#b03a2e",
            weight="bold",
            fontsize=9,
            ha="right",
        )

        # Líneas guía de descomposición (rectángulo N-T-W)
        ax.plot([self.xG + Nx, self.xG], [self.yG + Ny, self.yG - W_len], color="#7f8c8d", linestyle=":", lw=1.2)
        ax.plot([self.xG + Tx, self.xG], [self.yG + Ty, self.yG - W_len], color="#7f8c8d", linestyle=":", lw=1.2)

        # Fuerza resistente R a lo largo del plano de falla
        x_base = self.xc * 0.35
        y_base = self.yc_bot * 0.35
        R_len = self.R_total * scale
        Rx = R_len * np.cos(self.theta)
        Ry = R_len * np.sin(self.theta)
        ax.annotate(
            "",
            xy=(x_base + Rx, y_base + Ry),
            xytext=(x_base, y_base),
            arrowprops=dict(arrowstyle="-|>", lw=2.8, color="#16a085", mutation_scale=16),
        )
        ax.text(
            x_base + Rx * 0.5 + 0.4,
            y_base + Ry * 0.5 - 0.8,
            f"Resistencia al corte R = {self.R_total:.1f} kN/m\n(Cohesión C={self.C_force:.1f} + Fricción Fφ={self.F_fric:.1f})",
            color="#0e6655",
            weight="bold",
            fontsize=8.5,
            bbox=dict(boxstyle="square,pad=0.2", facecolor="#e8f8f5", edgecolor="#a3e4d7", alpha=0.9),
        )

        # Ángulos β y θ en el pie
        arc_r_beta = 2.0
        beta_arc = patches.Arc(
            (0, 0), arc_r_beta * 2, arc_r_beta * 2, angle=0, theta1=0, theta2=self.beta_deg, color="#2c3e50", lw=1.6
        )
        ax.add_patch(beta_arc)
        ax.text(
            arc_r_beta * 1.25 * np.cos(self.beta / 2),
            arc_r_beta * 1.25 * np.sin(self.beta / 2),
            f"β = {self.beta_deg:.0f}°",
            color="#2c3e50",
            weight="bold",
            fontsize=9,
        )

        arc_r_theta = 4.2
        theta_arc = patches.Arc(
            (0, 0), arc_r_theta * 2, arc_r_theta * 2, angle=0, theta1=0, theta2=self.theta_deg, color="#c0392b", lw=1.6
        )
        ax.add_patch(theta_arc)
        ax.text(
            arc_r_theta * 1.12 * np.cos(self.theta / 2),
            arc_r_theta * 1.12 * np.sin(self.theta / 2),
            f"θ = {self.theta_deg:.0f}°",
            color="#c0392b",
            weight="bold",
            fontsize=9,
        )

        # Cuadro de resultados
        summary_text = (
            f"CUÑA DE TALUD - RESULTADOS:\n"
            f" ───────────────────────────────────\n"
            f" GEOMETRÍA:\n"
            f"  • Área cuña (A):       {self.area:7.2f} m²\n"
            f"  • Centroide XG:         {self.xG:7.2f} m\n"
            f"  • Centroide YG:         {self.yG:7.2f} m\n"
            f"  • Longitud falla (Lp):  {self.Lp:7.2f} m\n"
            f"  • Grieta tracción (zc): {self.zc:7.2f} m\n"
            f" ───────────────────────────────────\n"
            f" COMPONENTES DE FUERZAS:\n"
            f"  • Peso cuña (W):       {self.W:7.2f} kN/m\n"
            f"  • Normal (N):          {self.Nw:7.2f} kN/m\n"
            f"  • Tangencial (T):      {self.Tw:7.2f} kN/m\n"
            f"  • Cohesión (C):        {self.C_force:7.2f} kN/m\n"
            f"  • Fricción (Fφ):       {self.F_fric:7.2f} kN/m\n"
            f"  • Resistente total (R):{self.R_total:7.2f} kN/m\n"
            f" ───────────────────────────────────\n"
            f" FACTOR DE SEGURIDAD (FS): {self.FS:.2f}"
        )
        props = dict(boxstyle="round,pad=0.6", facecolor="#fcfcfc", edgecolor="#bdc3c7", alpha=0.96, lw=1.2)
        ax.text(
            0.02,
            0.98,
            summary_text,
            transform=ax.transAxes,
            fontsize=8.5,
            verticalalignment="top",
            bbox=props,
            family="monospace",
        )

        ax.set_xlim(x_min, x_max + 1.0)
        ax.set_ylim(-2.0, y_max + 2.5)
        ax.set_xlabel("Distancia horizontal X [m]", fontsize=11)
        ax.set_ylabel("Cota vertical Y [m]", fontsize=11)
        ax.set_title(
            f"Análisis Geotécnico de Cuña de Falla en Talud (FS = {self.FS:.2f})",
            fontsize=13,
            weight="bold",
            pad=12,
        )
        ax.grid(True, linestyle=":", alpha=0.5)
        ax.legend(loc="lower right", fontsize=8.5, framealpha=0.92)

        plt.tight_layout()
        plt.savefig(filename, bbox_inches="tight")
        print(f"-> Imagen generada y guardada en: {filename}")
