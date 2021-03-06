import numpy as np
import scipy.constants as const

a_b = 5. * const.angstrom  # barrier width
V_b = 0.25 * const.eV  # barrier height V_b
m_e = const.m_e  # electron mass
hbar = const.hbar  # planck's reduced constant

kb_a = np.sqrt(2. * m_e * V_b) * a_b / hbar  # barrier strength
m = kb_a ** 2  # mass

E = 0.9  # E_0/V_0
p0 = np.sqrt(m * E)  # momentum
sigma_p = p0 / 10  # momentum width
sigma_x = 1. / sigma_p  # position width
x0 = -1 - 5 * sigma_x  # initial position

# discrete spatial coords (-2*x_0,-2*x_0+dx,...,2*x_0)
x_max = -2. * x0
n_x = 1000
x_j, dx = np.linspace(-x_max, x_max, n_x, retstep=True)

K = 1. / (np.pi * sigma_x) ** 0.25


def psi_0(x):
    """
    Initial wave packet psi(x,0) with average momentum p_0.
    :param x: spatial coords
    :return: initial wave packet
    """
    psi = np.zeros(x.size, complex)
    for i in range(x.size):
        psi[i] = K * np.exp(-(x[i] - x0) ** 2 / (sigma_x ** 2)) * np.exp(1j * p0 * (x[i] - x0))
    return psi


def psi_t(t, p):
    """
    Time dependent solution of schrodinger equation psi(t).
    :param t: time coord
    :param p: momentum
    :return: time dependent solution
    """
    return np.exp(-1j * (p ** 2 / m) * t)


def V(x):
    """
    Time independent potential V(x).
    :param x: spatial coord
    :return: potential
    """
    return np.heaviside(1. - np.abs(x), 1.)


def t_0(p=p0):
    """
    Collision time t_col with barrier for classical particle.
    :param p: momentum
    :return: collision time
    """
    return -x0 / (p / m)


def prob(psi2, x_start=-x_max, x_end=x_max):
    """
    Probability of finding the particle in selected interval based on formula: sum{|psi|^2*dx}.
    :param psi2: normalized probability density
    :param x_start: lower position boundary
    :param x_end: upper position boundary
    :return: probability sum{|psi|^2*dx} from a to b
    """
    P = 0.
    for index, value in enumerate(x_j):
        if x_start <= value <= x_end:
            P += psi2[index] * dx
    return P


def params():
    """
    Information about initial parameters for the console.
    """
    print('Parameters######################\n'
          f'Barrier strength: {round(kb_a, 2)}\n'
          f'E/V-ratio: {round(E, 2)}\n'
          f'Initial position: {round(x0, 2)}\n'
          '################################')


def probs(psi):
    """
    Scattering probabilities.
    :param psi: wave function
    """
    psi2_norm = prob(np.abs(psi) ** 2)
    refl = prob(np.abs(psi) ** 2 / psi2_norm, -x_max, -1.)
    trans = prob(np.abs(psi) ** 2 / psi2_norm, 1., x_max)
    print(f'Reflection probability: {round(refl, 4)}\n'
          f'Transmission probability: {round(trans, 4)}')
