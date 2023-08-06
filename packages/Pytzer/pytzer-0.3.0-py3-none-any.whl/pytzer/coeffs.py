# pytzer: Pitzer model for chemical activities in aqueous solutions
# Copyright (C) 2019  Matthew Paul Humphreys  (GNU GPLv3)

"""Evaluate Pitzer model interaction coefficients."""

from autograd.numpy import array, exp, float_, full_like, log, \
                           logical_and, sqrt
from autograd.numpy import abs as np_abs
from .constants import Tzero
from .tables import P91_Ch3_T12, P91_Ch3_T13_I, P91_Ch3_T13_II, \
                    PM73_TableI, PM73_TableVI, PM73_TableVIII, PM73_TableIX
from . import props

# Note that variable T in this module is equivalent to tempK elsewhere,
# and P is equivalent to pres, for convenience

#%%############################################################################
# === ZERO FUNCTIONS ==========================================================

def bC_none(T, P):
    b0 = 0
    b1 = 0
    b2 = 0
    C0 = 0
    C1 = 0
    alph1 = -9
    alph2 = -9
    omega = -9
    valid = T > 0
    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

def theta_none(T, P):
    theta = 0
    valid = T > 0
    return theta, valid

def psi_none(T, P):
    psi = 0
    valid = T > 0
    return psi, valid

def lambd_none(T, P):
    lambd = 0
    valid = T > 0
    return lambd, valid

def zeta_none(T, P):
    zeta = 0
    valid = T > 0
    return zeta, valid

def mu_none(T, P):
    mu = 0
    valid = T > 0
    return mu, valid

# === ZERO FUNCTIONS ==========================================================
###############################################################################

#%%############################################################################
# === ROY ET AL. 1980 =========================================================

# --- theta: hydrogen magnesium -----------------------------------------------

def theta_H_Mg_RGB80(T, P):
    # RGB80 do provide theta values at 5, 15, 25, 35 and 45 degC, but no
    #  equation to interpolate between them.
    # This function just returns the 25 degC value.
    theta = 0.0620
    valid = T == 298.15

    return theta, valid

# === ROY ET AL. 1980 =========================================================
###############################################################################

#%%############################################################################
# === RARD & MILLER 1981i =====================================================

# --- bC: magnesium sulfate ---------------------------------------------------

def bC_Mg_SO4_RM81i(T, P):
    b0 = 0.21499
    b1 = 3.3646
    b2 = -32.743
    Cphi = 0.02797
    zMg  = +2
    zSO4 = -2
    C0 = Cphi / (2 * sqrt(np_abs(zMg * zSO4)))
    C1 = 0
    alph1 = 1.4
    alph2 = 12
    omega = -9
    valid = T == 298.15
    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

# === RARD & MILLER 1981i =====================================================
###############################################################################

#%%############################################################################
# === ROY ET AL. 1982 =========================================================

# --- theta: calcium hydrogen -------------------------------------------------

def theta_Ca_H_RGO82(T, P):
    theta = 0.0612
    valid = T == 298.15
    return theta, valid

# === ROY ET AL. 1982 =========================================================
###############################################################################

#%%############################################################################
# === PHUTELA & PITZER 1986 ===================================================

PP86ii_Tr = 298.15

def PP86ii_eq28(T,q):
    Tr = PP86ii_Tr
    return ((T**2 - Tr**2) * q[0] / 2 \
          + (T**3 - Tr**3) * q[1] / 3 \
          + (T**4 - Tr**4) * q[2] / 4 \
          + (T**5 - Tr**5) * q[3] / 5 \
          +         Tr**2  * q[4]) / T**2

def PP86ii_eq29(T,q):
    # q[x]     b0         b1         b2         C0
    #   0      q6         q10        q12        q15
    #   1      q7         q11        q13        q16
    #   2      q8          0         q14        q17
    #   3      q9          0          0         q18
    #   4    b0L(Tr)    b1L(Tr)    b2L(Tr)    C0L(Tr)
    #   5     b0(Tr)     b1(Tr)     b2(Tr)     C0(Tr)    from RM81
    Tr = PP86ii_Tr
    # Substitute to avoid 'difference of two large numbers' error
    t = T / Tr
    # Original fourth line was:
    #  + q[3] * (T**4/20 + Tr**5/(5*T) - Tr**4/4)
    return q[0] * (T   / 2 + Tr**2/(2*T) - Tr     )   \
         + q[1] * (T**2/ 6 + Tr**3/(3*T) - Tr**2/2)   \
         + q[2] * (T**3/12 + Tr**4/(4*T) - Tr**3/3)   \
         + q[3] * (t**5 + 4 - 5*t) * Tr**5 / (20 * T) \
         + q[4] * (Tr - Tr**2/T)                      \
         + q[5]

# --- bC: magnesium sulfate ---------------------------------------------------

def bC_Mg_SO4_PP86ii(T, P):

    b0r, b1r, b2r, C0r, C1, alph1, alph2, omega, _ = bC_Mg_SO4_RM81i(T, P)

    b0 = PP86ii_eq29(T,float_([-1.0282   ,
                                8.4790e-3,
                               -2.3366e-5,
                                2.1575e-8,
                                6.8402e-4,
                                b0r      ]))

    b1 = PP86ii_eq29(T,float_([-2.9596e-1,
                                9.4564e-4,
                                0        ,
                                0        ,
                                1.1028e-2,
                                b1r      ]))

    b2 = PP86ii_eq29(T,float_([-1.3764e+1,
                                1.2121e-1,
                               -2.7642e-4,
                                0        ,
                               -2.1515e-1,
                                b2r      ]))

    C0 = PP86ii_eq29(T,float_([ 1.0541e-1,
                               -8.9316e-4,
                                2.5100e-6,
                               -2.3436e-9,
                               -8.7899e-5,
                                C0r      ]))

    valid = T <= 473.

    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

# === PHUTELA & PITZER 1986 ===================================================
###############################################################################

#%%############################################################################
# === DE LIMA & PITZER 1983 ===================================================

# --- bC: magnesium chloride --------------------------------------------------

def bC_Mg_Cl_dLP83(T, P):

    # dLP83 Eq. (11)

    b0 = 5.93915e-7 * T**2 \
       - 9.31654e-4 * T \
       + 0.576066

    b1 = 2.60169e-5 * T**2 \
       - 1.09438e-2 * T \
       + 2.60135

    b2 = 0

    Cphi = 3.01823e-7 * T**2 \
         - 2.89125e-4 * T \
         + 6.57867e-2

    zMg = +2
    zCl = -1
    C0 = Cphi / (2 * sqrt(np_abs(zMg * zCl)))

    C1 = 0

    alph1 = 2
    alph2 = -9
    omega = -9

    valid = logical_and(T >= 298.15, T <= 523.15)

    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

# === DE LIMA & PITZER 1983 ===================================================
###############################################################################

#%%############################################################################
# === HOLMES & MESMER 1983 ====================================================

def HM83_eq25(T, a):

    TR = 298.15

    return a[0] \
         + a[1] * (1/T - 1/TR) \
         + a[2] * log(T/TR) \
         + a[3] * (T - TR) \
         + a[4] * (T**2 - TR**2) \
         + a[5] * log(T - 260)

# --- bC: caesium chloride ----------------------------------------------------

def bC_Cs_Cl_HM83(T, P):

    b0    = HM83_eq25(T,float_([    0.03352  ,
                                -1290.0      ,
                                -   8.4279   ,
                                    0.018502 ,
                                -   6.7942e-6,
                                    0        ]))

    b1    = HM83_eq25(T,float_([    0.0429   ,
                                -  38.0      ,
                                    0        ,
                                    0.001306 ,
                                    0        ,
                                    0        ]))

    b2 = 0

    Cphi  = HM83_eq25(T,float_([-   2.62e-4  ,
                                  157.13     ,
                                    1.0860   ,
                                -   0.0025242,
                                    9.840e-7 ,
                                    0        ]))

    zCs   = +1
    zCl   = -1
    C0    = Cphi / (2 * sqrt(np_abs(zCs * zCl)))

    C1 = 0

    alph1 = 2
    alph2 = -9
    omega = -9

    valid = logical_and(T >= 273.15, T <= 523.15)

    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

# --- bC: potassium chloride --------------------------------------------------

def bC_K_Cl_HM83(T, P):

    b0    = HM83_eq25(T,float_([   0.04808  ,
                                -758.48     ,
                                -  4.7062   ,
                                   0.010072 ,
                                -  3.7599e-6,
                                   0        ]))

    b1    = HM83_eq25(T,float_([   0.0476   ,
                                 303.09     ,
                                   1.066    ,
                                   0        ,
                                   0        ,
                                   0.0470   ]))

    b2 = 0

    Cphi  = HM83_eq25(T,float_([-  7.88e-4  ,
                                  91.270    ,
                                   0.58643  ,
                                -  0.0012980,
                                   4.9567e-7,
                                   0        ]))

    zK    = +1
    zCl   = -1
    C0    = Cphi / (2 * sqrt(np_abs(zK * zCl)))

    C1 = 0

    alph1 = 2
    alph2 = -9
    omega = -9

    valid = logical_and(T >= 273.15, T <= 523.15)

    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

# --- bC: lithium chloride ----------------------------------------------------

def bC_Li_Cl_HM83(T, P):

    b0    = HM83_eq25(T,float_([ 0.14847 ,
                                 0       ,
                                 0       ,
                                -1.546e-4,
                                 0       ,
                                 0       ]))

    b1    = HM83_eq25(T,float_([ 0.307   ,
                                 0       ,
                                 0       ,
                                 6.36e-4 ,
                                 0       ,
                                 0       ]))

    b2 = 0

    Cphi  = HM83_eq25(T,float_([ 0.003710,
                                 4.115   ,
                                 0       ,
                                 0       ,
                                -3.71e-9 ,
                                 0       ]))

    zLi   = +1
    zCl   = -1
    C0    = Cphi / (2 * sqrt(np_abs(zLi * zCl)))

    C1 = 0

    alph1 = 2
    alph2 = -9
    omega = -9

    valid = logical_and(T >= 273.15, T <= 523.15)

    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

# === HOLMES & MESMER 1983 ====================================================
###############################################################################

#%%############################################################################
# === HOLMES & MESMER 1986 ====================================================

# Note that HM86 use alph1 of 1.4 even where there is no beta2 term (p. 502)

def HM86_eq8(T, a):

    TR = 298.15

    # Typo in a[5] term in HM86 has been corrected here

    return a[0]                                                         \
         + a[1] * (TR - TR**2/T)                                        \
         + a[2] * (T**2 + 2*TR**3/T - 3*TR**2)                          \
         + a[3] * (T + TR**2/T - 2*TR)                                  \
         + a[4] * (log(T/TR) + TR/T - 1)                             \
         + a[5] * (1/(T - 263) + (263*T - TR**2) / (T * (TR - 263)**2)) \
         + a[6] * (1/(680 - T) + (TR**2 - 680*T) / (T * (680 - TR)**2))

# --- bC: caesium sulfate -----------------------------------------------------

# --- bC: potassium sulfate ---------------------------------------------------

def bC_K_SO4_HM86(T, P):

    b0    = HM86_eq8(T,float_([ 0         ,
                                7.476e-4  ,
                                0         ,
                                4.265e-3  ,
                               -3.088     ,
                                0         ,
                                0         ]))

    b1    = HM86_eq8(T,float_([ 0.6179    ,
                                6.85e-3   ,
                                5.576e-5  ,
                               -5.841e-2  ,
                                0         ,
                               -0.90      ,
                                0         ]))

    b2 = 0

    Cphi  = HM86_eq8(T,float_([ 9.15467e-3,
                                0         ,
                                0         ,
                               -1.81e-4   ,
                                0         ,
                                0         ,
                                0         ]))

    zK    = +1
    zSO4  = -2
    C0    = Cphi / (2 * sqrt(np_abs(zK * zSO4)))

    C1 = 0

    alph1 = 1.4
    alph2 = -9
    omega = -9

    valid = logical_and(T >= 298.15, T <= 523.15)

    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

# --- bC: lithium sulfate -----------------------------------------------------

# --- bC: sodium sulfate ------------------------------------------------------

def bC_Na_SO4_HM86(T, P):

    b0    = HM86_eq8(T,float_([-   1.727e-2  ,
                                   1.7828e-3 ,
                                   9.133e-6  ,
                                   0         ,
                               -   6.552     ,
                                   0         ,
                               -  96.90      ]))

    b1    = HM86_eq8(T,float_([    0.7534    ,
                                   5.61e-3   ,
                               -   5.7513e-4 ,
                                   1.11068   ,
                               - 378.82      ,
                                   0         ,
                                1861.3       ]))

    b2 = 0

    Cphi  = HM86_eq8(T,float_([    1.1745e-2 ,
                               -   3.3038e-4 ,
                                   1.85794e-5,
                               -   3.9200e-2 ,
                                  14.2130    ,
                                   0         ,
                               -  24.950     ]))

    zNa   = +1
    zSO4  = -2
    C0    = Cphi / (2 * sqrt(np_abs(zNa * zSO4)))

    C1 = 0

    alph1 = 1.4
    alph2 = -9
    omega = -9

    valid = logical_and(T >= 298.15, T <= 523.15)

    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

# === HOLMES & MESMER 1986 ====================================================
###############################################################################

#%%############################################################################
# === PABALAN & PITZER 1987 ===================================================

# Note that there are two Pabalan & Pitzer (1987)'s: one compiling a suite of
#  electrolytes (PP87ii), and one just for NaOH (PP87i).
# There are also a bunch of Phutela & Pitzer papers in similar years, so will
#  need to take care with naming conventions!

# --- bC: sodium hydroxide ----------------------------------------------------

def PP87i_eqNaOH(T, P, a):

    # Pressure in bar

    return a[ 0] \
         + a[ 1] * P \
         + a[ 2] / T \
         + a[ 3] * P / T \
         + a[ 4] * log(T) \
         + a[ 5] * T \
         + a[ 6] * T * P \
         + a[ 7] * T**2 \
         + a[ 8] * T**2 * P \
         + a[ 9] / (T - 227) \
         + a[10] / (647 - T) \
         + a[11] * P / (647 - T)

