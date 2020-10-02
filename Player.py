class Player(object):
    def __init__(self):
        self.hand = []
        self.score = 0

    def pickNewLetters(self, letters):
        self.hand += letters
    
    def getNewScore(self, wordScore):
        self.score += wordScore
    
    def changeHand(self, word):
        for letter in word:
            self.hand.remove(letter)
        
    def convertHandToWord(self):
        hand = ""
        for letter in self.hand:
            hand += letter
        return hand


