# this module renders a level onto a screen
import pygame 
import pathlib
import os
from email.policy import default

ABSOLUTE_BORDER_SIZE = 18
IMAGE_WIDTH = 75
IMAGE_HEIGHT = 75

GRASS = pygame.image.load('./data/images/grass.png')
GRASS = pygame.transform.scale(GRASS, (IMAGE_WIDTH, IMAGE_HEIGHT))

SAND = pygame.image.load('./data/images/sand.png')
SAND = pygame.transform.scale(SAND, (IMAGE_WIDTH, IMAGE_HEIGHT))

UNDERWATER = pygame.image.load('./data/images/underwater.png')
UNDERWATER = pygame.transform.scale(UNDERWATER, (IMAGE_WIDTH, IMAGE_HEIGHT))

DEFAULT_STARTING_Y_COORD = -300
DEFAULT_STARTING_X_COORD = -300

default_x_coord = DEFAULT_STARTING_X_COORD
default_y_coord = DEFAULT_STARTING_Y_COORD

def loadLevel(screen, level_name:str ):
    '''this function takes in a screen and a level_name, and then fetches it from local text files'''
    level_file = open(f"./{level_name}")
    
    level_array = convertFileToLevelArray(level_file)
    renderLevelArrayOnScreen(screen, level_array)
    
    
def convertFileToLevelArray(level_file):
    
    translated_array = [ ]
    
    # for each row in the level
    for line in level_file:
        new_row = [ ]
        total = line.rstrip().split(';')
        
        #for each name:number in the file
        for item in total:
            pieces = item.split(':')
            name = pieces[0]
            number = int(pieces[1])
            
            #add as many tiles as the number specifies
            for num in range(number):
                new_row.append(name)
                
        #if the tiles given are insufficient to meet the border size, add a default tile
        while len(new_row) < ABSOLUTE_BORDER_SIZE:
            new_row.append('DEFAULT')
        
        #if the tiles given exceed the border size, remove tiles starting from the end
        while len(new_row) > ABSOLUTE_BORDER_SIZE:
            new_row = new_row[:len(new_row)-1]
            
        #add the row to the overall array 
        translated_array.append(new_row)
        
    #prints each individual row of the array
    #printArray(translated_array)
    return translated_array
            
def printArray(l:list):
    '''prints each row of an array on a separate line'''
    for row in l:
        print(row)
        
def renderLevelArrayOnScreen(screen, level_array):
    #waiting on seeing how screen is implemented in game_runner before adding
    x_coord = default_x_coord
    y_coord = default_y_coord
    
    for row in level_array:
        for tile in row:
            if tile == 'GRASS':
                screen.blit(GRASS, (x_coord, y_coord))
            elif tile == 'SAND':
                screen.blit(SAND, (x_coord, y_coord))
            elif tile == 'UNDERWATER':
                screen.blit(UNDERWATER, (x_coord, y_coord))
            x_coord += IMAGE_WIDTH
        y_coord += IMAGE_HEIGHT
        x_coord = default_x_coord
    