def bC_Na_OH_PP87i(T, P):

    # Convert dbar to bar
    P_bar = P / 10

    b0 = PP87i_eqNaOH(T, P_bar, [ \
         2.7682478e+2,
        -2.8131778e-3,
        -7.3755443e+3,
         3.7012540e-1,
        -4.9359970e+1,
         1.0945106e-1,
         7.1788733e-6,
        -4.0218506e-5,
        -5.8847404e-9,
         1.1931122e+1,
         2.4824963e00,
        -4.8217410e-3,
    ])

    b1 = PP87i_eqNaOH(T, P_bar, [ \
         4.6286977e+2,
         0           ,
        -1.0294181e+4,
         0           ,
        -8.5960581e+1,
         2.3905969e-1,
         0           ,
        -1.0795894e-4,
         0           ,
         0           ,
         0           ,
         0           ,
    ])

    b2 = 0

    Cphi = PP87i_eqNaOH(T, P_bar, [ \
        -1.6686897e+01,
         4.0534778e-04,
         4.5364961e+02,
        -5.1714017e-02,
         2.9680772e000,
        -6.5161667e-03,
        -1.0553037e-06,
         2.3765786e-06,
         8.9893405e-10,
        -6.8923899e-01,
        -8.1156286e-02,
         0            ,
    ])

    zNa = +1
    zOH = -1
    C0 = Cphi / (2 * sqrt(np_abs(zNa * zOH)))

    C1 = 0

    alph1 = 2
    alph2 = -9
    omega = -9

    valid = logical_and(T >= 298.15, T <= 523.15)

    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid


# --- bC: magnesium chloride --------------------------------------------------

def bC_Mg_Cl_PP87i(T, P):

    b0, b1, b2, _, C1, alph1, alph2, omega, _ = bC_Mg_Cl_dLP83(T, P)

    Cphi = 2.41831e-7 * T**2 \
         - 2.49949e-4 * T \
         + 5.95320e-2

    zMg = +2
    zCl = -1
    C0 = Cphi / (2 * sqrt(np_abs(zMg * zCl)))

    valid = logical_and(T >= 298.15, T <= 473.15)

    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

# === PALABAN & PITZER 1987 ===================================================
###############################################################################

#%%############################################################################
# === SIMONSON ET AL 1987 =====================================================

def SRRJ87_eq7(T, a):

    Tr = 298.15
    return a[0]                      \
         + a[1] * 1e-3 * (T - Tr)    \
         + a[2] * 1e-5 * (T - Tr)**2

# --- bC: potassium chloride --------------------------------------------------

def bC_K_Cl_SRRJ87(T, P):

    # Coefficients from SRRJ87 Table III

    b0   = SRRJ87_eq7(T,float_([ 0.0481,
                                 0.592 ,
                                -0.562 ]))

    b1   = SRRJ87_eq7(T,float_([ 0.2188,
                                 1.500 ,
                                -1.085 ]))

    b2 = 0

    Cphi = SRRJ87_eq7(T,float_([-0.790 ,
                                -0.639 ,
                                 0.613 ]))

    zK    = +1
    zCl   = -1
    C0    = Cphi / (2 * sqrt(np_abs(zK * zCl)))

    C1 = 0

    alph1 = 2
    alph2 = -9
    omega = -9

    valid = logical_and(T >= 278.15, T <= 328.15)

    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

# --- bC: sodium chloride -----------------------------------------------------

def bC_Na_Cl_SRRJ87(T, P):

    # Coefficients from SRRJ87 Table III

    b0   = SRRJ87_eq7(T,float_([ 0.0754,
                                 0.792 ,
                                -0.935 ]))

    b1   = SRRJ87_eq7(T,float_([ 0.2770,
                                 1.006 ,
                                -0.756 ]))

    b2 = 0

    Cphi = SRRJ87_eq7(T,float_([ 1.40  ,
                                -1.20  ,
                                 1.15  ]))

    zNa   = +1
    zCl   = -1
    C0    = Cphi / (2 * sqrt(np_abs(zNa * zCl)))

    C1 = 0

    alph1 = 2
    alph2 = -9
    omega = -9

    valid = logical_and(T >= 278.15, T <= 328.15)

    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

# --- bC: potassium borate ----------------------------------------------------

def bC_K_BOH4_SRRJ87(T, P):

    # Coefficients from SRRJ87 Table III

    b0   = SRRJ87_eq7(T,float_([  0.1469,
                                  2.881 ,
                                  0     ]))

    b1   = SRRJ87_eq7(T,float_([- 0.0989,
                                - 6.876 ,
                                  0     ]))

    b2 = 0

    Cphi = SRRJ87_eq7(T,float_([-56.43  ,
                                - 9.56  ,
                                  0     ]))

    zK    = +1
    zCl   = -1
    C0    = Cphi / (2 * sqrt(np_abs(zK * zCl)))

    C1 = 0

    alph1 = 2
    alph2 = -9
    omega = -9

    valid = logical_and(T >= 278.15, T <= 328.15)

    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

# --- bC: sodium borate -------------------------------------------------------

def bC_Na_BOH4_SRRJ87(T, P):

    # Coefficients from SRRJ87 Table III

    b0   = SRRJ87_eq7(T,float_([- 0.0510,
                                  5.264 ,
                                  0     ]))

    b1   = SRRJ87_eq7(T,float_([  0.0961,
                                -10.68  ,
                                  0     ]))

    b2 = 0

    Cphi = SRRJ87_eq7(T,float_([ 14.98  ,
                                -15.7   ,
                                  0     ]))

    zNa   = +1
    zCl   = -1
    C0    = Cphi / (2 * sqrt(np_abs(zNa * zCl)))

    C1 = 0

    alph1 = 2
    alph2 = -9
    omega = -9

    valid = logical_and(T >= 278.15, T <= 328.15)

    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

# --- theta: borate chloride --------------------------------------------------

def theta_BOH4_Cl_SRRJ87(T, P):

    # Coefficient from SRRJ87 Table III

    theta = -0.056

    valid = logical_and(T >= 278.15, T <= 328.15)

    return theta, valid

# --- psi: potassium borate chloride ------------------------------------------

def psi_K_BOH4_Cl_SRRJ87(T, P):

    psi = 0

    valid = logical_and(T >= 278.15, T <= 328.15)

    return psi, valid

# --- psi: sodium borate chloride ---------------------------------------------

def psi_Na_BOH4_Cl_SRRJ87(T, P):

    # Coefficient from SRRJ87 Table III

    psi = -0.019

    valid = logical_and(T >= 278.15, T <= 328.15)

    return psi, valid

# === SIMONSON ET AL 1987i ====================================================
###############################################################################

#%%############################################################################
# === SIMONSON ET AL 1987ii ===================================================

def SRM87_eqTableIII(T,abc):

    return abc[0] \
         + abc[1] * 1e-3 * (T - 298.15) \
         + abc[2] * 1e-3 * (T - 303.15)**2

# --- bc: magnesium borate ----------------------------------------------------

def bC_Mg_BOH4_SRM87(T, P):

    b0 = SRM87_eqTableIII(T,float_([
        - 0.6230,
          6.496 ,
          0     ]))

    b1 = SRM87_eqTableIII(T,float_([
          0.2515,
        -17.13  ,
          0     ]))

    b2 = SRM87_eqTableIII(T,float_([
        -11.47  ,
          0     ,
        - 3.240 ]))

    C0 = 0
    C1 = 0

    alph1 = 2
    alph2 = -9
    omega = -9

    valid = logical_and(T >= 278.15, T <= 528.15)

    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

# --- bc: magnesium borate ----------------------------------------------------

def bC_Ca_BOH4_SRM87(T, P):

    b0 = SRM87_eqTableIII(T,float_([
        - 0.4462,
          5.393 ,
          0     ]))

    b1 = SRM87_eqTableIII(T,float_([
        - 0.8680,
        -18.20  ,
          0     ]))

    b2 = SRM87_eqTableIII(T,float_([
        -15.88  ,
          0     ,
        - 2.858 ]))

    C0 = 0
    C1 = 0

    alph1 = 2
    alph2 = -9
    omega = -9

    valid = logical_and(T >= 278.15, T <= 528.15)

    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

# === SIMONSON ET AL 1987ii ===================================================
###############################################################################

#%%############################################################################
# === MOLLER 1988 =============================================================

def M88_eq13(T, a):

    return a[0]             \
         + a[1] * T         \
         + a[2] / T         \
         + a[3] * log(T) \
         + a[4] / (T-263.)  \
         + a[5] * T**2      \
         + a[6] / (680.-T)  \
         + a[7] / (T-227.)

# --- bC: calcium chloride ----------------------------------------------------

def b0_Ca_Cl_M88(T, P):
    return M88_eq13(T,float_([-9.41895832e+1,
                              -4.04750026e-2,
                               2.34550368e+3,
                               1.70912300e+1,
                              -9.22885841e-1,
                               1.51488122e-5,
                              -1.39082000e00,
                               0            ]))

def b1_Ca_Cl_M88(T, P):
    return M88_eq13(T,float_([ 3.47870000e00,
                              -1.54170000e-2,
                               0            ,
                               0            ,
                               0            ,
                               3.17910000e-5,
                               0            ,
                               0            ]))

def Cphi_Ca_Cl_M88(T, P):
    return M88_eq13(T,float_([-3.03578731e+1,
                              -1.36264728e-2,
                               7.64582238e+2,
                               5.50458061e00,
                              -3.27377782e-1,
                               5.69405869e-6,
                              -5.36231106e-1,
                               0            ]))

def bC_Ca_Cl_M88(T, P):

    b0    = b0_Ca_Cl_M88(T, P)
    b1    = b1_Ca_Cl_M88(T, P)
    b2 = 0

    Cphi  = Cphi_Ca_Cl_M88(T, P)
    zCa   = +2
    zCl   = -1
    C0    = Cphi / (2 * sqrt(np_abs(zCa * zCl)))

    C1 = 0

    alph1 = 2
    alph2 = -9
    omega = -9

    valid = logical_and(T >= 298.15, T <= 523.15)

    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

# --- bC: calcium sulfate -----------------------------------------------------

def bC_Ca_SO4_M88(T, P):

    b0 = 0.15

    b1    = 3.00

    b2    = M88_eq13(T,float_([-1.29399287e+2,
                                4.00431027e-1,
                                0            ,
                                0            ,
                                0            ,
                                0            ,
                                0            ,
                                0            ]))

    C0 = 0

    C1 = 0

    alph1 = 1.4
    alph2 = 12
    omega = -9

    valid = logical_and(T >= 298.15, T <= 523.15)

    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

# --- bC: sodium chloride -----------------------------------------------------

def bC_Na_Cl_M88(T, P):

    b0    = M88_eq13(T,float_([ 1.43783204e+1,
                                5.60767406e-3,
                               -4.22185236e+2,
                               -2.51226677e00,
                                0            ,
                               -2.61718135e-6,
                                4.43854508e00,
                               -1.70502337e00]))

    b1    = M88_eq13(T,float_([-4.83060685e-1,
                                1.40677479e-3,
                                1.19311989e+2,
                                0            ,
                                0            ,
                                0            ,
                                0            ,
                               -4.23433299e00]))

    b2 = 0

    Cphi  = M88_eq13(T,float_([-1.00588714e-1,
                               -1.80529413e-5,
                                8.61185543e00,
                                1.24880954e-2,
                                0            ,
                                3.41172108e-8,
                                6.83040995e-2,
                                2.93922611e-1]))

    zNa   = +1
    zCl   = -1
    C0    = Cphi / (2 * sqrt(np_abs(zNa * zCl)))

    C1 = 0

    alph1 = 2
    alph2 = -9
    omega = -9

    valid = logical_and(T >= 273.15, T <= 573.15)

    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

# --- bC: sodium sulfate ------------------------------------------------------

def bC_Na_SO4_M88(T, P):

    b0    = M88_eq13(T,float_([ 8.16920027e+1,
                                3.01104957e-2,
                               -2.32193726e+3,
                               -1.43780207e+1,
                               -6.66496111e-1,
                               -1.03923656e-5,
                                0            ,
                                0            ]))

    b1    = M88_eq13(T,float_([ 1.00463018e+3,
                                5.77453682e-1,
                               -2.18434467e+4,
                               -1.89110656e+2,
                               -2.03550548e-1,
                               -3.23949532e-4,
                                1.46772243e+3,
                                0            ]))

    b2 = 0

    Cphi  = M88_eq13(T,float_([-8.07816886e+1,
                               -3.54521126e-2,
                                2.02438830e+3,
                                1.46197730e+1,
                               -9.16974740e-2,
                                1.43946005e-5,
                               -2.42272049e00,
                                0            ]))

    zNa   = +1
    zSO4  = -2
    C0    = Cphi / (2 * sqrt(np_abs(zNa * zSO4)))

    C1 = 0

    alph1 = 2
    alph2 = -9
    omega = -9

    valid = logical_and(T >= 273.15, T <= 573.15)

    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

# --- theta: calcium sodium ---------------------------------------------------

def theta_Ca_Na_M88(T, P):

    theta = 0.05

    valid = logical_and(T >= 298.15, T <= 523.15)

    return theta, valid

# --- theta: chloride sulfate -------------------------------------------------

def theta_Cl_SO4_M88(T, P):

    theta = 0.07

    valid = logical_and(T >= 298.15, T <= 423.15)

    return theta, valid

# --- psi: calcium sodium chloride --------------------------------------------

def psi_Ca_Na_Cl_M88(T, P):

    psi = -0.003

    valid = logical_and(T >= 298.15, T <= 523.15)

    return psi, valid

# --- psi: calcium sodium sulfate ---------------------------------------------

def psi_Ca_Na_SO4_M88(T, P):

    psi = -0.012

    valid = logical_and(T >= 298.15, T <= 523.15)

    return psi, valid

# --- psi: calcium chloride sulfate -------------------------------------------

def psi_Ca_Cl_SO4_M88(T, P):

    psi = -0.018

    valid = logical_and(T >= 298.15, T <= 523.15)

    return psi, valid

# --- psi: sodium chloride sulfate --------------------------------------------

def psi_Na_Cl_SO4_M88(T, P):

    psi = -0.009

    valid = logical_and(T >= 298.15, T <= 423.15)

    return psi, valid

# --- dissociation: water -----------------------------------------------------

