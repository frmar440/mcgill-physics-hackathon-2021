import numpy as np


def spinor(theta, phi):
    return (np.cos(theta/2), np.exp(1j*phi)*np.sin(theta/2))


def analyzer(spinor, orientation, P_in):
    """
    Stern-Gerlach analyzer
    :param spinor: tuple (a, b) - spin state
    :param orientation: tuple (theta, phi) - analyzer orientation
    :param P_in: input probability
    :return: dict
    """
    a, b = spinor
    theta, phi = orientation

    spinor_up = (np.cos(theta/2), np.exp(1j*phi)*np.sin(theta/2))
    spinor_down = (np.sin(theta/2), -np.exp(-1j*phi)*np.cos(theta/2))
    P_up = np.absolute(a*np.cos(theta/2) + b*np.sin(theta/2)*np.exp(-1j*phi))**2
    P_down = np.absolute(a*np.sin(theta/2) - b*np.cos(theta/2)*np.exp(-1j*phi))**2

    output = {"up":(spinor_up, P_up, P_in*P_up), "down":(spinor_down, P_down, P_in*P_down)}
    return output