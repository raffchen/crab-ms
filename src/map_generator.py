# this module renders a level onto a screen
import pygame 

ABSOLUTE_BORDER_SIZE = 10

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
    printArray(translated_array)
    return translated_array
            
def printArray(l:list):
    '''prints each row of an array on a separate line'''
    for row in l:
        print(row)
        
def renderLevelArrayOnScreen(screen, level_array):
    #waiting on seeing how screen is implemented in game_runner before adding
    pass
    
    
loadLevel(None, 'level1.txt')