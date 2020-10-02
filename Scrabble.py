import pygame
import Player
import random

class scrabbleGame(object):
    def __init__(self):
        self.rows,self.cols = 15, 15
        self.firstRowIndex = self.firstColIndex = 0
        self.lastRowIndex = self.lastColIndex = 14
        self.board = [ (["*"] * self.cols) for row in range(self.rows) ]
        self.tripleWordIndices = [(0,0), (0,7), (0,14), (7,0), (7,14), 
        (14,0), (14,7), (14,14)]
        self.tripleLetterIndices = [(1,5), (1,9), (5,1), (5,5), (5,9), (5,13), 
        (9,1), (9,5), (9,9), (9,13), (13,5), (13,9)]
        self.doubleWordIndices = [(1,1), (1,13), (2,2), (2,12), (3,3), (3,11), 
        (4,4), (4,10), (10,4), (10,10), (11, 3), (11, 11), (12, 2), (12, 12), 
        (13, 1), (13, 13)]
        self.doubleLetterIndices = [(0,3), (0,11), (2,6), (2,8), (3,0), (3,7),
        (3,14), (6,2), (6,6), (6,8), (6,12), (7,3), (7,11), (8,2), (8,6), (8,8),
        (8,12), (11,0), (11,7), (11, 14), (12,6), (12,8), (14,3), (14,11)] 
        self.handLength = 7
        dictFile = open("scrabbleDictionary.txt", "r")
        self.wordDict = set(dictFile.read().split("\n"))    
        letterCounts =[('A', 9), ('B', 2),('C', 2),('D', 4), ('E', 12),('F', 2), 
                        ('G', 3),  ('H', 2), ('I', 9), ('J', 1), ('K', 1), 
                        ('L', 4), ('M', 2), ('N', 6), ('O', 8), ('P', 2), 
                        ('Q', 1), ('R', 6), ('S', 4), ('T', 6), ('U', 4), 
                        ('V', 2), ('W', 2), ('X', 1), ('Y', 2), ('Z', 1)]
        self.allLetters = []
        for pair in letterCounts:
            for num in range(pair[1]):
                self.allLetters.append(pair[0])
        random.shuffle(self.allLetters)
        #Letter Scores for the tiles
        self.letterScores = {'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 
                            'G': 2, 'H': 4, 'I': 1, 'J': 8, 'K': 5, 'L': 1, 
                            'M': 3, 'N': 1, 'O': 1, 'P': 3, 'Q': 10, 'R': 1, 
                            'S': 1, 'T': 1, 'U': 1, 'V': 4, 'W': 4, 'X': 8, 
                            'Y': 4, 'Z': 10, "*" : 0}

    #Updates current letter locations
    def currLetterLocations(self):
        letterIndices = []
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] != "*":
                    letterIndices.append(tuple((row,col)))
        return letterIndices
    
    #Finds all the possible locations on the board where a word could start
    def possibleStartLocations(self):
        possibleStartLocations = []
        secondRow = secondCol = 1
        secondToLastRow = secondToLastCol = 13
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] != "*":
                    #Open tile above taken tile
                    if (row>=secondRow) and \
                    (self.board[row - 1][col] == "*"):
                        possibleStartLocations.append((row-1,col))
                    #Open tile below taken tile
                    if (row<=secondToLastRow) and \
                    (self.board[row + 1][col] == "*"):
                        possibleStartLocations.append((row+1,col))
                    #Open tile to the left of taken tile
                    if (col>=secondCol) and \
                    (self.board[row][col - 1] == "*"):
                        possibleStartLocations.append((row,col-1))
                    #Open tile to the left of taken tile
                    if (col<=secondToLastCol) and \
                    (self.board[row][col + 1] == "*"):
                        possibleStartLocations.append((row,col+1))
        if possibleStartLocations == []:
            possibleStartLocations = [tuple((7,7))]
        result = []
        for tile in possibleStartLocations:
            if tile not in result:
                result.append(tile)
        return result
    
    #Functions to get new letters after playing a word
    def pickNewLetters(self, wordPlayed):
        newLetterLen = len(wordPlayed)
        newLetters = []
        if newLetterLen > len(self.allLetters):
            newLetters = self.allLetters
        else:
            for num in range(newLetterLen):
                newLetters+=self.allLetters.pop()
        return newLetters

    #Adapted from 
    #https://www.cs.cmu.edu/~112/notes/notes-recursion-part1.html#powerset
    def getPossiblePermutations(self, word):
        possibleWords = []
        if len(word)==1:
            possibleWords.append(word)
        else:
            for i in range(len(word)):
                partialPerms =  self.getPossiblePermutations(word[:i] \
                + word[i+1:])
                for item in partialPerms:
                    possibleWords.append(word[i] + item)
        return possibleWords
    
    #Adapted from 
    #https://www.cs.cmu.edu/~112/notes/notes-recursion-part1.html#powerset
    def powerset(self, word):
        if (len(word) == 0):
            return [ "" ]
        else:
            partialSubsets = self.powerset(word[1:])
            allSubsets = [ ]
            for subset in partialSubsets:
                allSubsets.append(subset)
                allSubsets.append(word[0] + subset)
        return allSubsets

    def getPossibleWords(self,hand):
        allPossibleWords = []
        subsets = self.powerset(hand)
        for subset in subsets:
            allPossibleWords.extend(self.getPossiblePermutations(subset))
        return set(allPossibleWords)

    #Functions to check if human placement is according to rules
    def wordConnectedInRow(self, tiles):
        tilesTaken = self.currLetterLocations()
        row = tiles[0][0]
        for index in range(len(tiles)):
            if tiles[index][0] != row:
                return False
        index = 0
        for ((row,col)) in tiles:
            if (row,(col+1)) in tilesTaken and (col < self.lastColIndex):
                tiles.insert(index + 1, ((row,col+1)))
            index += 1
        for index in range(len(tiles) - 1):
            if tiles[index][0] != tiles[index+1][0]:
                return False
        return True
    
    def wordConnectedInColumn(self, tiles):
        tilesTaken = self.currLetterLocations()
        col = tiles[0][1]
        for index in range(len(tiles)):
            if tiles[index][1] != col:
                return False
        index = 0
        for ((row,col)) in tiles:
            if ((row+1),col) in tilesTaken and (row < self.lastRowIndex):
                tiles.insert(index + 1, ((row+1),col))
            index += 1
        for index in range(len(tiles) - 1):
            if tiles[index][1] != tiles[index+1][1]:
                return False
        return True

    def wordAttached(self, tiles):
        possibleStartLocations = self.possibleStartLocations()
        for (row,col) in tiles:
            if (row,col) in possibleStartLocations:
                return True
        return False

    #Function to check if word is a legal Scrabble word
    def isScrabbleWord(self, word):
        if word in self.wordDict:
            return True
        return False
    
    def checkWordPlacement(self, word, tiles):
        locations = []
        locations.append(self.getPlayedWordLocation(tiles))
        if len(self.getAdditionalWordLocations(tiles)) != 0:
            locations+=(self.getAdditionalWordLocations(tiles))
        allPossible = True
        allWordsMade = []
        for location in locations:
            wordMade = ""
            index = 0
            for (row,col) in location:
                if (row,col) not in tiles:
                    wordMade += self.board[row][col]
                else:
                    wordMade += word[index]
                    index += 1
            if len(wordMade) != 0:
                allWordsMade.append(wordMade)
        for wordMade in allWordsMade:
            if not self.isScrabbleWord(wordMade): 
                allPossible = False
        return allPossible

    def isLegalWordHuman(self, word, tiles):
        possibleStartLocations = self.possibleStartLocations()
        if not(self.wordConnectedInRow(tiles) or self.wordConnectedInColumn(tiles)):
            return (False, "The letter tiles are not connected in a line. \
            Please try again.")
        elif not self.wordAttached(tiles): 
            return (False, "The letter tiles are not attached to a word on the board.\
            Please try again.")
        elif not self.isScrabbleWord(word):
            return (False, "This word is not a legal Scrabble word. Please try again.")
        elif self.checkWordPlacement(word, tiles):
            allLocations = []
            allLocations.append(self.getPlayedWordLocation(tiles))
            if len(self.getAdditionalWordLocations(tiles)) != 0:
                allLocations+=(self.getAdditionalWordLocations(tiles))
            return (True, allLocations)
    
    #Functions to get words made with human/computer letter placement  
    def getPlayedWordLocation(self, tiles):
            tilesTaken = self.currLetterLocations()
            wordPlayedTiles = []
            if self.wordConnectedInRow(tiles):
                for ((row, col)) in tiles:
                    if (row,col) not in wordPlayedTiles:
                        wordPlayedTiles+= [(row,col)]
                    if (col != self.lastColIndex):
                        while (((row, col + 1)) in tiles or ((row, col + 1)) in \
                        tilesTaken) and (((row, col + 1)) not in wordPlayedTiles):
                            wordPlayedTiles+=[(row,col+1)]
                            col += 1
                    if (col != self.firstColIndex):
                        while (((row, col - 1)) in tiles or ((row, col - 1)) in \
                        tilesTaken) and (((row, col - 1)) not in wordPlayedTiles):
                            wordPlayedTiles+=[(row,col-1)]
                            col -= 1
            elif self.wordConnectedInColumn(tiles):
                for ((row, col)) in tiles:
                    if (row,col) not in wordPlayedTiles:
                        wordPlayedTiles+= [(row,col)]
                    if (row != self.lastRowIndex):
                        while (((row+1, col)) in tiles or ((row+1, col)) in \
                        tilesTaken) and (((row+1, col)) not in wordPlayedTiles):
                            wordPlayedTiles+=[(row+1,col)]
                            row += 1
                    if (row != self.firstRowIndex):
                        while (((row - 1, col)) in tiles or ((row-1, col)) in \
                        tilesTaken) and (((row-1, col)) not in wordPlayedTiles):
                            wordPlayedTiles+=[(row-1,col)] 
                            row -= 1
            return wordPlayedTiles

    #Functions to add points based on additional words made by touching tiles
    def getAdditionalWordLocations(self, tiles):
        tilesTaken = self.currLetterLocations()
        additionalWordTiles = []
        if self.wordConnectedInRow(tiles):
            for (row,col) in tiles:
                wordMade = []
                if (row,col) not in wordMade:
                    wordMade+= [(row,col)]
                if (row != self.lastRowIndex):
                    while (((row+1, col) in tiles or ((row+1, col)) in \
                    tilesTaken)) and ((row+1, col) not in wordMade):
                        wordMade+=[(row+1,col)]
                        row += 1
                if (row != self.firstRowIndex):
                    while (((row-1, col) in tiles or ((row-1, col)) in \
                    tilesTaken)) and ((row-1, col) not in wordMade):
                        wordMade+=[(row-1,col)] 
                        row -= 1
                if len(wordMade) != 1:
                    additionalWordTiles.append(wordMade)
        elif self.wordConnectedInColumn(tiles):
            for (row,col) in tiles:
                wordMade = []
                if (row,col) not in wordMade:
                    wordMade+= [(row,col)]
                if (col != self.lastColIndex):
                    while (((row, col+1) in tiles or ((row, col+1)) in \
                    tilesTaken)) and ((row, col+1) not in wordMade):
                        wordMade+=[(row,col+1)]
                        col += 1
                if (col != self.firstColIndex):
                    while (((row, col-1) in tiles or ((row, col-1)) in \
                    tilesTaken)) and ((row, col-1) not in wordMade):
                        wordMade+=[(row,col-1)] 
                        col -= 1
                if len(wordMade) != 1:
                    additionalWordTiles.append(wordMade)
        result = []
        for location in additionalWordTiles:
            result.append(self.orderTiles(location))
        return result

    #Copied from 
    #https://www.cs.cmu.edu/~112/notes/notes-recursion-part1.html#powerset
    def quickSort(self, L):
        if (len(L) < 2):
            return L
        else:
            first = L[0]  # pivot
            rest = L[1:]
            lo = [x for x in rest if x < first]
            hi = [x for x in rest if x >= first]
            return self.quickSort(lo) + [first] + self.quickSort(hi)

    def orderTiles(self, tiles):
        return self.quickSort(tiles)

    #Functions to check all possible locations for computer-generated words 
    #Functions to get all locations of open spaces of a particular length n
    def getLocationsOfLength(self, n, inRow):
        tilesTaken = self.currLetterLocations()
        nLengthLocations = []
        if inRow:
            for row in range(self.rows):
                for col in range(self.cols):
                    if ((row,col)) not in tilesTaken:
                        tiles = [(row,col)]
                        for index in range(n-1):
                            if ((row,col+index+1)) not in tilesTaken and \
                            (col != self.lastColIndex):
                                tiles+=[(row,col+index+1)]
                        nLengthLocations.append(tiles)
        elif not inRow:
            for row in range(self.rows):
                for col in range(self.cols):
                    if ((row,col)) not in tilesTaken:
                        tiles = [(row,col)]
                        for index in range(n-1):
                            if ((row+index+1,col)) not in tilesTaken and \
                            (row != self.lastRowIndex):
                                tiles+=[(row+index+1,col)]
                        nLengthLocations.append(tiles)
        index = 0
        while (index < len(nLengthLocations)):
            if len(nLengthLocations[index]) != n:
                nLengthLocations.pop(index)
            else:
                index += 1
        return nLengthLocations
        
    #Function to get all possible row locations of a maximum length of 7
    def getRowLocations(self):
        possibleStartLocations = self.possibleStartLocations()
        possibleRowLocations = []
        for length in range(self.handLength):
            wordLength = length+1
            possibleRowLocations+=(self.getLocationsOfLength(wordLength, True))
        index = 0
        while (index < len(possibleRowLocations)):
            if not self.wordAttached(possibleRowLocations[index]):
                possibleRowLocations.pop(index)
            else:
                index += 1
        return possibleRowLocations
    
    #Function to get all possible column locations of a maximum length of 7
    def getColumnLocations(self):
        possibleStartLocations = self.possibleStartLocations()
        possibleColLocations = []
        for length in range(self.handLength):
            wordLength = length+1
            possibleColLocations+=(self.getLocationsOfLength(wordLength,False))
        index = 0
        while (index < len(possibleColLocations)):
            if not self.wordAttached(possibleColLocations[index]):
                possibleColLocations.pop(index)
            else:
                index += 1
        return possibleColLocations
    
    def getAllLocations(self):
        allPossibleLocations = []
        allPossibleLocations+=(self.getRowLocations())
        allPossibleLocations+=(self.getColumnLocations())
        seen = []
        for location in allPossibleLocations:
            if location not in seen:
                seen.append(location)
        return seen

    #Functions to check if computer-generated words are legal Scrabble words
    def playerPossibleWords(self, player):
        hand = player.convertHandToWord()
        handList = list(self.getPossibleWords(hand)) 
        maxLen = 0
        for word in handList:
            if len(word)>=maxLen:
                maxLen = len(word)
        result = []
        for length in range(maxLen):
            for word in handList:
                if len(word)==(length+1):
                    result.append(word)
        return result

    #Function to check if a computer word is legal
    def isLegalWordComputer(self, word, tiles):
        allPossible = True
        allWordsLocations = []
        allWordsMade = []
        allWordsLocations.append(self.getPlayedWordLocation(tiles))
        allWordsLocations+=(self.getAdditionalWordLocations(tiles))
        for location in allWordsLocations:
            location = self.orderTiles(location)
            wordMade = ""
            index = 0
            if len(location)!= 0 and len(wordMade) == len(location):
                for (row,col) in location:
                    if (row,col) not in tiles:
                        wordMade += self.board[row][col]
                    else:
                        wordMade += word[index]
                        index += 1
            if len(wordMade) != 0:
                allWordsMade.append(wordMade)
        for wordMade in allWordsMade:
            if not self.isScrabbleWord(wordMade): 
                allPossible = False 
        return allPossible

    def getRowWordPlacements(self, player):
        allLocations = self.getAllLocations()
        wordsPermutations = self.playerPossibleWords(player)
        wordsPossible = []
        for word in wordsPermutations:
            for location in allLocations:
                if self.wordConnectedInRow(location):
                    if len(word)==len(location):
                        if self.isLegalWordComputer(word, location):
                            wordsPossible.append((word, location))
        return wordsPossible

    def getColumnWordPlacements(self, player):
        allLocations = self.getAllLocations()
        wordsPermutations = self.playerPossibleWords(player)
        wordsPossible = []
        for word in wordsPermutations:
            for location in allLocations:
                if self.wordConnectedInColumn(location):
                    if len(word)==len(location):
                        if self.isLegalWordComputer(word, location):
                            wordsPossible.append((word, location))
        return wordsPossible
    
    def getAllWordPlacements(self, player):
        allWords = []
        allWords.extend(self.getRowWordPlacements(player))
        allWords.extend(self.getColumnWordPlacements(player))
        return allWords

    #Functions to find and calculate maximum word and score for the computer
    def getWordScore(self, tiles, tempBoard):
        score = 0
        tilesTaken = self.currLetterLocations()
        possibleStartLocations = self.possibleStartLocations()
        index = 0
        for ((row,col)) in tiles:
            if (row,col) in tilesTaken:
                score += self.letterScores[self.board[row][col]]
            elif (row,col) in self.tripleLetterIndices:
                score += 3*self.letterScores[tempBoard[index][1]]
            elif (row,col) in self.doubleLetterIndices:
                score += 2*self.letterScores[tempBoard[index][1]]
            else:
                score += 1
                index += 1
        for (row,col) in tiles:
            if (row,col) in tilesTaken:
                score *= 1
            elif (row,col) in self.tripleWordIndices:
                score *= 3
            elif (row,col) in self.doubleWordIndices:
                score *= 2
        if len(tiles) == self.handLength:
            score += 50
        return score
    
    def getWord(self, word, tiles):
        tilesTaken = self.currLetterLocations()
        wordMade = ""
        index = 0
        for (row,col) in tiles:
            if (row,col) in tilesTaken:
                wordMade+=self.board[row][col]
            else:
                wordMade += word[index]
            index += 1
            
    def getBestWordAndLocationComputer(self, player):
        tilesTaken = self.currLetterLocations()
        allWords = self.getAllWordPlacements(player)
        bestWord = ""
        bestLocation = []
        bestScore = 0
        for (word, location) in allWords:
            score = 0
            tempBoard = []
            index = 0
            if len(word) == len(location):
                for (row,col) in location:
                    if (row,col) in tilesTaken:
                        tempBoard.append(((row,col), self.board[row][col]))
                    else:
                        tempBoard.append(((row,col), word[index]))
                        index+=1
            allWordsMade = []
            allWordsMade.append(self.getPlayedWordLocation(location))
            allWordsMade+=self.getAdditionalWordLocations(location)
            for wordMade in allWordsMade:
                score += self.getWordScore(wordMade, tempBoard)
            if score > bestScore and self.isScrabbleWord(word):
                bestScore = score
                bestLocation = location
                bestWord = word
            
        return bestWord, bestLocation, bestScore
    
    def getHumanScore(self, word, tiles):
        allLocations = []
        allLocations.append(self.getPlayedWordLocation(tiles))
        if len(self.getAdditionalWordLocations(tiles)) != 0:
            allLocations+=(self.getAdditionalWordLocations(tiles))
        tempBoard = []
        index = 0
        for (row,col) in tiles:
            tempBoard.append(((row,col), word[index]))
            index+=1
        score = 0
        for location in allLocations:
            score += self.getWordScore(location, tempBoard)
        return score
    
    #Function to update special scoring board tiles (once they are used)
    def updateScoreTiles(self, tiles):
        for tile in tiles:
            if tile in self.tripleWordIndices:
                self.tripleWordIndices.remove(tile)
            elif tile in self.doubleWordIndices:
                self.doubleWordIndices.remove(tile)
            elif tile in self.tripleLetterIndices:
                self.tripleLetterIndices.remove(tile)
            elif tile in self.doubleLetterIndices:
                self.doubleLetterIndices.remove(tile)
    
    #AI Function to determine which letters need to be saved (for the future)
    #based on frequency of appearance in Scrabble Dictionary
    #Commonly-used letters should be saved for high-scoring words
    def frequencyHeuristic(self):
        self.totalLetters = {}
        for word in self.wordDict:
            for letter in word:
                count = 1 + self.totalLetters.get(letter, 0)
                self.totalLetters[letter] = count
        sum = 0
        for letter in (self.totalLetters):
            sum += self.totalLetters.get(letter)
        
        self.letterAverages = {}
        for letter in (self.totalLetters):
            self.letterAverages[letter] = sum/self.totalLetters.get(letter)
        self.letterAverages["*"] = 0

    #Using frequency heuristic 
    def getAdjustedWordScore(self, tiles, tempBoard):
        self.frequencyHeuristic()
        score = 0
        for tile in tiles:
            letterScore = self.letterAverages[self.board[tile[0]][tile[1]]]
            score -= letterScore
        tilesTaken = self.currLetterLocations()
        possibleStartLocations = self.possibleStartLocations()
        index = 0
        for ((row,col)) in tiles:
            if (row,col) in tilesTaken:
                score += self.letterScores[self.board[row][col]]
            elif (row,col) in self.tripleLetterIndices:
                score += 3*self.letterScores[tempBoard[index][1]]
            elif (row,col) in self.doubleLetterIndices:
                score += 2*self.letterScores[tempBoard[index][1]]
            else:
                score += 1
                index += 1
        for (row,col) in tiles:
            if (row,col) in tilesTaken:
                score *= 1
            elif (row,col) in self.tripleWordIndices:
                score *= 3
            elif (row,col) in self.doubleWordIndices:
                score *= 2
        if len(tiles) == self.handLength:
            score += 50
        return score
    
    #Gameplay functions
    def addWordToBoard(self, word, tiles):
        index = 0
        for ((row, col)) in tiles:
            self.board[row][col] = word[index]
            index += 1
    
    #Graphics functions for game screen
    def initValues(self):
        pygame.init()
        self.width = 1000
        self.height = 600
        self.margin = 50
        self.buttonFont = pygame.font.SysFont("optimattc", 18)
        self.boardFont = pygame.font.SysFont("sfcompactdisplaythinotf", 20)
        self.scoreFont = pygame.font.SysFont("sfcompactdisplaythinotf", 10)
        self.white = (255,255,255)
        self.black = (0,0,0)
        self.pastelYellow = (253, 253, 150) #yellow color for Scrabble board color
        self.orange = (255,140,0) #Triple Word Score tile color
        self.green = (50,205,50) #Triple Letter Score tile color
        self.red = (255,0,0) #Double Word Score tile color
        self.blue = (30,144,255) #Double Letter Score tile color
        self.tan = (222,184,135) #Player hand tile color
        self.cyan = (0,255,255) #Letter tiles added on board color
        self.playButtonColorOne = self.passButtonColorOne = (50,205,50)
        self.buttonWidth = 250
        self.buttonHeight = 50
        self.buttonX = 635
        self.buttonY = 475
        self.firstHandRow = 11
        self.secondHandRow = 3
        self.outsideBoardFirstCol = 18
        self.outsideBoardLastCol = 25
        self.drawnBoard = [(["*"] * self.cols) for row in range(self.rows)]
        #Initialized values for computer to play
        self.playerOneTurn = True
        self.playerTwoTurn = False
        self.playedOne = False
        self.passedOne = False
        self.winner = None
        self.output = "Click for the computer to make a move."

    def mouseMoved(self, x, y):
        gap = 4
        align = 6
        if (x >= self.buttonX) and (x <= self.buttonX + self.buttonWidth//gap)\
        and (y >= self.buttonY) and (y <= self.buttonY+self.buttonHeight-align):
            self.playButtonColorOne = (50, 255, 50)
        else: 
            self.playButtonColorOne = (50, 205, 50)
        if (x >= self.buttonX+2*self.margin) and (x <= self.buttonX + \
        2*self.margin + self.buttonWidth//gap) and (y >= self.buttonY) and \
        (y <= self.buttonY+self.buttonHeight-align):
            self.passButtonColorOne = (50, 255, 50)
        else: 
            self.passButtonColorOne = (50, 205, 50)
    
    def mousePressed(self, x, y):
        gap = 4
        align = 6
        if (x >= self.buttonX) and (x <= self.buttonX + self.buttonWidth//gap)\
        and (y >= self.buttonY) and (y <= self.buttonY+self.buttonHeight-align):
            self.playedOne = True
        elif (x >= self.buttonX+2*self.margin) and (x <= self.buttonX + \
        2*self.margin + self.buttonWidth//gap) and (y >= self.buttonY) and \
        (y <= self.buttonY+self.buttonHeight-align):
            self.passedOne = True
        
    #General functions for screen design and displaying logistics
    def drawTitle(self, screen):
        logo = pygame.image.load("title_logo.png")
        logoWidth = 100
        logoHeight = 50
        align = 3
        logo = pygame.transform.scale(logo, (logoWidth,logoHeight))
        screen.blit(logo, ((self.width/align)+2*self.margin ,\
        self.height/(align*align)-self.margin-(align*align)))

    def drawButton(self, screen, x, y, color, text):
        outline = 3
        gap = 4
        align = 6
        pygame.draw.rect(screen, color, (x,y,self.buttonWidth//gap,
        self.buttonHeight - align))
        pygame.draw.rect(screen, self.black, (x,y,self.buttonWidth//gap,
        self.buttonHeight - align), outline)
        text2 = self.buttonFont.render(text, 1, self.black)
        if len(text) > gap:
            screen.blit(text2, (x + align, y + align+gap))
        else:
            screen.blit(text2, (x + align*2+gap, y + align+gap))
    
    def drawScoreboard(self, screen):
       gap = 4 
       score = pygame.image.load("score.png")
       score = pygame.transform.scale(score,(self.buttonWidth, \
       self.buttonHeight + 2*self.margin))
       screen.blit(score, (self.buttonX, self.height//gap))
       pygame.draw.rect(screen, self.pastelYellow, (self.buttonX,self.height//gap 
       + 2*self.margin+self.margin//2, self.buttonWidth, self.buttonWidth//2))
       pygame.draw.rect(screen, self.black, (self.buttonX,self.height//gap 
       + 2*self.margin+self.margin//2, self.buttonWidth, self.buttonWidth//2),gap)

    def drawScore(self, screen, player, isPlayerOne):
        text = str(player.score)
        gap = 4
        align = 3
        if isPlayerOne:
            name = "Computer 1"
            name = self.buttonFont.render(name, 1, self.black)
            text = self.buttonFont.render(text, 1, self.black)
            screen.blit(name, (self.buttonX +self.margin//2, 
            self.height//gap + align*self.margin))
            screen.blit(text, (self.buttonX + self.margin, self.height//align + \
            self.buttonWidth//2))
        else:
            name = "Computer 2"
            name = self.buttonFont.render(name, 1, self.black)
            text = self.buttonFont.render(text, 1, self.black)
            screen.blit(name, (self.buttonX +align*self.margin, self.height//gap \
            + align*self.margin))
            screen.blit(text, (self.buttonX + gap*self.margin - self.margin//2, 
            self.height//align + self.buttonWidth//2))

    def drawBoardTile(self, screen, row, col, color, text, text2):
        text = " " + text
        self.boardSide = 500
        self.tileWidth = self.boardSide/self.rows
        outline = 2
        align = 8
        pygame.draw.rect(screen, color, (col*self.tileWidth+self.margin,
        row*self.tileWidth+self.margin, self.tileWidth, self.tileWidth))
        pygame.draw.rect(screen, self.black, (col*self.tileWidth+self.margin,
        row*self.tileWidth+self.margin, self.tileWidth, self.tileWidth), outline)
        text = self.boardFont.render(text, 1, self.black)
        screen.blit(text, (col*self.tileWidth+self.margin+outline, 
        row*self.tileWidth+self.margin + align/2))
        text2 = self.scoreFont.render(text2, 1, self.black)
        screen.blit(text2, ((col+outline)*self.tileWidth+align-outline, 
        (row+outline)*self.tileWidth))

    def drawHand(self, screen, player, isPlayerOne):
        if isPlayerOne:
            index = 0
            for col in range(self.outsideBoardFirstCol, self.outsideBoardLastCol):
                if index < len(player.hand):
                    self.drawBoardTile(screen, self.firstHandRow, col, self.tan, 
                    player.hand[index], str(self.letterScores[player.hand[index]]))

                else:
                    self.drawBoardTile(screen, self.firstHandRow, col, self.tan, 
                    "*", "")
                index += 1
        else:
            index = 0
            for col in range(self.outsideBoardFirstCol, self.outsideBoardLastCol):
                if index < len(player.hand):
                    self.drawBoardTile(screen, self.secondHandRow, col, self.tan, 
                    player.hand[index], str(self.letterScores[player.hand[index]]))
                else:
                    self.drawBoardTile(screen, self.secondHandRow, col, self.tan, 
                    "*", "")
                index += 1

    def drawStar(self, screen, row, col, color):
        gap = self.tileWidth/3
        shift = 2
        p1 = (col*self.tileWidth + self.margin + self.tileWidth//2, 
        row*self.tileWidth + self.margin)
        p2 = (col*self.tileWidth + self.margin, 
        row*self.tileWidth + self.margin + 2*gap + shift)
        p3 = ((col+1)*self.tileWidth + self.margin, 
        row*self.tileWidth + self.margin + 2*gap + shift)
        pygame.draw.polygon(screen, color, [p1, p2, p3])
        p4 = (col*self.tileWidth + self.margin, 
        row*self.tileWidth + self.margin + gap - shift)
        p5 = ((col+1)*self.tileWidth + self.margin, 
        row*self.tileWidth + self.margin + gap - shift)
        p6 = (col*self.tileWidth + self.margin + self.tileWidth//2, 
        (row+1)*self.tileWidth + self.margin)
        pygame.draw.polygon(screen, color, [p4, p5, p6])

    def drawBoard(self, screen):
        for row in range(self.rows):
            for col in range(self.cols):
                if (row,col)==(7,7):
                    self.drawStar(screen, row, col, self.red)
                if self.board[row][col] != "*":
                    self.drawBoardTile(screen, row, col, self.cyan, self.board[row][col], str(self.letterScores[self.board[row][col]]))
                elif self.drawnBoard[row][col] != "*":
                    self.drawBoardTile(screen, row, col, self.tan, self.drawnBoard[row][col], str(self.letterScores[self.drawnBoard[row][col]]))
                elif (row,col) in self.tripleWordIndices:
                    self.drawBoardTile(screen, row, col, self.orange, self.drawnBoard[row][col], "")
                elif (row,col) in self.tripleLetterIndices:
                    self.drawBoardTile(screen, row, col, self.green, self.drawnBoard[row][col], "")
                elif (row,col) in self.doubleWordIndices:
                    self.drawBoardTile(screen, row, col, self.red, self.drawnBoard[row][col], "")
                elif (row,col) in self.doubleLetterIndices:
                    self.drawBoardTile(screen, row, col, self.blue, self.drawnBoard[row][col], "")
                else:
                    self.drawBoardTile(screen, row, col, self.pastelYellow, self.drawnBoard[row][col], "")
    
    def drawKey(self, screen):
        keyY = 550
        outline = 3
        gap = 30
        midGap = 100
        pygame.draw.rect(screen, self.black, (self.margin, keyY, self.boardSide,
        self.buttonHeight), outline)
        self.drawButton(screen, midGap, keyY + outline, self.orange, "TW")
        self.drawButton(screen, midGap + gap + self.buttonWidth//outline, keyY + 
        outline, self.green, "TL")
        self.drawButton(screen, midGap + 2*(gap + self.buttonWidth//outline), 
        keyY + outline, self.red, "DW")
        self.drawButton(screen, midGap + outline*(gap + self.buttonWidth//outline), 
        keyY + outline, self.blue, "DL")
    
    def drawOutput(self, screen):
        gap = 1.2
        text = self.buttonFont.render(self.output, 1, self.red)
        screen.blit(text, (self.buttonX-gap*self.margin, self.height-self.margin))

    def redrawAll(self, screen):
        gap = 4
        pygame.draw.rect(screen, self.white, (0,0, self.width, self.height))
        self.drawBoard(screen)
        self.drawTitle(screen)
        self.drawButton(screen, self.buttonX, self.buttonY, self.playButtonColorOne, 
        "Play")
        self.drawButton(screen, self.buttonX + 2*self.margin, self.buttonY, 
        self.passButtonColorOne, "Pass")
        self.drawScoreboard(screen)
        self.drawKey(screen)
        self.drawOutput(screen)
        
        



