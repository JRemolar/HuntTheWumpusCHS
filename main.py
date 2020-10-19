#! /usr/bin/env python3


import sys
import random

from models.enumeration import Status, Action
from models.entity import Agent, Knowledge, Cave
from models.knowledge import perceive


def print_intro():
    print('Hunt the Wumpus')
    print('Created by Jose Remolar')
    print('----------------------------')
    print("Introducción")
    print('----------------------------\n')

    print("Objetivo:")
    print("""Encontrar el oro y volver a la casilla de salida lo más rápidamente posible ( vivo, claro¡¡)\n""")

    print("Peligros:")
    print("EL WUMPUS: Un monstruo enorme y apestoso, percibirás su hedor cuando te aproximes")
    print("Los Pozos: Si te descuidas y caes en un pozo, no saldrás de ahí. Percibirás una brisa al acercarte\n")

    print("Puedes lanzar una flecha que matará al wumpus o chocará con la pared.")
    print("Tienes 5 flechas. Suerte.")
    print('----------------------------\n\n')

def print_actions():
    print('1) Avanzar')
    print('2) Girar 90º a la izquierda')
    print('3) Girar 90º a la derecha')
    print('4) Recoger el tesoro')
    print('5) Disparar flecha')


def print_perceptions(perceptions):
    wumpus, pit, gold = perceptions
    if wumpus == Status.Present:
        print('Percibes un olor asqueroso.')
    if pit == Status.Present:
        print('Se nota una fuerte brisa')
    if gold == Status.Present:
        print('Un brillo dorado te deslumbra')
    if perceptions == (Status.Absent, Status.Absent, Status.Absent,):
        print('Todo está normal.')
    print()


def parse_action(action):
    if action == 1:
        return Action.Move, (0,)
    elif action == 2:
        return Action.Turn, -1
    elif action == 3:
        return Action.Turn, 1
    elif action == 4:
        return Action.Grab, None
    elif action == 5:
        return Action.Shoot, None


def print_cave(loc):
    print(' __________________')
    y = 0
    while y < 4:
        x = 0
        while x < 4:
            print('|_X_|' if (x, y) == loc else '|___|', end='')
            x += 1
        print()
        y += 1
    print()


if __name__ == '__main__':

    # define entities
    cave = Cave()
    knowledge = Knowledge()
    agent = Agent()
    # display introduction
    print_intro()
    # run the game
    while True:
        # print('Cave:\n{}\n'.format(cave))
        print('Tu situación:\n{}'.format(agent))
        print_cave(agent.location)
        # perceive in current location
        if agent.location is not None:
            perceptions = perceive(cave, agent.location)
            if perceptions is None:
                print('Has muerto.')
                break
        # print('Perceptions:\n{}\n'.format(perceptions))
            print_perceptions(perceptions)
        print_actions()
        TextInput = input('Qué haces??? ')
        print()
        while TextInput == "":
            TextInput = input('Qué haces??? ')

        numAction = int(TextInput)
        action = parse_action(numAction)
        # perform the action
        if agent.perform(action, cave, knowledge):
            print('Has escuchado un grito sombrío. El Wumpus ha muerto. \n')

        # check if the game is over
        if agent.has_gold and agent.location == (0, 0):
            print_cave(agent.location)
            print('Has ganado!')
            break
