from Dependences import FireWall_sc,Colors,options
import subprocess
import msvcrt
import os


def get_key():
    """Captura tecla pressionada (setas e enter)"""
    ch = msvcrt.getch()
    if ch == b'\xe0':  # tecla especial (setas)
        ch = msvcrt.getch()
        if ch == b'H':  # seta para cima
            return "UP"
        elif ch == b'P':  # seta para baixo
            return "DOWN"
    elif ch == b'\r':  # Enter
        return "ENTER"
    return None

def menu(options):
    idx = 0
    while True:
        os.system("cls")  # limpa tela no Windows
        print("Selecione uma opção:\n")

        for i, opt in enumerate(options):
            if i == idx:
                print(f"{Colors['CYAN']}> {opt}{Colors['RESET']}")
            else:
                print(f"  {opt}")

        key = get_key()
        if key == "UP":
            idx = (idx - 1) % len(options)
        elif key == "DOWN":
            idx = (idx + 1) % len(options)
        elif key == "ENTER":
            return options[idx]


if __name__ == "__main__":
    choice = menu(options)
    if "Opção 1 - Firewall" in choice:
        FireWall_sc.DefenderFirewal()
    if "Iniciar" in choice:
        print(Colors['GREEN'] + "Você escolheu Iniciar!" + Colors['RESET'])
    elif "Configurações" in choice:
        print(Colors['YELLOW'] + "Você escolheu Configurações!" + Colors['RESET'])
    elif "Sair" in choice:
        print(Colors['RED'] + "Você escolheu Sair!" + Colors['RESET'])