def dissoc_H2O_M88(T, P):

    lnKw  = M88_eq13(T,float_([ 1.04031130e+3,
                                4.86092851e-1,
                               -3.26224352e+4,
                               -1.90877133e+2,
                               -5.35204850e-1,
                               -2.32009393e-4,
                                5.20549183e+1,
                                0            ]))

    valid = logical_and(T >= 298.15, T <= 523.15)

    return exp(lnKw), valid

# === MOLLER 1988 =============================================================
###############################################################################

#%%############################################################################
# === GREENBERG & MOLLER 1989 =================================================

# --- inherit from M88 --------------------------------------------------------

GM89_eq3 = M88_eq13

# --- bC: calcium chloride ----------------------------------------------------

def Cphi_Ca_Cl_GM89(T, P):
    return GM89_eq3(T,float_([ 1.93056024e+1,
                               9.77090932e-3,
                              -4.28383748e+2,
                              -3.57996343e00,
                               8.82068538e-2,
                              -4.62270238e-6,
                               9.91113465e00,
                               0            ]))

def bC_Ca_Cl_GM89(T, P):

    b0,b1,b2,_,C1,alph1,alph2,omega,valid = bC_Ca_Cl_M88(T, P)

    Cphi  = Cphi_Ca_Cl_GM89(T, P)

    zCa   = +2
    zCl   = -1
    C0    = Cphi / (2 * sqrt(np_abs(zCa * zCl)))

    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

# --- bC: potassium chloride --------------------------------------------------

def bC_K_Cl_GM89(T, P):

    b0    = GM89_eq3(T,float_([ 2.67375563e+1,
                                1.00721050e-2,
                               -7.58485453e+2,
                               -4.70624175e00,
                                0            ,
                               -3.75994338e-6,
                                0            ,
                                0            ]))

    b1    = GM89_eq3(T,float_([-7.41559626e00,
                                0            ,
                                3.22892989e+2,
                                1.16438557e00,
                                0            ,
                                0            ,
                                0            ,
                               -5.94578140e00]))

    b2 = 0

    Cphi  = GM89_eq3(T,float_([-3.30531334e00,
                               -1.29807848e-3,
                                9.12712100e+1,
                                5.86450181e-1,
                                0            ,
                                4.95713573e-7,
                                0            ,
                                0            ]))

    zK    = +1
    zCl   = -1
    C0    = Cphi / (2 * sqrt(np_abs(zK * zCl)))

    C1 = 0

    alph1 = 2
    alph2 = -9
    omega = -9

    valid = logical_and(T >= 273.15, T <= 523.15)

    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

# --- bC: potassium sulfate ---------------------------------------------------

def bC_K_SO4_GM89(T, P):

    b0    = GM89_eq3(T,float_([ 4.07908797e+1,
                                8.26906675e-3,
                               -1.41842998e+3,
                               -6.74728848e00,
                                0            ,
                                0            ,
                                0            ,
                                0            ]))

    b1    = GM89_eq3(T,float_([-1.31669651e+1,
                                2.35793239e-2,
                                2.06712594e+3,
                                0            ,
                                0            ,
                                0            ,
                                0            ,
                                0            ]))

    b2 = 0

    Cphi  = -0.0188

    zK    = +1
    zSO4  = -2
    C0    = Cphi / (2 * sqrt(np_abs(zK * zSO4)))

    C1 = 0

    alph1 = 2
    alph2 = -9
    omega = -9

    valid = logical_and(T >= 273.15, T <= 523.15)

    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

# --- theta: calcium potassium ------------------------------------------------

def theta_Ca_K_GM89(T, P):

    theta = 0.1156

    valid = logical_and(T >= 273.15, T <= 523.15)

    return theta, valid

# --- theta: potassium sodium -------------------------------------------------

def theta_K_Na_GM89(T, P):

    theta = GM89_eq3(T,float_([-5.02312111e-2,
                                0            ,
                                1.40213141e+1,
                                0            ,
                                0            ,
                                0            ,
                                0            ,
                                0            ]))

    valid = logical_and(T >= 273.15, T <= 523.15)

    return theta, valid

# --- psi: calcium potassium chloride -----------------------------------------

def psi_Ca_K_Cl_GM89(T, P):

    psi = GM89_eq3(T,float_([ 4.76278977e-2,
                                0            ,
                               -2.70770507e+1,
                                0            ,
                                0            ,
                                0            ,
                                0            ,
                                0            ]))

    valid = logical_and(T >= 273.15, T <= 523.15)

    return psi, valid

# --- psi: calcium potassium sulfate ------------------------------------------

def psi_Ca_K_SO4_GM89(T, P):

    theta = 0

    valid = logical_and(T >= 273.15, T <= 523.15)

    return theta, valid

# --- psi: potassium sodium chloride ------------------------------------------

def psi_K_Na_Cl_GM89(T, P):

    psi = GM89_eq3(T,float_([ 1.34211308e-2,
                                0            ,
                               -5.10212917e00,
                                0            ,
                                0            ,
                                0            ,
                                0            ,
                                0            ]))

    valid = logical_and(T >= 273.15, T <= 523.15)

    return psi, valid

# --- psi: potassium sodium sulfate -------------------------------------------

def psi_K_Na_SO4_GM89(T, P):

    psi = GM89_eq3(T,float_([ 3.48115174e-2,
                                0            ,
                               -8.21656777e00,
                                0            ,
                                0            ,
                                0            ,
                                0            ,
                                0            ]))

    valid = logical_and(T >= 273.15, T <= 423.15)

    return psi, valid

# --- psi: potassium chloride sulfate -----------------------------------------

def psi_K_Cl_SO4_GM89(T, P):

    psi = GM89_eq3(T,float_([-2.12481475e-1,
                                2.84698333e-4,
                                3.75619614e+1,
                                0            ,
                                0            ,
                                0            ,
                                0            ,
                                0            ]))

    valid = logical_and(T >= 273.15, T <= 523.15)

    return psi, valid

# === GREENBERG & MOLLER 1989 =================================================
###############################################################################

#%%############################################################################
# === ARCHER 1992 =============================================================

# Set up T/P function
def A92ii_eq36(T, P, a):

    # Pressure in MPa
    # a[5] and a[6] multipliers are corrected for typos in A92ii

    return  a[ 0]                               \
          + a[ 1] * 10**-3 * T                  \
          + a[ 2] * 4e-6 * T**2                 \
          + a[ 3] * 1 / (T - 200)               \
          + a[ 4] * 1 / T                       \
          + a[ 5] * 100 / (T - 200)**2          \
          + a[ 6] * 200 / T**2                  \
          + a[ 7] * 8e-9 * T**3                 \
          + a[ 8] * 1 / (650 - T)**0.5          \
          + a[ 9] * 10**-5 * P                  \
          + a[10] * 2e-4 * P / (T - 225)        \
          + a[11] * 100 * P / (650 - T)**3      \
          + a[12] * 2e-8 * P * T                \
          + a[13] * 2e-4 * P / (650 - T)        \
          + a[14] * 10**-7 * P**2               \
          + a[15] * 2e-6 * P**2 / (T - 225)     \
          + a[16] * P**2 / (650 - T)**3         \
          + a[17] * 2e-10 * P**2 * T            \
          + a[18] * 4e-13 * P**2 * T**2         \
          + a[19] * 0.04 * P / (T - 225)**2     \
          + a[20] * 4e-11 * P * T**2            \
          + a[21] * 2e-8 * P**3 / (T - 225)     \
          + a[22] * 0.01 * P**3 / (650 - T)**3  \
          + a[23] * 200 / (650 - T)**3

# --- bC: sodium chloride -----------------------------------------------------

def bC_Na_Cl_A92ii(T, P):

    # Convert dbar to MPa
    P_MPa = P / 100

    # Coefficients from A92ii Table 2, with noted corrections

    b0 = A92ii_eq36(T, P_MPa, [ \
          0.242408292826506,
          0,
        - 0.162683350691532,
          1.38092472558595,
          0,
          0,
        -67.2829389568145,
          0,
          0.625057580755179,
        -21.2229227815693,
         81.8424235648693,
        - 1.59406444547912,
          0,
          0,
         28.6950512789644,
        -44.3370250373270,
          1.92540008303069,
        -32.7614200872551,
          0,
          0,
         30.9810098813807,
          2.46955572958185,
        - 0.725462987197141,
         10.1525038212526,
    ])

    b1 = A92ii_eq36(T, P_MPa, [ \
        - 1.90196616618343,
          5.45706235080812,
          0,
        -40.5376417191367,
          0,
          0,
          4.85065273169753  * 1e2,
        - 0.661657744698137,
          0,
          0,
          2.42206192927009  * 1e2,
          0,
        -99.0388993875343,
          0,
          0,
        -59.5815563506284,
          0,
          0,
          0,
          0,
          0,
          0,
          0,
          0,
    ])

    b2 = 0

    C0 = A92ii_eq36(T, P_MPa, [ \
          0,
        - 0.0412678780636594,
          0.0193288071168756,
        - 0.338020294958017,      # typo in A92ii
          0,
          0.0426735015911910,
          4.14522615601883,
        - 0.00296587329276653,
          0,
          1.39697497853107,
        - 3.80140519885645,
          0.06622025084,          # typo in A92ii - "Rard's letter"
          0,
        -16.8888941636379,
        - 2.49300473562086,
          3.14339757137651,
          0,
          2.79586652877114,
          0,
          0,
          0,
          0,
          0,
        - 0.502708980699711,
    ])

    C1 = A92ii_eq36(T, P_MPa, [ \
          0.788987974218570,
        - 3.67121085194744,
          1.12604294979204,
          0,
          0,
        -10.1089172644722,
          0,
          0,
          0,
          0,
          0,
          0,
          0,
          0,
          0,
          0,
          0,
          0,
          0,
          0,
          0,
          0,
          0,
         16.6503495528290,
    ])

    # Alpha and omega values
    alph1 = 2
    alph2 = -9
    omega = 2.5

    # Validity range
    valid = logical_and(T >= 250, T <= 600)
    valid = logical_and(valid, P_MPa <= 100)

    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

# === ARCHER 1992 =============================================================
###############################################################################

#%%############################################################################
# === CAMPBELL ET AL 1993 =====================================================

# --- inherit from M88 --------------------------------------------------------

CMR93_eq31 = M88_eq13

# --- bC: hydrogen chloride ---------------------------------------------------

def bC_H_Cl_CMR93(T, P):

    # b0 a[1] term corrected here for typo, following WM13
    b0    = CMR93_eq31(T,float_([   1.2859     ,
                                 -  2.1197e-3  ,
                                 -142.5877     ,
                                    0          ,
                                    0          ,
                                    0          ,
                                    0          ,
                                    0          ]))

    b1    = CMR93_eq31(T,float_([-  4.4474     ,
                                    8.425698e-3,
                                  665.7882     ,
                                    0          ,
                                    0          ,
                                    0          ,
                                    0          ,
                                    0          ]))

    b2 = 0

    Cphi  = CMR93_eq31(T,float_([-  0.305156   ,
                                    5.16e-4    ,
                                   45.52154    ,
                                    0          ,
                                    0          ,
                                    0          ,
                                    0          ,
                                    0          ]))

    zH    = +1
    zCl   = -1
    C0    = Cphi / (2 * sqrt(np_abs(zH * zCl)))

    C1 = 0

    alph1 = 2
    alph2 = -9
    omega = -9

    valid = logical_and(T >= 273.15, T <= 328.15)

    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

# --- theta: hydrogen potassium -----------------------------------------------

def theta_H_K_CMR93(T, P):

    # assuming CMR93's lowercase t means temperature in degC
    theta = 0.005 - 0.0002275 * (T - Tzero)

    valid = logical_and(T >= 273.15, T <= 328.15)

    return theta, valid

# --- theta: hydrogen sodium --------------------------------------------------

def theta_H_Na_CMR93(T, P):

    # assuming CMR93's lowercase t means temperature in degC
    theta = 0.0342 - 0.000209 * (T - Tzero)

    valid = logical_and(T >= 273.15, T <= 328.15)

    return theta, valid

# --- psi: hydrogen potassium chloride ----------------------------------------

def psi_H_K_Cl_CMR93(T, P):

    psi = 0

    valid = logical_and(T >= 273.15, T <= 523.15)

    return psi, valid

# --- psi: hydrogen sodium chloride -------------------------------------------

def psi_H_Na_Cl_CMR93(T, P):

    psi = 0

    valid = logical_and(T >= 273.15, T <= 523.15)

    return psi, valid

# === CAMPBELL ET AL 1993 =====================================================
###############################################################################

#%%############################################################################
# === HOVEY, PITZER AND RARD 1993 =============================================

def HPR93_eq36(T, a):

    Tref = 298.15

    return a[0] + a[1] * (1/T - 1/Tref) + a[2] * log(T/Tref)

# --- bC: sodium sulfate ------------------------------------------------------

def bC_Na_SO4_HPR93(T, P):

    b0    = HPR93_eq36(T,float_([  0.006536438,
                                 -30.197349   ,
                                 - 0.20084955 ]))

    b1    = HPR93_eq36(T,float_([  0.87426420 ,
                                 -70.014123   ,
                                   0.2962095  ]))

    b2 = 0

    Cphi  = HPR93_eq36(T,float_([  0.007693706,
                                   4.5879201  ,
                                   0.019471746]))

    zNa   = +1
    zSO4  = -2
    C0    = Cphi / (2 * sqrt(np_abs(zNa * zSO4)))

    C1 = 0

    alph1 = 1.7
    alph2 = -9
    omega = -9

    valid = logical_and(T >= 273., T <= 373.)

    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

# --- bC: sodium bisulfate ----------------------------------------------------

# Coefficients from HPR93 Table 3 for low ionic strengths

def bC_Na_HSO4_HPR93(T, P):

    b0 = 0.0670967
    b1 = 0.3826401
    b2 = 0

    Cphi = -0.0039056

    zNa   = +1
    zHSO4 = -1
    C0    = Cphi / (2 * sqrt(np_abs(zNa * zHSO4)))

    C1 = 0

    alph1 = 2
    alph2 = -9
    omega = -9

    valid = T == 298.15

    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid


# === HOVEY, PITZER AND RARD 1993 =============================================
###############################################################################

#%%############################################################################
# === CLEGG ET AL 1994 ========================================================

# --- betas and Cs ------------------------------------------------------------

CRP94_Tr = 328.15 # K

