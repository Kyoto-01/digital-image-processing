#!/usr/bin/env python3

import cv2

from spatial_resolution import SpatialResolutionHandler


def menu():
    print("""# Editor de imagens

## O que deseja fazer?
          
1) Expandir resolução espacial de uma imagem
2) Reduzir resolução espacial de uma imagem
          
Opção: """, end='')

    opcao = input()

    match opcao:
        case "1":
            ...
        case "2":
            ...
        case _:
            ...

    return opcao

def expand_resolution():
    ...

def reduce_resolution():
    ...

def main():
    menu()

main()
