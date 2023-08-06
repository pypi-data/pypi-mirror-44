#!/usr/bin/env python
# -*- coding: utf8 -*-

# Imports

import argparse
import math
from random import randint
import base64
import binascii
# Funciones

def tieneInverso(numero, modulo):

    try:
        numero == int(numero)
        modulo == int(modulo)
    except:
        return("No has introducido un número")

    return math.gcd(int(numero), int(modulo)) == 1

def euclides(numero, modulo):
    
    n = int(modulo)
    a = int(numero)

    try:
        n == int(modulo)
        a == int(numero)
    except:
        return("No has introducido un número")

    g = [n, a]
    u = [1, 0]
    v = [0, 1]
    y = [None, None]

    i = 1

    while g[i] != 0:
        y.append( g[i-1] // g[i] )
        g.append( g[i-1] - (y[i+1] * g[i]))
        u.append( u[i-1] - (y[i+1] * u[i]))
        v.append( v[i-1] - (y[i+1] * v[i]))
        i += 1
    
    if v[i-1] < 0:
        x = v[i-1] + n
    else:
        x = v[i-1]

    return x

def producto(numero1, numero2):

    producto = numero1 * numero2
    return producto

def Euler(numero1, numero2):
    
    Euler = (numero1 - 1) * (numero2 - 1)
    return Euler

def Cifrar(mensaje, claveCifrado, modulo):
    mensajeCifrado = (mensaje ** claveCifrado) % modulo
    return mensajeCifrado

def Descifrar(mensaje, claveDescifrado, modulo):
    mensajeDescifrado = (mensaje ** claveDescifrado) % modulo
    return mensajeDescifrado

def mensajeASCII(mensaje):

    mensajeASCII = []
    for palabra in mensaje:
        mensajeASCII.append(ord(palabra))
    return mensajeASCII

def ASCII_Hex(mensaje):

    mensajeHex = []
    for numero in mensaje:
        mensajeHex.append(hex(numero)[2:])
    
    return mensajeHex

def Hex_Base64(mensaje):
    
    mensajeBase64 = []
    for numero in mensaje:
        mensajeBase64.append(base64.b64encode(numero.encode()))
    
    return mensajeBase64

def unirBase64(mensaje):

    Base64 = "".encode()
    for i in range(0, len(mensaje)):
        Base64 = Base64 + mensaje[i]
    return Base64

def recibirBase64(mensaje):

    Base64 = []
    for i in range(0,len(mensaje), 4):
        Base64.append(mensaje[i:i+4])
    return  Base64
    
def Base64_Hex(mensaje):
    mensajeHex = []
    for b64 in mensaje:

        mensajeHex.append(base64.b64decode(b64))
        
    return mensajeHex

def Hex_decimal(mensaje):

    mensajeDecimal = []
    for hexa in mensaje:

        hexa = hexa.decode("UTF-8")
        numero = int(hexa, 16)
        mensajeDecimal.append(numero)    
    return mensajeDecimal

def decimal_ASCII(mensaje):

    mensaje1 = ""
    for decimal in mensaje:
    
        mensaje1 = mensaje1 + chr(decimal)

    return mensaje1

if __name__ == "__main__":
    # Programa principal

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--primo1", help = "Inserte un número primo")
    parser.add_argument("-q", "--primo2", help = "Inserte un número primo")
    parser.add_argument("-e", "--clavePublica", help = "Inserte la clave pública de la persona destinataria")
    parser.add_argument("-n", "--modulo", help = "Inserte el módulo de la persona destinataria")
    parser.add_argument("-c", "--cifrar", help = "Inserte el mensaje a cifrar en RSA")
    parser.add_argument("-d", "--descifrar", help = "Inserte el mensaje a descifrar en RSA")
    parser.add_argument("-cc", "--cambiarclave", help = "Indique algo sólo si quiere generar una nueva clave")
    args = parser.parse_args()

    p = int(args.primo1)
    q = int(args.primo2)
    n = producto(p,q)
    print("El módulo n para el cifrado RSA es: {n}".format(n = n))
    e = int(3)
    Euler = Euler(p, q)
    #e = int(input("Escoja un número entre 1 y {e}: ".format(e = Euler)))
    if args.cambiarclave != None:
        e = randint(2, Euler)
        while tieneInverso(e, Euler) == False:
            #print("El número {numero} con modulo {modulo} no tiene inversa.".format(numero=e, modulo= Euler))
            #e = int(input("Escoja otro número entre 1 y {e}: ".format(e = Euler)))
            e = randint(2, Euler)
    
    # for i in range(1, Euler+1):
    #     if tieneInverso(i, Euler) == False:
    #         print("El número {numero} con modulo {modulo} no tiene inversa.".format(numero= i, modulo= Euler))
    #         print("*"*20)
    #     else:
    #         print("El número {e} es válido".format(e = i))
    #         print("El inverso multiplicativo de {e} es: {d}".format(e = i, d = euclides(i, Euler)))
    #         print("*"*20)
    
    print("La clave pública será: {e}".format(e = e))
    d = euclides(e, Euler)
    # print(d)
    # print("El inverso multiplicativo de {e} es: {d}".format(e = e, d = euclides(e, Euler)))
    if args.cifrar != None:
        mensaje = mensajeASCII(args.cifrar)
        mensaje1 = []
        print(mensaje)

        for i in range (0, len(mensaje)):

            mensaje1.append(Cifrar(mensaje[i],  int(args.clavePublica), int(args.modulo)))
            #mensajeCifrado = Cifrar(int(args.cifrar), int(args.clavePublica), int(args.modulo))
        print("El mensaje cifrado es: {m}".format(m = mensaje1))

        mensajeHex = ASCII_Hex(mensaje1)
        print("El mensaje en Hexadecimal es: {m}".format(m = mensajeHex))

        mensajeBase64 = Hex_Base64(mensajeHex)
        print("El mensaje en Base64 es: {m}".format(m = mensajeBase64))

        mensajeFinalBase64 = unirBase64(mensajeBase64)
        print("El mensaje final en Base64 es: {m}".format(m = mensajeFinalBase64))

    if args.descifrar != None:
        mensajeRecibido = recibirBase64(args.descifrar)
        print("El mensaje cifrado recibido es: {}".format(mensajeRecibido))

        mensajeHexRecibido = Base64_Hex(mensajeRecibido)
        print("El mensaje recibido en hexadecimal es: {}".format(mensajeHexRecibido))

        mensajeDecimalRecibido = Hex_decimal(mensajeHexRecibido)
        print("El mensaje recibido en decimal es: {}".format(mensajeDecimalRecibido))

        mensajeDescifrado = []
        for i in range (0, len(mensajeDecimalRecibido)):

            mensajeDescifrado.append(Descifrar(mensajeDecimalRecibido[i], d, n))
        
        print("El mensaje descifrado en ASCII es: {}".format(mensajeDescifrado))

        mensajeFinal = decimal_ASCII(mensajeDescifrado)
        print("El mensaje descifrado legible es: {}".format(mensajeFinal))
    