def CRP94_eq24(T,q):
    return q[0] + 1e-3 *                 \
        ( (T-CRP94_Tr)    * q[1]         \
        + (T-CRP94_Tr)**2 * q[2] / 2.    \
        + (T-CRP94_Tr)**3 * q[3] / 6.)

# --- bC: hydrogen bisulfate --------------------------------------------------

def bC_H_HSO4_CRP94(T, P):

    # Evaluate coefficients, parameters from CRP94 Table 6
    b0 = CRP94_eq24(T,float_([  0.227784933   ,
                              - 3.78667718    ,
                              - 0.124645729   ,
                              - 0.00235747806 ]))

    b1 = CRP94_eq24(T,float_([  0.372293409   ,
                                1.50          ,
                                0.207494846   ,
                                0.00448526492 ]))

    b2 = 0

    C0 = CRP94_eq24(T,float_([- 0.00280032520 ,
                                0.216200279   ,
                                0.0101500824  ,
                                0.000208682230]))

    C1 = CRP94_eq24(T,float_([- 0.025         ,
                               18.1728946     ,
                                0.382383535   ,
                                0.0025        ]))

    alph1 = 2
    alph2 = -9
    omega = 2.5

    valid = logical_and(T >= 273.15, T <= 328.15)

    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

# --- bC: hydrogen sulfate ----------------------------------------------------

def bC_H_SO4_CRP94(T, P):

    # Evaluate coefficients, parameters from CRP94 Table 6
    b0 = CRP94_eq24(T,float_([  0.0348925351  ,
                                4.97207803    ,
                                0.317555182   ,
                                0.00822580341 ]))

    b1 = CRP94_eq24(T,float_([- 1.06641231    ,
                              -74.6840429     ,
                              - 2.26268944    ,
                              - 0.0352968547  ]))

    b2 = 0

    C0 = CRP94_eq24(T,float_([  0.00764778951 ,
                              - 0.314698817   ,
                              - 0.0211926525  ,
                              - 0.000586708222]))

    C1 = CRP94_eq24(T,float_([  0.0           ,
                              - 0.176776695   ,
                              - 0.731035345   ,
                                0.0           ]))

    alph1 = 2 - 1842.843 * (1/T - 1/298.15)
    alph2 = -9
    omega = 2.5

    valid = logical_and(T >= 273.15, T <= 328.15)

    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

# --- theta: bisulfate sulfate ------------------------------------------------

def theta_HSO4_SO4_CRP94(T, P):

    theta = 0

    valid = logical_and(T >= 273.15, T <= 328.15)

    return theta, valid

# --- psi: hydrogen bisulfate sulfate -----------------------------------------

def psi_H_HSO4_SO4_CRP94(T, P):

    psi = 0

    valid = logical_and(T >= 273.15, T <= 328.15)

    return psi, valid

# --- dissociation: bisulfate -------------------------------------------------

def dissoc_HSO4_CRP94(T, P):

    valid = logical_and(T >= 273.15, T <= 328.15)

    return 10**(562.69486 - 102.5154 * log(T) \
        - 1.117033e-4 * T**2 + 0.2477538*T - 13273.75/T), valid

# === CLEGG ET AL 1994 ========================================================
###############################################################################

#%%############################################################################
# === ARCHER 1999 =============================================================

def A99_eq22(T, a):

    Tref  = 298.15

    return   a[0]                        \
           + a[1] * (T - Tref)    * 1e-2 \
           + a[2] * (T - Tref)**2 * 1e-5 \
           + a[3] * 1e2 / (T - 225)      \
           + a[4] * 1e3 /  T             \
           + a[5] * 1e6 / (T - 225)**3

# --- bC: potassium chloride --------------------------------------------------

def bC_K_Cl_A99(T, P):

    # KCl T parameters from A99 Table 4
    b0 = A99_eq22(T,float_( \
           [ 0.413229483398493  ,
            -0.0870121476114027 ,
             0.101413736179231  ,
            -0.0199822538522801 ,
            -0.0998120581680816 ,
             0                  ]))

    b1 = A99_eq22(T,float_( \
           [ 0.206691413598171  ,
             0.102544606022162  ,
             0,
             0,
             0,
            -0.00188349608000903]))

    b2 = 0

    C0 = A99_eq22(T,float_( \
           [-0.00133515934994478,
             0,
             0,
             0.00234117693834228,
            -0.00075896583546707,
             0                  ]))

    C1 = 0

    # Alpha and omega values
    alph1 = 2
    alph2 = -9
    omega = -9

    # Validity range
    valid = logical_and(T >= 260, T <= 420)

    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

# === ARCHER 1999 =============================================================
###############################################################################

#%%############################################################################
# === RARD & CLEGG 1999 =======================================================

# --- bC: magnesium bisulfate -------------------------------------------------

def bC_Mg_HSO4_RC99(T, P):

    # RC99 Table 6, left column
    b0 = 0.40692
    b1 = 1.6466
    b2 = 0
    C0 = 0.024293
    C1 = -0.127194

    # Alpha and omega values
    alph1 = 2
    alph2 = -9
    omega = 1

    # Validity range
    valid = T == 298.15

    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

# --- psi: hydrogen magnesium bisulfate ---------------------------------------

def psi_H_Mg_HSO4_RC99(T, P):

    # RC99 Table 6, left column
    psi = -0.027079
    valid = T == 298.15

    return psi, valid

# --- psi: hydrogen magnesium sulfate -----------------------------------------

def psi_H_Mg_SO4_RC99(T, P):

    # RC99 Table 6, left column
    psi = -0.047368
    valid = T == 298.15

    return psi, valid

# --- psi: magnesium bisulfate sulfate ----------------------------------------

def psi_Mg_HSO4_SO4_RC99(T, P):

    # RC99 Table 6, left column
    psi = -0.078418
    valid = T == 298.15

    return psi, valid

# === RARD & CLEGG 1999 =======================================================
###############################################################################

#%%############################################################################
# === WATERS & MILLERO 2013 ===================================================
#
# Some are functions that WM13 declared came from another source, but I
#  couldn't find them there, so copied directly from WM13 instead.
#
# Others were just declared by WM13 as zero. These all seem to agree with
#  HMW84; it's unclear why HMW84 wasn't cited by WM13 for these.

#~~~~ HMW84 + P91 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# First, a few functions that WM13 constructed by taking 298.15 K coefficients
#  from HMW84, and correcting for temperature using derivatives from P91

# --- bC: calcium sulfate -----------------------------------------------------

def bC_Ca_SO4_WM13(T, P):

    # Define reference temperature
    TR = 298.15

    # Inherit 298.15 K values from HMW84
    b0, b1, b2, C0, C1, alph1, alph2, omega, valid = bC_Ca_SO4_HMW84(T, P)

    # WM13 use temperature derivatives from P91
    # The b0 temperature correction in P91 is zero
    b1 = b1 + (T - TR) * P91_Ch3_T13_II['Ca-SO4']['b1']
    b2 = b2 + (T - TR) * P91_Ch3_T13_II['Ca-SO4']['b2']
    # The C0 temperature correction in P91 is zero

    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

# --- bC: calcium bisulfate ---------------------------------------------------

def bC_Ca_HSO4_WM13(T, P):

    # Define reference temperature
    TR = 298.15

    # Inherit 298.15 K values from HMW84
    b0, b1, b2, C0, C1, alph1, alph2, omega, valid = bC_Ca_HSO4_HMW84(T, P)

    # WM13 use temperature derivatives for Ca-ClO4 from P91, but with typos
    b0 = b0 + (T - TR) * P91_Ch3_T13_I['Ca-ClO4']['b0']
    b1 = b1 + (T - TR) * P91_Ch3_T13_I['Ca-ClO4']['b1']
    C0 = C0 + (T - TR) * P91_Ch3_T13_I['Ca-ClO4']['C0']

    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

# --- bC: potassium bisulfate -------------------------------------------------

def bC_K_HSO4_WM13(T, P):

    # Define reference temperature
    TR = 298.15

    # Inherit 298.15 K values from HMW84
    b0, b1, b2, C0, C1, alph1, alph2, omega, valid = bC_K_HSO4_HMW84(T, P)

    # WM13 use temperature derivatives for K-ClO4 from P91
    b0 = b0 + (T - TR) * P91_Ch3_T12['K-ClO4']['b0']
    b1 = b1 + (T - TR) * P91_Ch3_T12['K-ClO4']['b1']
    # The Cphi temperature correction in P91 is zero

    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# --- theta: calcium hydrogen -------------------------------------------------

def theta_Ca_H_MarChemSpec(T, P):
    # 1. WM13 cite the wrong reference for this (they say RXX80)
    # 2. The equation given by WM13 doesn't match RGO82
    # 3. RGO82 give a 25degC value but no temperature coefficient
    # So MarChemSpec uses RGO82's 25degC value plus the WM13 temperature cxn

    thetar = theta_Ca_H_RGO82(T, P)[0]

    theta = thetar + 3.275e-4 * (T - 298.15)

    valid = logical_and(T >= 273.15, T <= 323.15)

    return theta, valid

# --- bC: sodium sulfate ------------------------------------------------------

def bC_Na_HSO4_HPR93viaWM13(T, P):
    # WM13 Table A1 - can't find where HPR93 state this
    return bC_none(T, P)

# --- theta: bisulfate sulfate ------------------------------------------------

def theta_HSO4_SO4_WM13(T, P):
    # WM13 Table A7
    return theta_none(T, P)

# --- psi: hydrogen chloride sulfate ------------------------------------------

def psi_H_Cl_SO4_WM13(T, P):
    # WM13 Table A8
    return psi_none(T, P)

# --- psi: hydrogen chloride hydroxide ----------------------------------------

def psi_H_Cl_OH_WM13(T, P):
    # WM13 Table A8
    return psi_none(T, P)

# --- psi: magnesium chloride hydroxide ---------------------------------------

def psi_Mg_Cl_OH_WM13(T, P):
    # WM13 Table A8
    return psi_none(T, P)

# --- psi: calcium bisulfate sulfate ------------------------------------------

def psi_Ca_HSO4_SO4_WM13(T, P):
    # WM13 Table A8
    return psi_none(T, P)

# --- psi: hydrogen hydroxide sulfate ------------------------------------------

def psi_H_OH_SO4_WM13(T, P):
    # WM13 Table A8
    return psi_none(T, P)

# --- psi: magnesium hydroxide sulfate ----------------------------------------

def psi_Mg_OH_SO4_WM13(T, P):
    # WM13 Table A8
    return psi_none(T, P)

# --- psi: calcium hydroxide sulfate ------------------------------------------

def psi_Ca_OH_SO4_WM13(T, P):
    # WM13 Table A8
    return psi_none(T, P)

# --- psi: hydrogen sodium sulfate --------------------------------------------

def psi_H_Na_SO4_WM13(T, P):
    # WM13 Table A9
    return psi_none(T, P)

# --- psi: calcium hydrogen sulfate -------------------------------------------

def psi_Ca_H_SO4_WM13(T, P):
    # WM13 Table A9
    return psi_none(T, P)

# --- psi: calcium hydrogen bisulfate -----------------------------------------

def psi_Ca_H_HSO4_WM13(T, P):
    # WM13 Table A9
    return psi_none(T, P)

# --- psi: magnesium sodium bisulfate -----------------------------------------

def psi_Mg_Na_HSO4_WM13(T, P):
    # WM13 Table A9
    return psi_none(T, P)

# --- psi: calcium sodium bisulfate -------------------------------------------

def psi_Ca_Na_HSO4_WM13(T, P):
    # WM13 Table A9
    return psi_none(T, P)

# --- psi: potassium sodium bisulfate -----------------------------------------

def psi_K_Na_HSO4_WM13(T, P):
    # WM13 Table A9
    return psi_none(T, P)

# --- psi: calcium magnesium bisulfate ----------------------------------------

def psi_Ca_Mg_HSO4_WM13(T, P):
    # WM13 Table A9
    return psi_none(T, P)

# --- psi: potassium magnesium bisulfate --------------------------------------

def psi_K_Mg_HSO4_WM13(T, P):
    # WM13 Table A9
    return psi_none(T, P)

# --- psi: calcium potassium sulfate ------------------------------------------

def psi_Ca_K_SO4_WM13(T, P):
    # WM13 Table A9
    return psi_none(T, P)

# --- psi: calcium potassium bisulfate ----------------------------------------

def psi_Ca_K_HSO4_WM13(T, P):
    # WM13 Table A9
    return psi_none(T, P)

# === WATERS & MILLERO 2013 ===================================================
###############################################################################

#%%############################################################################
# === GALLEGO-URREA & TURNER 2017 =============================================

# --- bC: sodium chloride -----------------------------------------------------

def bC_Na_Cl_GT17simopt(T, P):

    # From G17 Supp. Info. Table S6, 'simultaneous optimisation'
    b0 = 0.07722
    b1 = 0.26768
    b2 = 0
    Cphi  = 0.001628

    zNa   = +1
    zCl   = -1
    C0    = Cphi / (2 * sqrt(np_abs(zNa * zCl)))

    C1 = 0

    alph1 = 2
    alph2 = -9
    omega = -9

    valid = T == 298.15

    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

# --- bC: trisH+ chloride -----------------------------------------------------

def bC_trisH_Cl_GT17simopt(T, P):

    # From G17 Supp. Info. Table S6, 'simultaneous optimisation'
    b0     = 0.04181
    b1     = 0.16024
    b2     = 0
    Cphi   = -0.00132

    ztrisH = +1
    zCl    = -1
    C0     = Cphi / (2 * sqrt(np_abs(ztrisH * zCl)))

    C1     = 0

    alph1  = 2
    alph2  = -9
    omega  = -9

    valid  = T == 298.15

    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

# --- bC: trisH+ sulfate ------------------------------------------------------

def bC_trisH_SO4_GT17simopt(T, P):

    # From G17 Supp. Info. Table S6, 'simultaneous optimisation'
    b0     = 0.09746
    b1     = 0.52936
    b2     = 0
    Cphi   = -0.004957

    ztrisH = +1
    zSO4   = -2
    C0     = Cphi / (2 * sqrt(np_abs(ztrisH * zSO4)))

    C1     = 0

    alph1  = 2
    alph2  = -9
    omega  = -9

    valid  = T == 298.15

    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

# --- theta: hydrogen trisH ---------------------------------------------------

