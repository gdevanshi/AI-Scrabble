import Scrabble
import Player
import pygame
import random

def run(width = 1000, height = 600, title = "Scrabble", fps = 60):
    class Struct(object): pass
    game = Struct()
    game.screen = "homeScreen"
    screen = pygame.display.set_mode((width,height))
    game.width = width
    game.height = height
    pygame.display.set_caption(title) 
    game.Scrabble = Scrabble.scrabbleGame()
    game.Scrabble.initValues()
    timer = pygame.time.Clock()
    game.gameOver = False
    gameRunning = True
    while gameRunning:
        time = timer.tick(fps)
        timerFired(time, game)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePressed(screen, game, *(event.pos))
            elif event.type == pygame.MOUSEBUTTONUP:
                mouseReleased(game, *(event.pos))
            elif (event.type == pygame.MOUSEMOTION and
                  event.buttons[0] == 0):
                mouseMoved(game, *(event.pos))
            elif event.type == pygame.QUIT:
                gameRunning = False
        redrawAll(screen, game)            
        pygame.display.flip()
    pygame.quit()

def timerFired(time, game):
    pass

def mouseMoved(game, x, y):
    if (game.screen == "homeScreen"): homeScreenMouseMoved(game, x, y)
    elif (game.screen == "helpScreen"): helpScreenMouseMoved(game, x, y)
    elif (game.screen == "onePlayerScreen"):onePlayerScreenMouseMoved(game, x, y)

def mousePressed(screen, game, x, y):
    if (game.screen == "homeScreen"): homeScreenMousePressed(game, x, y)
    elif (game.screen == "helpScreen"): helpScreenMousePressed(game, x, y)
    elif (game.screen == "onePlayerScreen"):onePlayerScreenMousePressed(screen, game, x,y)

def mouseReleased(game, x, y):
    if (game.screen == "homeScreen"): homeScreenMouseReleased(game, x, y)
    elif (game.screen == "helpScreen"): helpScreenMouseReleased(game, x, y)
    elif (game.screen == "onePlayerScreen"):onePlayerScreenMouseReleased(game,x,y)

def redrawAll(screen, game):
    if (game.screen == "homeScreen"): homeScreenRedrawAll(screen, game)
    elif (game.screen == "helpScreen"): helpScreenRedrawAll(screen, game)
    elif (game.screen == "onePlayerScreen"): onePlayerScreenRedrawAll(screen, game)

