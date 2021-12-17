import PySimpleGUI as sg
import matplotlib.pyplot as plt
import numpy as np
import sympy as sy
import scipy.integrate as integrate
import scipy.special as special

import math

m0 = 3.64 # Para esferas de aço
pi = math.pi
u0 = 4*pi*10**(-7)
R = 0.0095 #Raio da esfera 
d = 0.02
E = 210 #GPa
v = 0.3
M = 28 #Massa da esfera em g
B = (u0*m0)/(2*pi*d**3)
n = 3 #Esferas antes do imã
m = 3 #Esferas após o imã
rend = 0.97 # Rendimento da colisão 
vinit = 1



Kinit = (M*vinit*vinit)/2 # Energia cinetica inicial

def Fm():
    return -((6*u0*(R**3)*(m0**2))/(pi*(d**7))) 

def Un(n):
    return (4*pi*R**3*B**2*(2*(n+1)*R))/u0     

def F(n):
    x = 1  
    result = integrate.quad(lambda x: Fm(), -math.inf, x)[0]
    for i in range(n):
        x1 = math.sqrt((2/M)*result + x**2)
        dist = x1 - x
        x = x1
        result = integrate.quad(lambda x: Fm(), -math.inf, x1)[0]
    return -(E*math.sqrt((2*R))/(3*(1-(v*v)))*(-(dist + 2*R)**(3/2)))

def Kfinal():
    return rend*(n+m+1)*(Kinit+Un(n))

sg.theme('BluePurple')
layout = [  [sg.Text('Variaveis')],
            [sg.Text('Massa das esferas(g)'), sg.InputText(size = 5,key='-M-')],
            [sg.Text('Raio das esferas(m)'), sg.InputText(size = 5,key='-R-')],
            [sg.Text('Distância entre as esferas(m)'), sg.InputText(size = 5,key='-d-')],
            [sg.Text('Quantidade de esferas antes do imã'), sg.InputText(size = 5,key='-n-')],
            [sg.Text('Quantidade de esferas depois do imã'), sg.InputText(size = 5,key='-m-')],
            [sg.Text('Velocidade inicial da primeira esfera(m/s)'), sg.InputText(size = 5,key='-vinit-')],
            [sg.Text('Força magnética = 0',key='-Fm-')],
            [sg.Text('Energia cinética inicial = 0',key='-Kinit-')],
            [sg.Text('Força entre esferas = 0',key='-F-')],
            [sg.Text('Energia cinética final = 0',key='-Kfinal-')],
            [sg.Button('Ok',key='-OK-'), sg.Button('Cancel')]] 

window = sg.Window('Calculadora de rifle magnético', layout)
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break
    elif event == '-M-':
        M = float(values['-M-'])
    elif event == '-R-':
        R = float(values['-R-'])
    elif event == '-d-':
        d = float(values['-d-'])
    elif event == '-n-':
        n = float(values['-n-'])
    elif event == '-m-':
        m = float(values['-m-'])
    elif event == '-vinit-':
        vinit = float(values['-vinit-'])
    elif event == '-OK-':
        window['-Fm-'].update('Força magnética = ' + str(-Fm()))
        window['-Kinit-'].update('Energia cinética inicial =' + str(Kinit))
        window['-F-'].update('Força entre esferas =' +str(F(n)))
        window['-Kfinal-'].update('Energia cinética final =' + str(Kfinal()))
window.close()