def theta_H_trisH_GT17simopt(T, P):

    # From G17 Supp. Info. Table S6, 'simultaneous optimisation'
    theta = -0.00575
    valid = T == 298.15

    return theta, valid

# --- psi: hydrogen trisH chloride --------------------------------------------

def psi_H_trisH_Cl_GT17simopt(T, P):

    # From G17 Supp. Info. Table S6, 'simultaneous optimisation'
    psi = -0.00700
    valid = T == 298.15

    return psi, valid

# --- lambd: tris trisH -------------------------------------------------------

def lambd_tris_trisH_GT17simopt(T, P):

    # From G17 Supp. Info. Table S6, 'simultaneous optimisation'
    lambd = 0.06306
    valid = T == 298.15

    return lambd, valid

# --- lambd: tris sodium ------------------------------------------------------

def lambd_tris_Na_GT17simopt(T, P):

    # From G17 Supp. Info. Table S6, 'simultaneous optimisation'
    lambd = 0.01580
    valid = T == 298.15

    return lambd, valid

# --- lambd: tris potassium ---------------------------------------------------

def lambd_tris_K_GT17simopt(T, P):

    # From G17 Supp. Info. Table S6, 'simultaneous optimisation'
    lambd = 0.02895
    valid = T == 298.15

    return lambd, valid

# --- lambd: tris magnesium ---------------------------------------------------

def lambd_tris_Mg_GT17simopt(T, P):

    # From G17 Supp. Info. Table S6, 'simultaneous optimisation'
    lambd = -0.14505
    valid = T == 298.15

    return lambd, valid

# --- lambd: tris calcium -----------------------------------------------------

def lambd_tris_Ca_GT17simopt(T, P):

    # From G17 Supp. Info. Table S6, 'simultaneous optimisation'
    lambd = -0.31081
    valid = T == 298.15

    return lambd, valid

# === GALLEGO-URREA & TURNER 2017 =============================================
###############################################################################

#%%############################################################################
# === ZEZIN & DRIESNER 2017 ===================================================

def ZD17_eq8(T, P, b):

    # T = temperature in K
    # P = pressure in MPa

    return b[ 0] \
         + b[ 1] *  T/1000 \
         + b[ 2] * (T/500)**2 \
         + b[ 3] / (T - 215) \
         + b[ 4] * 1e4 / (T - 215)**3 \
         + b[ 5] * 1e2 / (T - 215)**2 \
         + b[ 6] * 2e2 /  T**2 \
         + b[ 7] * (T/500)**3 \
         + b[ 8] / (650 - T)**0.5 \
         + b[ 9] * 1e-5 * P \
         + b[10] * 2e-4 * P / (T - 225) \
         + b[11] * 1e2  * P / (650 - T)**3 \
         + b[12] * 1e-5 * P *  T/500 \
         + b[13] * 2e-4 * P / (650 - T) \
         + b[14] * 1e-7 * P**2 \
         + b[15] * 2e-6 * P**2 / (T - 225) \
         + b[16] * P**2 / (650 - T)**3 \
         + b[17] * 1e-7 * P**2 *  T/500 \
         + b[18] * 1e-7 * P**2 * (T/500)**2 \
         + b[19] * 4e-2 * P / (T - 225)**2 \
         + b[20] * 1e-5 * P * (T/500)**2 \
         + b[21] * 2e-8 * P**3 / (T - 225) \
         + b[22] * 1e-2 * P**3 / (650 - T)**3 \
         + b[23] * 2e2  / (650 - T)**3

# --- bC: potassium chloride --------------------------------------------------

def bC_K_Cl_ZD17(T, P):

    # Convert dbar to MPa
    P_MPa = P / 100 # MPa

    # KCl T and P parameters from ZD17 Table 2
    b0 = ZD17_eq8(T, P_MPa, [ \
           0.0263285,
           0.0713524,
        -  0.008957 ,
        -  1.3320169,
        -  0.6454779,
        -  0.758977 ,
           9.4585163,
        -  0.0186077,
           0.211171 ,
           0        ,
          22.686075 ,
           0        ,
           0        ,
           0        ,
           0        ,
           0        ,
           0        ,
           0        ,
           0        ,
           0        ,
           0        ,
           0        ,
           0        ,
           0        ,
    ])

    b1 = ZD17_eq8(T, P_MPa, [ \
        -  0.1191678,
           0.7216226,
           0        ,
           8.5388026,
           4.3794936,
        - 11.743658 ,
        - 25.744757 ,
        -  0.1638556,
           3.444429 ,
           0        ,
           0.7549375,
        -  7.2651892,
           0        ,
           0        ,
           0        ,
           0        ,
           4.0457998,
           0        ,
           0        ,
        -162.81428  ,
         296.7078   ,
           0        ,
        -  0.7343191,
          46.340392 ,
    ])

    b2 = 0

    C0 = ZD17_eq8(T, P_MPa, [ \
        -  0.0005981,
           0.002905 ,
        -  0.0028921,
        -  0.1711606,
           0.0479309,
           0.141835 ,
           0        ,
           0.0009746,
           0.0084333,
           0        ,
          10.518644 ,
           0        ,
           1.1917209,
        -  9.3262105,
           0        ,
           0        ,
           0        ,
           0        ,
           0        ,
        -  5.4129002,
           0        ,
           0        ,
           0        ,
           0        ,
    ])

    C1 = ZD17_eq8(T, P_MPa, [ \
           0        ,
           1.0025605,
           0        ,
           0        ,
           3.0805818,
           0        ,
        - 86.99429  ,
        -  0.3005514,
           0        ,
        - 47.235583 ,
        -901.18412  ,
        -  2.326187 ,
           0        ,
        -504.46628  ,
           0        ,
           0        ,
        -  4.7090241,
           0        ,
           0        ,
         542.1083   ,
           0        ,
           0        ,
           1.6548655,
          59.165704 ,
    ])

    # Alpha and omega values
    alph1 = 2
    alph2 = -9
    omega = 2.5

    # Validity range
    valid = T <= 600

    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

# === ZEZIN & DRIESNER 2017 ===================================================
###############################################################################

#%%############################################################################
# === HARVIE, MOLLER AND WEARE 1984 ===========================================

# --- Auto-generated by HMW84_funcgen_bC.py -----------------------------------

def bC_Na_Cl_HMW84(T, P):
# Coefficients from HMW84 Table 1
    b0   = 0.0765
    b1   = 0.2644
    b2   = 0.0
    Cphi = 0.00127
    zNa = 1
    zCl = -1
    C0 = Cphi / (2 * sqrt(np_abs(zNa * zCl)))
    C1 = 0
    alph1 = 2
    alph2 = -9
    omega = -9
    valid = T == 298.15
    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

def bC_Na_SO4_HMW84(T, P):
# Coefficients from HMW84 Table 1
    b0   = 0.01958
    b1   = 1.113
    b2   = 0.0
    Cphi = 0.00497
    zNa = 1
    zSO4 = -2
    C0 = Cphi / (2 * sqrt(np_abs(zNa * zSO4)))
    C1 = 0
    alph1 = 2
    alph2 = -9
    omega = -9
    valid = T == 298.15
    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

def bC_Na_HSO4_HMW84(T, P):
# Coefficients from HMW84 Table 1
    b0   = 0.0454
    b1   = 0.398
    b2   = 0.0
    Cphi = 0.0
    zNa = 1
    zHSO4 = -1
    C0 = Cphi / (2 * sqrt(np_abs(zNa * zHSO4)))
    C1 = 0
    alph1 = 2
    alph2 = -9
    omega = -9
    valid = T == 298.15
    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

def bC_Na_OH_HMW84(T, P):
# Coefficients from HMW84 Table 1
    b0   = 0.0864
    b1   = 0.253
    b2   = 0.0
    Cphi = 0.0044
    zNa = 1
    zOH = -1
    C0 = Cphi / (2 * sqrt(np_abs(zNa * zOH)))
    C1 = 0
    alph1 = 2
    alph2 = -9
    omega = -9
    valid = T == 298.15
    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

def bC_Na_HCO3_HMW84(T, P):
# Coefficients from HMW84 Table 1
    b0   = 0.0277
    b1   = 0.0411
    b2   = 0.0
    Cphi = 0.0
    zNa = 1
    zHCO3 = -1
    C0 = Cphi / (2 * sqrt(np_abs(zNa * zHCO3)))
    C1 = 0
    alph1 = 2
    alph2 = -9
    omega = -9
    valid = T == 298.15
    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

def bC_Na_CO3_HMW84(T, P):
# Coefficients from HMW84 Table 1
    b0   = 0.0399
    b1   = 1.389
    b2   = 0.0
    Cphi = 0.0044
    zNa = 1
    zCO3 = -2
    C0 = Cphi / (2 * sqrt(np_abs(zNa * zCO3)))
    C1 = 0
    alph1 = 2
    alph2 = -9
    omega = -9
    valid = T == 298.15
    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

def bC_K_Cl_HMW84(T, P):
# Coefficients from HMW84 Table 1
    b0   = 0.04835
    b1   = 0.2122
    b2   = 0.0
    Cphi = -0.00084
    zK = 1
    zCl = -1
    C0 = Cphi / (2 * sqrt(np_abs(zK * zCl)))
    C1 = 0
    alph1 = 2
    alph2 = -9
    omega = -9
    valid = T == 298.15
    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

def bC_K_SO4_HMW84(T, P):
# Coefficients from HMW84 Table 1
    b0   = 0.04995
    b1   = 0.7793
    b2   = 0.0
    Cphi = 0.0
    zK = 1
    zSO4 = -2
    C0 = Cphi / (2 * sqrt(np_abs(zK * zSO4)))
    C1 = 0
    alph1 = 2
    alph2 = -9
    omega = -9
    valid = T == 298.15
    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

def bC_K_HSO4_HMW84(T, P):
# Coefficients from HMW84 Table 1
    b0   = -0.0003
    b1   = 0.1735
    b2   = 0.0
    Cphi = 0.0
    zK = 1
    zHSO4 = -1
    C0 = Cphi / (2 * sqrt(np_abs(zK * zHSO4)))
    C1 = 0
    alph1 = 2
    alph2 = -9
    omega = -9
    valid = T == 298.15
    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

def bC_K_OH_HMW84(T, P):
# Coefficients from HMW84 Table 1
    b0   = 0.1298
    b1   = 0.32
    b2   = 0.0
    Cphi = 0.0041
    zK = 1
    zOH = -1
    C0 = Cphi / (2 * sqrt(np_abs(zK * zOH)))
    C1 = 0
    alph1 = 2
    alph2 = -9
    omega = -9
    valid = T == 298.15
    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

def bC_K_HCO3_HMW84(T, P):
# Coefficients from HMW84 Table 1
    b0   = 0.0296
    b1   = -0.013
    b2   = 0.0
    Cphi = -0.008
    zK = 1
    zHCO3 = -1
    C0 = Cphi / (2 * sqrt(np_abs(zK * zHCO3)))
    C1 = 0
    alph1 = 2
    alph2 = -9
    omega = -9
    valid = T == 298.15
    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

def bC_K_CO3_HMW84(T, P):
# Coefficients from HMW84 Table 1
    b0   = 0.1488
    b1   = 1.43
    b2   = 0.0
    Cphi = -0.0015
    zK = 1
    zCO3 = -2
    C0 = Cphi / (2 * sqrt(np_abs(zK * zCO3)))
    C1 = 0
    alph1 = 2
    alph2 = -9
    omega = -9
    valid = T == 298.15
    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

def bC_Ca_Cl_HMW84(T, P):
# Coefficients from HMW84 Table 1
    b0   = 0.3159
    b1   = 1.614
    b2   = 0.0
    Cphi = -0.00034
    zCa = 2
    zCl = -1
    C0 = Cphi / (2 * sqrt(np_abs(zCa * zCl)))
    C1 = 0
    alph1 = 2
    alph2 = -9
    omega = -9
    valid = T == 298.15
    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

def bC_Ca_SO4_HMW84(T, P):
# Coefficients from HMW84 Table 1
    b0   = 0.2
    b1   = 3.1973
    b2   = -54.24
    Cphi = 0.0
    zCa = 2
    zSO4 = -2
    C0 = Cphi / (2 * sqrt(np_abs(zCa * zSO4)))
    C1 = 0
    alph1 = 1.4
    alph2 = 12
    omega = -9
    valid = T == 298.15
    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

def bC_Ca_HSO4_HMW84(T, P):
# Coefficients from HMW84 Table 1
    b0   = 0.2145
    b1   = 2.53
    b2   = 0.0
    Cphi = 0.0
    zCa = 2
    zHSO4 = -1
    C0 = Cphi / (2 * sqrt(np_abs(zCa * zHSO4)))
    C1 = 0
    alph1 = 2
    alph2 = -9
    omega = -9
    valid = T == 298.15
    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

def bC_Ca_OH_HMW84(T, P):
# Coefficients from HMW84 Table 1
    b0   = -0.1747
    b1   = -0.2303
    b2   = -5.72
    Cphi = 0.0
    zCa = 2
    zOH = -1
    C0 = Cphi / (2 * sqrt(np_abs(zCa * zOH)))
    C1 = 0
    alph1 = 2
    alph2 = 12
    omega = -9
    valid = T == 298.15
    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

def bC_Ca_HCO3_HMW84(T, P):
# Coefficients from HMW84 Table 1
    b0   = 0.4
    b1   = 2.977
    b2   = 0.0
    Cphi = 0.0
    zCa = 2
    zHCO3 = -1
    C0 = Cphi / (2 * sqrt(np_abs(zCa * zHCO3)))
    C1 = 0
    alph1 = 2
    alph2 = -9
    omega = -9
    valid = T == 298.15
    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

def bC_Ca_CO3_HMW84(T, P):
# Coefficients from HMW84 Table 1
    b0   = 0.0
    b1   = 0.0
    b2   = 0.0
    Cphi = 0.0
    zCa = 2
    zCO3 = -2
    C0 = Cphi / (2 * sqrt(np_abs(zCa * zCO3)))
    C1 = 0
    alph1 = 2
    alph2 = -9
    omega = -9
    valid = T == 298.15
    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