#Home Screen functions
def homeScreenMousePressed(game, x, y):
    outline = 2
    align = 3.5
    if (x >= game.width/align + game.buttonAlign) and (x <= game.width/align + \
    game.buttonAlign + game.Scrabble.buttonWidth) and (y >= game.buttonHeight) \
    and (y <= game.buttonHeight + game.Scrabble.buttonHeight):
        game.screen = "onePlayerScreen"
        game.Scrabble = Scrabble.scrabbleGame()
        game.Scrabble.initValues()
        game.playerOne = Player.Player()
        game.playerOne.hand = game.Scrabble.pickNewLetters("abcde")
        game.computer = Player.Player()
        game.computer.hand = game.Scrabble.pickNewLetters("abcde")
        game.Scrabble.playerOneTurn = True
        game.Scrabble.playerTwoTurn = False
    elif (x >= game.width/align + 2*game.buttonAlign - align**2) and \
    (x <= game.width/align + 2*game.buttonAlign - align**2 + \
    game.Scrabble.buttonWidth//2)and(y >= game.buttonHeight + 2*game.buttonAlign) \
    and (y <= game.buttonHeight + 2*game.buttonAlign + game.Scrabble.buttonHeight):
        game.screen = "helpScreen"

def homeScreenMouseReleased(game, x, y):
    pass

def homeScreenMouseMoved(game, x, y):
    pass


def homeScreenRedrawAll(screen, game):
    game.buttonHeight = 300
    game.buttonAlign = 80
    pygame.draw.rect(screen, game.Scrabble.white, (0,0,game.width, game.height))
    #Background from https://tinyurl.com/rxakz92
    background = pygame.image.load("scrabble_background.jpg")
    background = pygame.transform.scale(background, (game.width, game.height))
    screen.blit(background, (0,0))
    #Logo from https://tinyurl.com/rtjgznz
    logo = pygame.image.load("title_logo.png") 
    logoWidth = 400
    logoHeight = 200
    align = 3.5
    logo = pygame.transform.scale(logo, (logoWidth,logoHeight))
    screen.blit(logo, (game.width/align, game.height/(2*align)))
    #Created with font from https://www.fontspace.com/character/scramblemixed
    singlePlayer = pygame.image.load("singlePlayer.png")
    singlePlayer = pygame.transform.scale(singlePlayer, 
    (game.Scrabble.buttonWidth,game.Scrabble.buttonHeight))
    screen.blit(singlePlayer, (game.width/align + game.buttonAlign, game.buttonHeight))
    helpButton = pygame.image.load("help.png")
    helpButton = pygame.transform.scale(helpButton, 
    (game.Scrabble.buttonWidth//2,game.Scrabble.buttonHeight))
    screen.blit(helpButton, (game.width/align + 2*game.buttonAlign - align**2, 
    game.buttonHeight + 2*game.buttonAlign))

#Help Screen functions
def helpScreenMousePressed(game, x, y):
    align = 3.5
    if (x >= game.width/align + 2*game.buttonAlign - align**2) and \
    (x <= game.width/align + 2*game.buttonAlign - align**2 + \
    game.Scrabble.buttonWidth//2)and(y >= game.buttonHeight + 2*game.buttonAlign) \
    and (y <= game.buttonHeight + 2*game.buttonAlign + game.Scrabble.buttonHeight):
        game.screen = "homeScreen"

def helpScreenMouseReleased(game, x, y):
    pass

def helpScreenMouseMoved(game, x, y):
    pass

def helpScreenRedrawAll(screen, game):
    pygame.draw.rect(screen, game.Scrabble.pastelYellow,
    (0,0, game.width, game.height))
    align = 3.5
    align2 = 1.5
    logoWidth = 400
    logoHeight = 200
    #All buttons created using font from https://www.fontspace.com/character/scramblemixed
    helpButton = pygame.image.load("help.png")
    helpButton = pygame.transform.scale(helpButton, (logoWidth,logoHeight))
    screen.blit(helpButton, (game.width/align, game.height/(align**2)))
    homeButton = pygame.image.load("home.png")
    homeButton = pygame.transform.scale(homeButton, 
    (game.Scrabble.buttonWidth//2,game.Scrabble.buttonHeight))
    screen.blit(homeButton, (game.width/align + 2*game.buttonAlign - align**2, 
    game.buttonHeight + 2*game.buttonAlign))
    instructions = "Click the mouse to watch the two computer players make their moves."
    instructions2 = "Each computer player is designed to make the best possible move with its hand."
    game.boardFont = pygame.font.SysFont("sfcompactdisplaythinotf", 20)
    instructions = game.Scrabble.boardFont.render(instructions, 1, game.Scrabble.black)
    instructions2 = game.Scrabble.boardFont.render(instructions2, 1, game.Scrabble.black)
    screen.blit(instructions, (game.width/(align+1), game.height - align2*logoHeight))
    screen.blit(instructions2, (game.width/(align+1)-2*align, game.height - logoHeight))

#Player vs. Computer Screen functions
def onePlayerScreenMousePressed(screen, game, x, y):
    onePlayerScreenRedrawAll(screen, game)
    game.Scrabble.mousePressed(x,y)
    if len(game.playerOne.hand)<2 and len(game.Scrabble.allLetters) == 0:
        game.gameOver = True
        if game.playerOne.score > game.playerTwo.score:
            game.Scrabble.winner = game.playerOne
        elif game.playerOne.score < game.playerTwo.score:
            game.Scrabble.winner = game.playerTwo
    if game.Scrabble.playerOneTurn:
        game.Scrabble.mousePressed(x,y)
        bestWord, bestLocation, bestScore = game.Scrabble.getBestWordAndLocationComputer(game.playerOne)
        if bestWord == "":
            game.Scrabble.playerOneTurn = False
            game.Scrabble.playerTwoTurn = True
        else:
            game.Scrabble.addWordToBoard(bestWord, bestLocation)
            game.playerOne.score += bestScore
            game.Scrabble.updateScoreTiles(bestLocation)
            game.playerOne.changeHand(bestWord)
            game.playerOne.hand += game.Scrabble.pickNewLetters(bestWord)
            game.Scrabble.playerTwoTurn = True
            game.Scrabble.playerOneTurn = False
    elif game.Scrabble.playerTwoTurn:
        game.Scrabble.mousePressed(x,y)
        bestWord, bestLocation, bestScore = game.Scrabble.getBestWordAndLocationComputer(game.computer)
        if bestWord == "":
            game.Scrabble.playerTwoTurn = False
            game.Scrabble.playerOneTurn = True
        else:
            game.Scrabble.addWordToBoard(bestWord, bestLocation)
            game.computer.score += bestScore
            game.Scrabble.updateScoreTiles(bestLocation)
            game.computer.changeHand(bestWord)
            game.computer.hand += game.Scrabble.pickNewLetters(bestWord)
            game.Scrabble.playerTwoTurn = False
            game.Scrabble.playerOneTurn = True
    onePlayerScreenRedrawAll(screen, game)
    if (x >= game.width-game.Scrabble.buttonWidth//2) and \
    (x <= game.width) and(y >= game.buttonHeight + 2*game.buttonAlign) \
    and (y <= game.buttonHeight + 2*game.buttonAlign + game.Scrabble.buttonHeight):
        game.screen = "homeScreen"

def onePlayerScreenMouseReleased(game, x, y):
    pass

def onePlayerScreenMouseMoved(game, x, y):
    game.Scrabble.mouseMoved(x, y)

def onePlayerScreenRedrawAll(screen, game):
    align = 3.5
    align2 = 1.5
    logoWidth = 400
    game.Scrabble.redrawAll(screen)
    game.Scrabble.drawScore(screen, game.playerOne, True)
    game.Scrabble.drawScore(screen, game.computer, False)
    game.Scrabble.drawHand(screen, game.playerOne, True)
    game.Scrabble.drawHand(screen, game.computer, False)
    homeButton = pygame.image.load("home.png")
    homeButton = pygame.transform.scale(homeButton, 
    (game.Scrabble.buttonWidth//2,game.Scrabble.buttonHeight))
    screen.blit(homeButton, (game.width-game.Scrabble.buttonWidth//2, 
    game.buttonHeight + 2*game.buttonAlign))
    if game.gameOver:
        if game.Scrabble.winner == game.playerOne:
            text = "Computer 1 Won!"
            text = game.Scrabble.boardFont.render(instructions2, 1, game.Scrabble.red)
            screen.blit(text, (game.width/(align+1), game.height - align2*logoHeight))
        elif game.Scrabble.winner == game.playerTwo:
            text = "Computer 2 Won!"
            text = game.Scrabble.boardFont.render(instructions2, 1, game.Scrabble.red)
            screen.blit(text, (game.width/(align+1), game.height - align2*logoHeight))

def main():
    run()

if __name__ == '__main__':
    main()