def bC_Mg_Cl_HMW84(T, P):
# Coefficients from HMW84 Table 1
    b0   = 0.35235
    b1   = 1.6815
    b2   = 0.0
    Cphi = 0.00519
    zMg = 2
    zCl = -1
    C0 = Cphi / (2 * sqrt(np_abs(zMg * zCl)))
    C1 = 0
    alph1 = 2
    alph2 = -9
    omega = -9
    valid = T == 298.15
    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

def bC_Mg_SO4_HMW84(T, P):
# Coefficients from HMW84 Table 1
    b0   = 0.221
    b1   = 3.343
    b2   = -37.23
    Cphi = 0.025
    zMg = 2
    zSO4 = -2
    C0 = Cphi / (2 * sqrt(np_abs(zMg * zSO4)))
    C1 = 0
    alph1 = 1.4
    alph2 = 12
    omega = -9
    valid = T == 298.15
    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

def bC_Mg_HSO4_HMW84(T, P):
# Coefficients from HMW84 Table 1
    b0   = 0.4746
    b1   = 1.729
    b2   = 0.0
    Cphi = 0.0
    zMg = 2
    zHSO4 = -1
    C0 = Cphi / (2 * sqrt(np_abs(zMg * zHSO4)))
    C1 = 0
    alph1 = 2
    alph2 = -9
    omega = -9
    valid = T == 298.15
    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

def bC_Mg_OH_HMW84(T, P):
# Coefficients from HMW84 Table 1
    b0   = 0.0
    b1   = 0.0
    b2   = 0.0
    Cphi = 0.0
    zMg = 2
    zOH = -1
    C0 = Cphi / (2 * sqrt(np_abs(zMg * zOH)))
    C1 = 0
    alph1 = 2
    alph2 = -9
    omega = -9
    valid = T == 298.15
    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

def bC_Mg_HCO3_HMW84(T, P):
# Coefficients from HMW84 Table 1
    b0   = 0.329
    b1   = 0.6072
    b2   = 0.0
    Cphi = 0.0
    zMg = 2
    zHCO3 = -1
    C0 = Cphi / (2 * sqrt(np_abs(zMg * zHCO3)))
    C1 = 0
    alph1 = 2
    alph2 = -9
    omega = -9
    valid = T == 298.15
    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

def bC_Mg_CO3_HMW84(T, P):
# Coefficients from HMW84 Table 1
    b0   = 0.0
    b1   = 0.0
    b2   = 0.0
    Cphi = 0.0
    zMg = 2
    zCO3 = -2
    C0 = Cphi / (2 * sqrt(np_abs(zMg * zCO3)))
    C1 = 0
    alph1 = 2
    alph2 = -9
    omega = -9
    valid = T == 298.15
    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

def bC_MgOH_Cl_HMW84(T, P):
# Coefficients from HMW84 Table 1
    b0   = -0.1
    b1   = 1.658
    b2   = 0.0
    Cphi = 0.0
    zMgOH = 1
    zCl = -1
    C0 = Cphi / (2 * sqrt(np_abs(zMgOH * zCl)))
    C1 = 0
    alph1 = 2
    alph2 = -9
    omega = -9
    valid = T == 298.15
    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

def bC_MgOH_SO4_HMW84(T, P):
# Coefficients from HMW84 Table 1
    b0   = 0.0
    b1   = 0.0
    b2   = 0.0
    Cphi = 0.0
    zMgOH = 1
    zSO4 = -2
    C0 = Cphi / (2 * sqrt(np_abs(zMgOH * zSO4)))
    C1 = 0
    alph1 = 2
    alph2 = -9
    omega = -9
    valid = T == 298.15
    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

def bC_MgOH_HSO4_HMW84(T, P):
# Coefficients from HMW84 Table 1
    b0   = 0.0
    b1   = 0.0
    b2   = 0.0
    Cphi = 0.0
    zMgOH = 1
    zHSO4 = -1
    C0 = Cphi / (2 * sqrt(np_abs(zMgOH * zHSO4)))
    C1 = 0
    alph1 = 2
    alph2 = -9
    omega = -9
    valid = T == 298.15
    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

def bC_MgOH_OH_HMW84(T, P):
# Coefficients from HMW84 Table 1
    b0   = 0.0
    b1   = 0.0
    b2   = 0.0
    Cphi = 0.0
    zMgOH = 1
    zOH = -1
    C0 = Cphi / (2 * sqrt(np_abs(zMgOH * zOH)))
    C1 = 0
    alph1 = 2
    alph2 = -9
    omega = -9
    valid = T == 298.15
    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

def bC_MgOH_HCO3_HMW84(T, P):
# Coefficients from HMW84 Table 1
    b0   = 0.0
    b1   = 0.0
    b2   = 0.0
    Cphi = 0.0
    zMgOH = 1
    zHCO3 = -1
    C0 = Cphi / (2 * sqrt(np_abs(zMgOH * zHCO3)))
    C1 = 0
    alph1 = 2
    alph2 = -9
    omega = -9
    valid = T == 298.15
    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

def bC_MgOH_CO3_HMW84(T, P):
# Coefficients from HMW84 Table 1
    b0   = 0.0
    b1   = 0.0
    b2   = 0.0
    Cphi = 0.0
    zMgOH = 1
    zCO3 = -2
    C0 = Cphi / (2 * sqrt(np_abs(zMgOH * zCO3)))
    C1 = 0
    alph1 = 2
    alph2 = -9
    omega = -9
    valid = T == 298.15
    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

def bC_H_Cl_HMW84(T, P):
# Coefficients from HMW84 Table 1
    b0   = 0.1775
    b1   = 0.2945
    b2   = 0.0
    Cphi = 0.0008
    zH = 1
    zCl = -1
    C0 = Cphi / (2 * sqrt(np_abs(zH * zCl)))
    C1 = 0
    alph1 = 2
    alph2 = -9
    omega = -9
    valid = T == 298.15
    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

def bC_H_SO4_HMW84(T, P):
# Coefficients from HMW84 Table 1
    b0   = 0.0298
    b1   = 0.0
    b2   = 0.0
    Cphi = 0.0438
    zH = 1
    zSO4 = -2
    C0 = Cphi / (2 * sqrt(np_abs(zH * zSO4)))
    C1 = 0
    alph1 = 2
    alph2 = -9
    omega = -9
    valid = T == 298.15
    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

def bC_H_HSO4_HMW84(T, P):
# Coefficients from HMW84 Table 1
    b0   = 0.2065
    b1   = 0.5556
    b2   = 0.0
    Cphi = 0.0
    zH = 1
    zHSO4 = -1
    C0 = Cphi / (2 * sqrt(np_abs(zH * zHSO4)))
    C1 = 0
    alph1 = 2
    alph2 = -9
    omega = -9
    valid = T == 298.15
    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

def bC_H_OH_HMW84(T, P):
# Coefficients from HMW84 Table 1
    b0   = 0.0
    b1   = 0.0
    b2   = 0.0
    Cphi = 0.0
    zH = 1
    zOH = -1
    C0 = Cphi / (2 * sqrt(np_abs(zH * zOH)))
    C1 = 0
    alph1 = 2
    alph2 = -9
    omega = -9
    valid = T == 298.15
    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

def bC_H_HCO3_HMW84(T, P):
# Coefficients from HMW84 Table 1
    b0   = 0.0
    b1   = 0.0
    b2   = 0.0
    Cphi = 0.0
    zH = 1
    zHCO3 = -1
    C0 = Cphi / (2 * sqrt(np_abs(zH * zHCO3)))
    C1 = 0
    alph1 = 2
    alph2 = -9
    omega = -9
    valid = T == 298.15
    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

def bC_H_CO3_HMW84(T, P):
# Coefficients from HMW84 Table 1
    b0   = 0.0
    b1   = 0.0
    b2   = 0.0
    Cphi = 0.0
    zH = 1
    zCO3 = -2
    C0 = Cphi / (2 * sqrt(np_abs(zH * zCO3)))
    C1 = 0
    alph1 = 2
    alph2 = -9
    omega = -9
    valid = T == 298.15
    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

# --- Auto-generated by HMW84_funcgen_cca.py ----------------------------------

def theta_K_Na_HMW84(T, P):
# Coefficients from HMW84 Table 2
    theta = -0.012
    valid = T == 298.15
    return theta, valid

def psi_K_Na_Cl_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = -0.0018
    valid = T == 298.15
    return psi, valid

def psi_K_Na_SO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = -0.01
    valid = T == 298.15
    return psi, valid

def psi_K_Na_HSO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_K_Na_OH_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0
    valid = T == 298.15
    return psi, valid

def psi_K_Na_HCO3_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = -0.003
    valid = T == 298.15
    return psi, valid

def psi_K_Na_CO3_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.003
    valid = T == 298.15
    return psi, valid

def theta_Ca_Na_HMW84(T, P):
# Coefficients from HMW84 Table 2
    theta = 0.07
    valid = T == 298.15
    return theta, valid

def psi_Ca_Na_Cl_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = -0.007
    valid = T == 298.15
    return psi, valid

def psi_Ca_Na_SO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = -0.055
    valid = T == 298.15
    return psi, valid

def psi_Ca_Na_HSO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_Ca_Na_OH_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0
    valid = T == 298.15
    return psi, valid

def psi_Ca_Na_HCO3_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_Ca_Na_CO3_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def theta_Mg_Na_HMW84(T, P):
# Coefficients from HMW84 Table 2
    theta = 0.07
    valid = T == 298.15
    return theta, valid

def psi_Mg_Na_Cl_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = -0.012
    valid = T == 298.15
    return psi, valid

def psi_Mg_Na_SO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = -0.015
    valid = T == 298.15
    return psi, valid

def psi_Mg_Na_HSO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_Mg_Na_OH_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0
    valid = T == 298.15
    return psi, valid

def psi_Mg_Na_HCO3_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_Mg_Na_CO3_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def theta_MgOH_Na_HMW84(T, P):
# Coefficients from HMW84 Table 2
    theta = 0.0
    valid = T == 298.15
    return theta, valid

def psi_MgOH_Na_Cl_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_MgOH_Na_SO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_MgOH_Na_HSO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_MgOH_Na_OH_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0
    valid = T == 298.15
    return psi, valid

def psi_MgOH_Na_HCO3_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_MgOH_Na_CO3_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def theta_H_Na_HMW84(T, P):
# Coefficients from HMW84 Table 2
    theta = 0.036
    valid = T == 298.15
    return theta, valid

def psi_H_Na_Cl_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = -0.004
    valid = T == 298.15
    return psi, valid

def psi_H_Na_SO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_H_Na_HSO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = -0.0129
    valid = T == 298.15
    return psi, valid

def psi_H_Na_OH_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0
    valid = T == 298.15
    return psi, valid

def psi_H_Na_HCO3_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_H_Na_CO3_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def theta_Ca_K_HMW84(T, P):
# Coefficients from HMW84 Table 2
    theta = 0.032
    valid = T == 298.15
    return theta, valid

def psi_Ca_K_Cl_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = -0.025
    valid = T == 298.15
    return psi, valid

def psi_Ca_K_SO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_Ca_K_HSO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_Ca_K_OH_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0
    valid = T == 298.15
    return psi, valid

def psi_Ca_K_HCO3_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_Ca_K_CO3_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def theta_K_Mg_HMW84(T, P):
# Coefficients from HMW84 Table 2
    theta = 0.0
    valid = T == 298.15
    return theta, valid

def psi_K_Mg_Cl_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = -0.022
    valid = T == 298.15
    return psi, valid

def psi_K_Mg_SO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = -0.048
    valid = T == 298.15
    return psi, valid

def psi_K_Mg_HSO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_K_Mg_OH_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0
    valid = T == 298.15
    return psi, valid

def psi_K_Mg_HCO3_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_K_Mg_CO3_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def theta_K_MgOH_HMW84(T, P):
# Coefficients from HMW84 Table 2
    theta = 0.0
    valid = T == 298.15
    return theta, valid

def psi_K_MgOH_Cl_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_K_MgOH_SO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_K_MgOH_HSO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_K_MgOH_OH_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0
    valid = T == 298.15
    return psi, valid

def psi_K_MgOH_HCO3_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_K_MgOH_CO3_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def theta_H_K_HMW84(T, P):
# Coefficients from HMW84 Table 2
    theta = 0.005
    valid = T == 298.15
    return theta, valid

def psi_H_K_Cl_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = -0.011
    valid = T == 298.15
    return psi, valid

def psi_H_K_SO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.197
    valid = T == 298.15
    return psi, valid

def psi_H_K_HSO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = -0.0265
    valid = T == 298.15
    return psi, valid

def psi_H_K_OH_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0
    valid = T == 298.15
    return psi, valid

def psi_H_K_HCO3_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_H_K_CO3_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def theta_Ca_Mg_HMW84(T, P):
# Coefficients from HMW84 Table 2
    theta = 0.007
    valid = T == 298.15
    return theta, valid

def psi_Ca_Mg_Cl_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = -0.012
    valid = T == 298.15
    return psi, valid

def psi_Ca_Mg_SO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.024
    valid = T == 298.15
    return psi, valid

def psi_Ca_Mg_HSO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_Ca_Mg_OH_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0
    valid = T == 298.15
    return psi, valid

def psi_Ca_Mg_HCO3_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_Ca_Mg_CO3_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def theta_Ca_MgOH_HMW84(T, P):
# Coefficients from HMW84 Table 2
    theta = 0.0
    valid = T == 298.15
    return theta, valid

def psi_Ca_MgOH_Cl_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_Ca_MgOH_SO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_Ca_MgOH_HSO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_Ca_MgOH_OH_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0
    valid = T == 298.15
    return psi, valid

def psi_Ca_MgOH_HCO3_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_Ca_MgOH_CO3_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def theta_Ca_H_HMW84(T, P):
# Coefficients from HMW84 Table 2
    theta = 0.092
    valid = T == 298.15
    return theta, valid

def psi_Ca_H_Cl_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = -0.015
    valid = T == 298.15
    return psi, valid

def psi_Ca_H_SO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_Ca_H_HSO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_Ca_H_OH_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0
    valid = T == 298.15
    return psi, valid

def psi_Ca_H_HCO3_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_Ca_H_CO3_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def theta_Mg_MgOH_HMW84(T, P):
# Coefficients from HMW84 Table 2
    theta = 0.0
    valid = T == 298.15
    return theta, valid

def psi_Mg_MgOH_Cl_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.028
    valid = T == 298.15
    return psi, valid

def psi_Mg_MgOH_SO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_Mg_MgOH_HSO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_Mg_MgOH_OH_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0
    valid = T == 298.15
    return psi, valid

def psi_Mg_MgOH_HCO3_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_Mg_MgOH_CO3_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def theta_H_Mg_HMW84(T, P):
# Coefficients from HMW84 Table 2
    theta = 0.1
    valid = T == 298.15
    return theta, valid

def psi_H_Mg_Cl_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = -0.011
    valid = T == 298.15
    return psi, valid

def psi_H_Mg_SO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_H_Mg_HSO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = -0.0178
    valid = T == 298.15
    return psi, valid

def psi_H_Mg_OH_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0
    valid = T == 298.15
    return psi, valid

def psi_H_Mg_HCO3_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_H_Mg_CO3_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def theta_H_MgOH_HMW84(T, P):
# Coefficients from HMW84 Table 2
    theta = 0.0
    valid = T == 298.15
    return theta, valid

def psi_H_MgOH_Cl_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_H_MgOH_SO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_H_MgOH_HSO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_H_MgOH_OH_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0
    valid = T == 298.15
    return psi, valid

def psi_H_MgOH_HCO3_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_H_MgOH_CO3_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

# --- Auto-generated by HMW84_funcgen_caa.py ----------------------------------

def theta_Cl_SO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    theta = 0.02
    valid = T == 298.15
    return theta, valid

def psi_Na_Cl_SO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0014
    valid = T == 298.15
    return psi, valid

def psi_K_Cl_SO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_Ca_Cl_SO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = -0.018
    valid = T == 298.15
    return psi, valid

def psi_Mg_Cl_SO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = -0.004
    valid = T == 298.15
    return psi, valid

def psi_MgOH_Cl_SO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0
    valid = T == 298.15
    return psi, valid

def psi_H_Cl_SO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def theta_Cl_HSO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    theta = -0.006
    valid = T == 298.15
    return theta, valid

def psi_Na_Cl_HSO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = -0.006
    valid = T == 298.15
    return psi, valid

def psi_K_Cl_HSO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_Ca_Cl_HSO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_Mg_Cl_HSO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_MgOH_Cl_HSO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0
    valid = T == 298.15
    return psi, valid

def psi_H_Cl_HSO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.013
    valid = T == 298.15
    return psi, valid

def theta_Cl_OH_HMW84(T, P):
# Coefficients from HMW84 Table 2
    theta = -0.05
    valid = T == 298.15
    return theta, valid

def psi_Na_Cl_OH_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = -0.006
    valid = T == 298.15
    return psi, valid

def psi_K_Cl_OH_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = -0.006
    valid = T == 298.15
    return psi, valid

def psi_Ca_Cl_OH_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = -0.025
    valid = T == 298.15
    return psi, valid

def psi_Mg_Cl_OH_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_MgOH_Cl_OH_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0
    valid = T == 298.15
    return psi, valid

def psi_H_Cl_OH_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def theta_Cl_HCO3_HMW84(T, P):
# Coefficients from HMW84 Table 2
    theta = 0.03
    valid = T == 298.15
    return theta, valid

def psi_Na_Cl_HCO3_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = -0.15
    valid = T == 298.15
    return psi, valid

def psi_K_Cl_HCO3_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_Ca_Cl_HCO3_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_Mg_Cl_HCO3_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = -0.096
    valid = T == 298.15
    return psi, valid

def psi_MgOH_Cl_HCO3_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0
    valid = T == 298.15
    return psi, valid

def psi_H_Cl_HCO3_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def theta_CO3_Cl_HMW84(T, P):
# Coefficients from HMW84 Table 2
    theta = -0.02
    valid = T == 298.15
    return theta, valid

def psi_Na_CO3_Cl_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0085
    valid = T == 298.15
    return psi, valid

def psi_K_CO3_Cl_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.004
    valid = T == 298.15
    return psi, valid

def psi_Ca_CO3_Cl_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_Mg_CO3_Cl_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_MgOH_CO3_Cl_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0
    valid = T == 298.15
    return psi, valid

def psi_H_CO3_Cl_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def theta_HSO4_SO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    theta = 0.0
    valid = T == 298.15
    return theta, valid

def psi_Na_HSO4_SO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = -0.0094
    valid = T == 298.15
    return psi, valid

def psi_K_HSO4_SO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = -0.0677
    valid = T == 298.15
    return psi, valid

def psi_Ca_HSO4_SO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_Mg_HSO4_SO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = -0.0425
    valid = T == 298.15
    return psi, valid

def psi_MgOH_HSO4_SO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0
    valid = T == 298.15
    return psi, valid

def psi_H_HSO4_SO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def theta_OH_SO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    theta = -0.013
    valid = T == 298.15
    return theta, valid

def psi_Na_OH_SO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = -0.009
    valid = T == 298.15
    return psi, valid

def psi_K_OH_SO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = -0.05
    valid = T == 298.15
    return psi, valid

def psi_Ca_OH_SO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_Mg_OH_SO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_MgOH_OH_SO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0
    valid = T == 298.15
    return psi, valid

def psi_H_OH_SO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def theta_HCO3_SO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    theta = 0.01
    valid = T == 298.15
    return theta, valid

def psi_Na_HCO3_SO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = -0.005
    valid = T == 298.15
    return psi, valid

def psi_K_HCO3_SO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_Ca_HCO3_SO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_Mg_HCO3_SO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = -0.161
    valid = T == 298.15
    return psi, valid

def psi_MgOH_HCO3_SO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0
    valid = T == 298.15
    return psi, valid

def psi_H_HCO3_SO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def theta_CO3_SO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    theta = 0.02
    valid = T == 298.15
    return theta, valid

def psi_Na_CO3_SO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = -0.005
    valid = T == 298.15
    return psi, valid

def psi_K_CO3_SO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = -0.009
    valid = T == 298.15
    return psi, valid

def psi_Ca_CO3_SO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_Mg_CO3_SO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_MgOH_CO3_SO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0
    valid = T == 298.15
    return psi, valid

def psi_H_CO3_SO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def theta_HSO4_OH_HMW84(T, P):
# Coefficients from HMW84 Table 2
    theta = 0.0
    valid = T == 298.15
    return theta, valid

def psi_Na_HSO4_OH_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_K_HSO4_OH_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_Ca_HSO4_OH_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_Mg_HSO4_OH_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_MgOH_HSO4_OH_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0
    valid = T == 298.15
    return psi, valid

def psi_H_HSO4_OH_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def theta_HCO3_HSO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    theta = 0.0
    valid = T == 298.15
    return theta, valid

def psi_Na_HCO3_HSO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_K_HCO3_HSO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_Ca_HCO3_HSO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_Mg_HCO3_HSO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_MgOH_HCO3_HSO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0
    valid = T == 298.15
    return psi, valid

def psi_H_HCO3_HSO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def theta_CO3_HSO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    theta = 0.0
    valid = T == 298.15
    return theta, valid

def psi_Na_CO3_HSO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_K_CO3_HSO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_Ca_CO3_HSO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_Mg_CO3_HSO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_MgOH_CO3_HSO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0
    valid = T == 298.15
    return psi, valid

def psi_H_CO3_HSO4_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def theta_HCO3_OH_HMW84(T, P):
# Coefficients from HMW84 Table 2
    theta = 0.0
    valid = T == 298.15
    return theta, valid

def psi_Na_HCO3_OH_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_K_HCO3_OH_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_Ca_HCO3_OH_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_Mg_HCO3_OH_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_MgOH_HCO3_OH_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0
    valid = T == 298.15
    return psi, valid

def psi_H_HCO3_OH_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def theta_CO3_OH_HMW84(T, P):
# Coefficients from HMW84 Table 2
    theta = 0.1
    valid = T == 298.15
    return theta, valid

def psi_Na_CO3_OH_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = -0.017
    valid = T == 298.15
    return psi, valid

def psi_K_CO3_OH_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = -0.01
    valid = T == 298.15
    return psi, valid

def psi_Ca_CO3_OH_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_Mg_CO3_OH_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_MgOH_CO3_OH_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0
    valid = T == 298.15
    return psi, valid

def psi_H_CO3_OH_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def theta_CO3_HCO3_HMW84(T, P):
# Coefficients from HMW84 Table 2
    theta = -0.04
    valid = T == 298.15
    return theta, valid

def psi_Na_CO3_HCO3_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.002
    valid = T == 298.15
    return psi, valid

def psi_K_CO3_HCO3_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.012
    valid = T == 298.15
    return psi, valid

def psi_Ca_CO3_HCO3_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_Mg_CO3_HCO3_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

def psi_MgOH_CO3_HCO3_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0
    valid = T == 298.15
    return psi, valid

def psi_H_CO3_HCO3_HMW84(T, P):
# Coefficients from HMW84 Table 2
    psi = 0.0
    valid = T == 298.15
    return psi, valid

# === HARVIE, MOLLER AND WEARE 1984 ===========================================
###############################################################################

#%%############################################################################
# === MILLERO & PIERROT 1998 ==================================================

def MP98_eq15(T,q):

    # q[0] = PR
    # q[1] = PJ  * 1e5
    # q[2] = PRL * 1e4

    Tr = 298.15

    return q[0] + q[1]*1e-5 * (Tr**3/3 - Tr**2 * q[2]*1e-4) * (1/T - 1/Tr) \
        + q[1]*1e-5 * (T**2 - Tr**2) / 6

# --- bC: sodium iodide -------------------------------------------------------

def bC_Na_I_MP98(T, P):

    b0    = MP98_eq15(T,float_([ 0.1195,
                                -1.01  ,
                                 8.355 ]))

    b1    = MP98_eq15(T,float_([ 0.3439,
                                -2.54  ,
                                 8.28  ]))

    b2 = 0

    Cphi  = MP98_eq15(T,float_([ 0.0018,
                                 0     ,
                                -0.835 ]))

    zNa   = +1
    zI    = -1
    C0    = Cphi / (2 * sqrt(np_abs(zNa * zI)))

    C1 = 0

    alph1 = 2
    alph2 = -9
    omega = -9

    valid = logical_and(T >= 273.15, T <= 323.15)

    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

# --- bC: sodium bromide ------------------------------------------------------

def bC_Na_Br_MP98(T, P):

    b0    = MP98_eq15(T,float_([  0.0973 ,
                                - 1.3    ,
                                  7.692  ]))

    b1    = MP98_eq15(T,float_([  0.2791 ,
                                - 1.06   ,
                                 10.79   ]))

    b2 = 0

    Cphi  = MP98_eq15(T,float_([  0.00116,
                                  0.16405,
                                - 0.93   ]))

    zNa   = +1
    zBr   = -1
    C0    = Cphi / (2 * sqrt(np_abs(zNa * zBr)))

    C1 = 0

    alph1 = 2
    alph2 = -9
    omega = -9

    valid = logical_and(T >= 273.15, T <= 323.15)

    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

# --- bC: sodium fluoride -----------------------------------------------------

def bC_Na_F_MP98(T, P):

    b0    = MP98_eq15(T,float_([  0.215   ,
                                - 2.37    ,
                                  5.361e-4]))

    b1    = MP98_eq15(T,float_([  0.2107  ,
                                  0       ,
                                  8.7e-4  ]))

    b2 = 0
    C0 = 0
    C1 = 0

    alph1 = 2
    alph2 = -9
    omega = -9

    valid = logical_and(T >= 273.15, T <= 323.15)

    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

# --- bC: potassium bromide ---------------------------------------------------

def bC_K_Br_MP98(T, P):

    b0    = MP98_eq15(T,float_([  0.0569 ,
                                - 1.43   ,
                                  7.39   ]))

    b1    = MP98_eq15(T,float_([  0.2122 ,
                                - 0.762  ,
                                  1.74   ]))

    b2 = 0

    Cphi  = MP98_eq15(T,float_([- 0.0018 ,
                                  0.216  ,
                                - 0.7004 ]))

    zK    = +1
    zBr   = -1
    C0    = Cphi / (2 * sqrt(np_abs(zK * zBr)))

    C1 = 0

    alph1 = 2
    alph2 = -9
    omega = -9

    valid = logical_and(T >= 273.15, T <= 323.15)

    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

# --- bC: potassium fluoride --------------------------------------------------

def bC_K_F_MP98(T, P):

    b0    = MP98_eq15(T,float_([  0.08089,
                                - 1.39   ,
                                  2.14   ]))

    b1    = MP98_eq15(T,float_([  0.2021 ,
                                  0      ,
                                  5.44   ]))

    b2 = 0

    Cphi  = MP98_eq15(T,float_([  0.00093,
                                  0      ,
                                  0.595  ]))

    zK    = +1
    zF    = -1
    C0    = Cphi / (2 * sqrt(np_abs(zK * zF)))

    C1 = 0

    alph1 = 2
    alph2 = -9
    omega = -9

    valid = logical_and(T >= 273.15, T <= 323.15)

    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

# --- bC: potassium hydroxide -------------------------------------------------

def bC_K_OH_MP98(T, P):

    b0    = MP98_eq15(T,float_([  0.1298 ,
                                - 0.946  ,
                                  9.914  ])) # copy of KI

    b1    = MP98_eq15(T,float_([  0.32   ,
                                - 2.59   ,
                                 11.86   ])) # copy of KI

    b2 = 0

    Cphi  = MP98_eq15(T,float_([- 0.0041 ,
                                  0.0638 ,
                                - 0.944  ])) # copy of KI

    zK    = +1
    zOH   = -1
    C0    = Cphi / (2 * sqrt(np_abs(zK * zOH)))

    C1 = 0

    alph1 = 2
    alph2 = -9
    omega = -9

    valid = logical_and(T >= 273.15, T <= 323.15)

    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

# --- bC: potassium iodide ----------------------------------------------------

def bC_K_I_MP98(T, P):

    b0    = MP98_eq15(T,float_([  0.0746 ,
                                - 0.748  ,
                                  9.914  ]))

    b1    = MP98_eq15(T,float_([  0.2517 ,
                                - 1.8    ,
                                 11.86   ]))

    b2 = 0

    Cphi  = MP98_eq15(T,float_([- 0.00414,
                                  0      ,
                                - 0.944  ]))

    zK    = +1
    zI    = -1
    C0    = Cphi / (2 * sqrt(np_abs(zK * zI)))

    C1 = 0

    alph1 = 2
    alph2 = -9
    omega = -9

    valid = logical_and(T >= 273.15, T <= 323.15)

    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

#~~~~ Table A3 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def MP98_eqTableA3(T,abc):
    Tr = 298.15
    return abc[0] + abc[1] * (T - Tr) + abc[2] * (T - Tr)**2

# --- bC: sodium bisulfate ----------------------------------------------------
#
# MP98 cite Pierrot et al. (1997) J Solution Chem 26(1),
#   but their equations look quite different, and there is no Cphi there.
# This equation is therefore directly from MP98.

def bC_Na_HSO4_MP98(T, P):

    b0 = MP98_eqTableA3(T,float_([ 0.544    ,
                                  -1.8478e-3,
                                   5.3937e-5]))

    b1 = MP98_eqTableA3(T,float_([ 0.3826401,
                                  -1.8431e-2,
                                   0        ]))

    b2 = 0

    Cphi = 0.003905

    zNa   = +1
    zHSO4 = -1

    C0 = Cphi / (2 * sqrt(np_abs(zNa * zHSO4)))
    C1 = 0

    alph1 = 2
    alph2 = -9
    omega = -9

    valid = logical_and(T >= 273.15, T <= 323.15)

    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid


#~~~~ Copies ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# This section contains assignments that MP98 gave for unknown coefficients.
#
# They must be assigned in this format (using def) for CoefficientDictionary
#   methods like get_contents() to work properly.

def bC_Ca_SO3_MP98(T, P): return bC_Ca_SO4_M88(T, P)
def bC_Sr_SO4_MP98(T, P): return bC_Ca_SO4_M88(T, P)
def bC_Sr_BOH4_MP98(T, P): return bC_Ca_BOH4_SRM87(T, P)

# === MILLERO & PIERROT 1998 ==================================================
###############################################################################

#%%############################################################################
# === PITZER & MARGOYA 1973 ===================================================
#
# Experimental function - not production-ready

def bC_PM73(T, iset):

    zM, zX = props.charges(array(iset.split('-')))[0]

    PM73_Tables = {-1: PM73_TableI   ,
                   -2: PM73_TableVI  ,
                   -3: PM73_TableVIII,
                   -4: PM73_TableIX  ,
                   -5: PM73_TableIX  }

    b0 = full_like(T,PM73_Tables[zM*zX][iset]['b0'])
    b1 = full_like(T,PM73_Tables[zM*zX][iset]['b1'])
    b2 = 0

    Cphi = full_like(T,PM73_Tables[zM*zX][iset]['Cphi'])
    C0 = Cphi / (2 * sqrt(np_abs(zM * zX)))
    C1 = 0

    alph1 = 2
    alph2 = -9
    omega = -9

    valid = T == 298.15

    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

# --- bC: strontium bromide ---------------------------------------------------

def bC_Sr_Br_PM73(T, P):

    # PM73 cite Robinson & Stokes (1965) Electrolyte Solutions, 2nd Ed.

    b0 = full_like(T,0.4415 * 3/4)
    b1 = full_like(T,2.282  * 3/4)
    b2 = 0

    Cphi = full_like(T,0.00231 * 3/2**2.5)
    zSr = +2
    zBr = -1

    C0 = Cphi / (2 * sqrt(np_abs(zSr * zBr)))
    C1 = 0

    alph1 = 2
    alph2 = -9
    omega = -9

    valid = T == 298.15

    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

# --- bC: strontium chloride --------------------------------------------------

def bC_Sr_Cl_PM73(T, P):

    # PM73 cite Robinson & Stokes (1965) Electrolyte Solutions, 2nd Ed.

    b0 = full_like(T,0.3810 * 3/4)
    b1 = full_like(T,2.223  * 3/4)
    b2 = 0

    Cphi = full_like(T,-0.00246 * 3/2**2.5)
    zSr = +2
    zCl = -1

    C0 = Cphi / (2 * sqrt(np_abs(zSr * zCl)))
    C1 = 0

    alph1 = 2
    alph2 = -9
    omega = -9

    valid = T == 298.15

    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

# --- bC: potassium dihydrogen-phosphate --------------------------------------

def bC_K_H2PO4_PM73(T, P):

    b0 = -0.0678
    b1 = -0.1042
    b2 = 0
    C0 = 0
    C1 = 0

    alph1 = 2
    alph2 = -9
    omega = -9

    valid = T == 298.15

    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

# --- bC: potassium thiocyanate -----------------------------------------------

def bC_K_SCN_PM73(T, P):

    b0 = 0.0416
    b1 = 0.2302
    b2 = 0

    Cphi = -0.00252
    zK   = +1
    zSCN = -1

    C0 = Cphi / (2 * sqrt(np_abs(zK * zSCN)))
    C1 = 0

    alph1 = 2
    alph2 = -9
    omega = -9

    valid = T == 298.15

    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

# === PITZER & MARGOYA 1973 ===================================================
###############################################################################

###############################################################################
# === SILVESTER & PITZER 1978 =================================================

# General procedure:
#  - Inherit 298.15 K value from PM73;
#  - Add temperature derivative correction from SP78.

SP78_Tr = 298.15

# --- bC: strontium bromide ---------------------------------------------------

def bC_Sr_Br_SP78(T, P):

    # SP78 cite Lange & Streeck (1930) Z Phys Chem Abt A 152

    b0r,b1r,b2,C0,C1, alph1,alph2,omega, _ = bC_Sr_Br_PM73(T, P)

    b0 = b0r + float_(-0.437 * 1e-3 * 3/4) * (T - SP78_Tr)
    b1 = b1r + float_( 8.71  * 1e-3 * 3/4) * (T - SP78_Tr)

    # Validity range declared by MP98
    valid = logical_and(T >= 283.15,T <= 313.15)

    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

# --- bC: strontium chloride --------------------------------------------------

def bC_Sr_Cl_SP78(T, P):

    # SP78 cite Lange & Streeck (1930) Z Phys Chem Abt A 152

    b0r,b1r,b2,C0,C1, alph1,alph2,omega, _ = bC_Sr_Br_PM73(T, P)

    b0 = b0r + float_(0.956 * 1e-3 * 3/4) * (T - SP78_Tr)
    b1 = b1r + float_(3.79  * 1e-3 * 3/4) * (T - SP78_Tr)

    # Validity range declared by MP98
    valid = logical_and(T >= 283.15,T <= 313.15)

    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

# --- bC: potassium dihydrogen-phosphate --------------------------------------

def bC_K_H2PO4_SP78(T, P):

    b0r,b1r,b2,C0r,C1, alph1,alph2,omega, _ = bC_K_H2PO4_PM73(T, P)

    b0 = b0r + float_( 6.045 * 1e-4) * (T - SP78_Tr)
    b1 = b1r + float_(28.6   * 1e-4) * (T - SP78_Tr)

    zK     = +1
    zH2PO4 = -1

    Cphi = C0r * (2 * sqrt(np_abs(zK * zH2PO4))) \
           + float_(-10.11 * 1e-5) * (T - SP78_Tr)

    C0 = Cphi / (2 * sqrt(np_abs(zK * zH2PO4)))

    alph1 = 2
    alph2 = -9
    omega = -9

    # Validity range declared by MP98
    valid = logical_and(T >= 283.15,T <= 313.15)

    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

# --- bC: potassium thiocyanate -----------------------------------------------

def bC_K_SCN_SP78(T, P):

    b0r,b1r,b2,C0r,C1, alph1,alph2,omega, _ = bC_K_SCN_PM73(T, P)

    b0 = b0r + float_( 6.87 * 1e-4) * (T - SP78_Tr)
    b1 = b1r + float_(37    * 1e-4) * (T - SP78_Tr)

    zK   = +1
    zSCN = -1

    Cphi = C0r * (2 * sqrt(np_abs(zK * zSCN))) \
           + float_(0.43 * 1e-5) * (T - SP78_Tr)

    C0 = Cphi / (2 * sqrt(np_abs(zK * zSCN)))

    alph1 = 2
    alph2 = -9
    omega = -9

    # Validity range declared by MP98
    valid = logical_and(T >= 283.15,T <= 313.15)

    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

# === SILVESTER & PITZER 1978 =================================================
###############################################################################

#%%############################################################################
# === PEIPER & PITZER 1982 ====================================================

# The equation below was derived by MP Humphreys.

def PP82_eqMPH(T,q):

    Tr = 298.15

    return q[0] + q[1] * (T - Tr) + q[2] * (T - Tr)**2 / 2

# --- bC: sodium carbonate ----------------------------------------------------

def bC_Na_CO3_PP82(T, P):

    # I have no idea where MP98 got their T**2 coefficients from
    #   or why they are so small.
    b0 = PP82_eqMPH(T,float_([
          0.0362 ,
          1.79e-3,
        - 4.22e-5]))

    b1 = PP82_eqMPH(T,float_([
          1.51   ,
          2.05e-3,
        -16.8e-5 ]))

    b2 = 0

    Cphi = 0.0052
    zNa  = +1
    zCO3 = -2

    C0 = Cphi / (2 * sqrt(np_abs(zNa * zCO3)))
    C1 = 0

    alph1 = 2
    alph2 = -9
    omega = -9

    valid = logical_and(T >= 273.15, T <= 323.15)

    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

# --- bC: sodium bicarbonate --------------------------------------------------

def bC_Na_HCO3_PP82(T, P):

    # I have no idea where MP98 got their T**2 coefficients from
    #   or why they are so small.
    b0 = PP82_eqMPH(T,float_([
         0.028  ,
         1.00e-3,
        -2.6e-5 ]))

    b1 = PP82_eqMPH(T,float_([
         0.044  ,
         1.10e-3,
        -4.3e-5 ]))

    b2 = 0

    C0 = 0
    C1 = 0

    alph1 = 2
    alph2 = -9
    omega = -9

    valid = logical_and(T >= 273.15, T <= 323.15)

    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

# --- theta: chloride bicarbonate ---------------------------------------------

def theta_Cl_HCO3_PP82(T, P):

    theta = 0.0359
    valid = T == 298.15

    return theta, valid

# --- theta: chloride carbonate -----------------------------------------------

def theta_Cl_CO3_PP82(T, P):

    theta = -0.053
    valid = T == 298.15

    return theta, valid

# --- psi: sodium chloride bicarbonate ----------------------------------------

def psi_Na_Cl_HCO3_PP82(T, P):

    psi = -0.0143
    valid = T == 298.15

    return psi, valid

# === PEIPER & PITZER 1982 ====================================================
###############################################################################

#%%############################################################################
# === ROY ET AL 1983 ==========================================================

def bC_K_HCO3_RGW83(T, P):

    b0 = -0.022
    b1 = full_like(T, 0.09 )
    b2 = 0
    C0 = 0
    C1 = 0

    alph1 = 2
    alph2 = -9
    omega = -9

    valid = T == 298.15

    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

# === ROY ET AL 1983 ==========================================================
###############################################################################

#%%############################################################################
# === HERSHEY ET AL 1988 ======================================================

# --- bC: sodium bisulfide ----------------------------------------------------

def bC_Na_HS_HPM88(T, P):

    b0 = 3.66e-1 - 6.75e+1 / T
    b1 = 0
    b2 = 0

    Cphi = full_like(T,-1.27e-2)

    zNa = +1
    zHS = -1
    C0 = Cphi / (2 * sqrt(np_abs(zNa * zHS)))

    C1 = 0

    alph1 = -9
    alph2 = -9
    omega = -9

    valid = logical_and(T >= 278.15,T <= 318.15)

    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

# --- bC: potassium bisulfide -------------------------------------------------

def bC_K_HS_HPM88(T, P):

    b0 = 6.37e-1 - 1.40e+2 / T
    b1 = 0
    b2 = 0

    Cphi = full_like(T,-1.94e-1)

    zK  = +1
    zHS = -1
    C0 = Cphi / (2 * sqrt(np_abs(zK * zHS)))

    C1 = 0

    alph1 = -9
    alph2 = -9
    omega = -9

    valid = logical_and(T >= 278.15,T <= 298.15)

    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

# --- bC: magnesium bisulfide -------------------------------------------------

def bC_Mg_HS_HPM88(T, P):

    b0 = full_like(T,1.70e-1)
    b1 = full_like(T,2.78   )
    b2 = 0

    C0 = 0
    C1 = 0

    alph1 = 2
    alph2 = -9
    omega = -9

    valid = T == 298.15

    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

# --- bC: calcium bisulfide ---------------------------------------------------

def bC_Ca_HS_HPM88(T, P):

    b0 = full_like(T,-1.05e-1)
    b1 = full_like(T, 3.43   )
    b2 = 0

    C0 = 0
    C1 = 0

    alph1 = 2
    alph2 = -9
    omega = -9

    valid = T == 298.15

    return b0, b1, b2, C0, C1, alph1, alph2, omega, valid

###############################################################################
# === HERSHEY ET AL 1988 ======================================================

#%%############################################################################
# === MARCHEMSPEC SPECIALS ====================================================
#
# --- theta: hydrogen sodium --------------------------------------------------

def theta_H_Na_MarChemSpec25(T, P):

    theta = 0.036
    valid = T == 298.15

    return theta, valid

# --- theta: hydrogen potassium -----------------------------------------------

def theta_H_K_MarChemSpec25(T, P):

    theta = 0.005
    valid = T == 298.15

    return theta, valid

# --- lambd: tris tris --------------------------------------------------------
#
# Temporary value from "MODEL PARAMETERS FOR TRIS Tests.docx" (2019-01-31)

def lambd_tris_tris_MarChemSpec25(T, P):

    lambd = -0.006392
    valid = T == 298.15

    return lambd, valid

# --- eta: tris sodium chloride -----------------------------------------------
#
# Temporary value from "MODEL PARAMETERS FOR TRIS Tests.docx" (2019-01-31)

def zeta_tris_Na_Cl_MarChemSpec25(T, P):

    zeta  = -0.003231
    valid = T == 298.15

    return zeta, valid

# --- mu: tris tris tris ------------------------------------------------------
#
# Temporary value from "MODEL PARAMETERS FOR TRIS Tests.docx" (2019-01-31)

def mu_tris_tris_tris_MarChemSpec25(T, P):

    mu    = 0.0009529
    valid = T == 298.15

    return mu, valid

# === MARCHEMSPEC SPECIALS ====================================================
###############################################################################
