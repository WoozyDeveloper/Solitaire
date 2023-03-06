
"""
    This class is used to create a board for the game.
    The board contains the cards that are in the game.
"""

import random
import pygame
import os

from card import Card

GREEN = (100, 150, 100)


class Board:
    _xSpaceBetweenCards = 300  # space between cards on ox(in pixels)
    # space between cards on oy (when we place them on slots with the first faced forward and the others backwards)
    _ySpaceBetweenCards = 30
    _screen = None
    _cards = []  # deck of cards
    _cardSlots = []  # the 6 slots with cards
    _facedUpCards = []  # cards that have their face up
    _finalSlots = dict()  # the 4 slots with the symbols
    _remainingCards = []  # cards that are not in any slot
    _indexLonelyCard = 0  # index for the remaining cards
    _extractedCard = None  # extracted card from the remaining cards
    _fakeCard = None

    def eliminateCard(self, card):
        """
            Eliminate the card from the _remainingCards

            Args:
                card: the card that you want to remove

        """
        self._remainingCards.remove(card)

    def getFakeCard(self):
        """
            Getter for the separated card

            Args:
                no arguments
            Returns:
                returns the card that helps the player not to get stuck
        """
        return self._fakeCard

    def goToNextCard(self):
        """
            Go to the next card from the array

            Args:
                no arguments
            Returns:
                void
        """
        self._indexLonelyCard += 1

    """
        Flip the card if you click on it
        Args:
            no arguments
        Returns:
            void
    """

    def flipCard(self):

        self._extractedCard.setFaceUp(True)

    def extractCard(self):
        """
            Get 1 card from the remaining cards in the deck

            Args:
                no arguments
            Returns:
                returns a card from the remaining cards in the deck
        """
        # print(self._remainingCards)
        self._extractedCard = self._remainingCards[self._indexLonelyCard % int(
            len(self._remainingCards))]
        return self._extractedCard

    def calculateRemainingCards(self):
        """
            Calculate the remaining cards

            Args:
                no arguments
            Returns:
                void
        """
        self._remainingCards = self._cards
        for i in range(0, 6):
            for card in self._cardSlots[i]:
                # print(card)
                if card in self._remainingCards:
                    self._remainingCards.remove(card)

        # for each final slot
        for x in self._finalSlots:
            for card in x:
                if card in self._remainingCards:
                    self._remainingCards.remove(card)

        #print("cards left: ", len(self._remainingCards))

    def __init__(self):
        """
            Constructor
        """
        # initialize the final slots where the player sorts the cards
        self._finalSlots['heart'] = 0
        self._finalSlots['diamond'] = 0
        self._finalSlots['spade'] = 0
        self._finalSlots['club'] = 0

    def getSlot(self, slot):
        """
            Returns the slot

            Args:
                slot: the slot that you want to return
            Returns:
                returns the selected slot
        """
        return self._cardSlots[slot]

    def printSlots(self):
        """
            Prints the values inside each slot

            Args:
                no arguments
            Returns:
                void
        """
        for i in range(0, 6):
            print("Slot " + str(i) + " " + str(len(self._cardSlots[i])))
            for card in self._cardSlots[i]:
                print("Card= ", card)
            print("")

        print("------------------------------")

    def cardsInSlot(self, slot):
        """
            Returns the number of cards in the slot

            Args:
                slot: selected slot
            Returns:
                returns the length of the selected slot (the number of cards from that slot)
        """
        return len(self._cardSlots[slot])

    def aproximatePositionCardToSlot(self, card, slotIndex):
        """
            This method is used to put a card on the screen with the right allignment

            Args:
                card: the card that you want to aproximate the position
                slotIndex: index of the slot where you want to place the card
            Returns:
                void
        """
        referencePosition = self._cardSlots[slotIndex][0].getPosition()
        if len(self._cardSlots[slotIndex]) <= 1:
            if type(card) is Card:
                card.setPosition(referencePosition[0], referencePosition[1])
        else:
            if type(card) is Card:
                card.setPosition(referencePosition[0], referencePosition[1] +
                                 self._ySpaceBetweenCards * (len(self._cardSlots[slotIndex]) - 1))

    def isMoveValid(self, card, toSlot):
        """
            Checks if the move is valid

            Args:
                card: the card
                toSlot: where you want to place the card
            Returns:
                returns a boolean value representing if the move is valid or not (True if valid, False otherwise)
        """
        if toSlot >= 6:  # sloturile finale
            if toSlot == 6:
                if self._finalSlots['heart'] == 0 and card.getValue() == 1:
                    return True
                elif self._finalSlots['heart'] == int(card.getValue()) - 1 and card.getSymbol() == 'heart':
                    return True
            elif toSlot == 7:
                if self._finalSlots['diamond'] == 0 and card.getValue() == 1:
                    return True
                elif self._finalSlots['diamond'] == int(card.getValue()) - 1 and card.getSymbol() == 'diamond':
                    return True
            elif toSlot == 8:
                if self._finalSlots['spade'] == 0 and card.getValue() == 1:
                    return True
                elif self._finalSlots['spade'] == int(card.getValue()) - 1 and card.getSymbol() == 'spade':
                    return True
            elif toSlot == 9:
                if self._finalSlots['club'] == 0 and card.getValue() == 1:
                    return True
                elif self._finalSlots['club'] == int(card.getValue()) - 1 and card.getSymbol() == 'club':
                    return True

        else:  # sloturile de la 0 la 5
            previousCard = None
            if len(self._cardSlots[toSlot]):
                previousCard = self._cardSlots[toSlot][-1]

            if previousCard == None:
                return True
            if int(previousCard.getValue()) - int(card.getValue()) != 1 or previousCard.getColor() == card.getColor():
                return False
            return True

    """
        Place the card in one of the 4 slots where the player should sort the cards
        Args:
            fromSlot: the slot where the card was taken from
            toSlot: the slot where the card should be put
            card: the card
        Returns:
            void
    """

    def placeCardInFinalSlot(self, fromSlot, toSlot, card):

        if toSlot != -1 and type(card) is Card and fromSlot != 10:
            if card in self._cardSlots[fromSlot]:
                if len(self._cardSlots[fromSlot]) > 0:
                    self._cardSlots[fromSlot].remove(card)
                if len(self._cardSlots[fromSlot]) > 0 and fromSlot != toSlot:
                    self._cardSlots[fromSlot][-1].setFaceUp(True)
            # add the card to the slot
            if toSlot == 6:
                self._finalSlots['heart'] += 1
            elif toSlot == 7:
                self._finalSlots['diamond'] += 1
            elif toSlot == 8:
                self._finalSlots['spade'] += 1
            elif toSlot == 9:
                self._finalSlots['club'] += 1
        elif fromSlot == 10:
            if toSlot == 6:
                self._finalSlots['heart'] += 1
            elif toSlot == 7:
                self._finalSlots['diamond'] += 1
            elif toSlot == 8:
                self._finalSlots['spade'] += 1
            elif toSlot == 9:
                self._finalSlots['club'] += 1

    """
        Place the card in the new slot
            - remove the card from the old slot
            - add the card to the new slot

        Args:
            fromSlot: the slot where the card was taken from
            toSlot: the slot where the card should be put
            card: the card
        Returns:
            void
    """

    def placeCardInSlot(self, fromSlot, toSlot, card):

        if fromSlot == 10:
            pass
        elif toSlot != -1:
            if card in self._cardSlots[fromSlot]:
                if len(self._cardSlots[fromSlot]) > 0:
                    self._cardSlots[fromSlot].remove(card)
                if len(self._cardSlots[fromSlot]) > 0 and fromSlot != toSlot:
                    self._cardSlots[fromSlot][-1].setFaceUp(True)
            # add the card to the slot
        self._cardSlots[toSlot].append(card)
        self.aproximatePositionCardToSlot(card, toSlot)

    """
        Setter method for the screen.

        Args:
            screen: the screen
        Returns:
            void
    """

    def setScreen(self, screen):
        self._screen = screen

    def getCardIndexInSlot(self, card, slot):
        """
            Returns the index of the card in the slot

            Args:
                card: the card
                slot: the slot
            Returns:
                returns the index of the card in the slot
        """
        return self._cardSlots[slot].index(card)

    def checkCardsBelow(self, card, slot):
        """
            Check if the cards below are faced up and in the correct order according to the game

            Args:
                card: the card
                slot: the slot
            Returns:
                returns a boolean value that represents if the cards below 'card' are in the correct order (example: 4, 3, 2)
        """
        for i in range(0, len(self._cardSlots[slot]) - 1):
            if self._cardSlots[slot][i] == card:
                for j in range(i+1, len(self._cardSlots[slot])):
                    card1 = self._cardSlots[slot][j-1]
                    card2 = self._cardSlots[slot][j]

                    if card1.isFacedUp() == False or card2.isFacedUp() == False or int(card1.getValue()) - int(card2.getValue()) != 1 or card1.getColor() == card2.getColor():
                        return False
                    else:
                        return True
        return True

    def detectSelectedCard(self, x, y):
        """
            Detect the selected card

            Args:
                x: ox position on the screen
                y: oy position on the screen
            Returns:
                returns the card that you clicked on (according to the position (x,y))
        """
        # detect the slot position
        if y < 500:
            for i in range(0, 6):
                if x > self._xSpaceBetweenCards * i + 15 and x < self._xSpaceBetweenCards * i + 200:
                    # TODO: see what card on OY is selected
                    cardsInSlot = len(self._cardSlots[i])
                    for j in range(0, cardsInSlot):
                        if y > self._ySpaceBetweenCards * j + 15 and y < self._ySpaceBetweenCards * (j + 1) + 15:
                            if self.checkCardsBelow(self._cardSlots[i][j], i) == True:
                                return self._cardSlots[i][j]
                    # if we have at least a card in the slot
                    if (self._cardSlots[i]):
                        # PUNE POP AICI ???? #nu tin minte ce face asta
                        return self._cardSlots[i][-1]
                    return 0  # if the slot is empty
        elif y >= 500 and x > 1100 and x < 1500:
            print(self._fakeCard)
            return self._fakeCard
        return -1

    def detectSlotPosition(self, x, y):
        """
            Detect on which slot the card goes based on its position

            Args:
                x: ox position on the screen
                y: oy position on the screen
            Returns:
                returns the index of the closest slot from the position (x,y)
        """
        # detect the slot position
        if y < 500:
            for i in range(0, 6):
                if x > self._xSpaceBetweenCards * i + 15 and x < self._xSpaceBetweenCards * i + 200 and y > 15 and y < self._screen.get_rect().height / 2:
                    return i
        else:
            # 4 cases for the 4 slots with the symbols
            if x > 50 and x < 200:  # heart
                return 6
            elif x > 250 and x < 400:  # diamond
                return 7
            elif x > 450 and x < 600:  # spade
                return 8
            elif x > 650 and x < 800:  # club
                return 9

            # one case for the backwards card that gives other cards
            elif x > 1100 and x < 1500:
                return 10
        return -1

    def loadCards(self):
        """
            Load all the cards from the img folder into a deck.
            In each card object put the corresponding picture, color, value and symbol based on the name of the file.

            Args:
                no arguments
            Returns:
                void
        """
        # go through all the files in the img folder
        for file in os.listdir("img"):
            if file.endswith(".svg"):  # file is a .svg
                # get information from the name of the file
                cardSymbol = file.split("-")[0].lower()
                cardValue = file.split("-")[1].split(".")[0]

                # get the color of the card based on the symbol
                if cardSymbol == 'club' or cardSymbol == 'spade':
                    cardColor = 'black'
                else:
                    cardColor = 'red'

                # create a card object
                card = Card("img/" + file, cardColor, cardValue, cardSymbol)

                # add the card to the deck
                self._cards.append(card)

    def shuffleDeck(self):
        """
           Shuffle the deck of cards.

           Args:
               screen: the screen
           Returns:
               void
       """
        # shuffle the deck of cards
        random.shuffle(self._cards)

    def prepareBoard(self):
        """
        Prepare the board by placing the cards

        Args:
            no arguments
        Return:
            void
    """
        self._screen.fill(GREEN)
        # create the card slots
        self._cardSlots = []
        for i in range(0, 6):
            self._cardSlots.append([])

        # put the cards in the card slots
        for i in range(0, 6):
            for j in range(0, i + 1):
                self._cardSlots[i].append(self._cards.pop())

        # print card slots and put the cards on the screen
        for i in range(0, 6):
            # print("Slot " + str(i))
            for index, card in enumerate(self._cardSlots[i]):
                if index < i:
                    faceUp = False
                else:
                    faceUp = True

                # place the card with the face up or down
                card.setFaceUp(faceUp)

                # set the position of the card inside the card object
                card.setPosition(self._xSpaceBetweenCards *
                                 i + 20, index * self._ySpaceBetweenCards + 20)
                card.calculateRect()
                # put the card on the screen
                self.putCard(card, self._xSpaceBetweenCards * i +
                             20, index * self._ySpaceBetweenCards + 20, faceUp)
                # print(card)
            # print("")

        # put the 4 empty slots on the screen

        # 1
        fakeCard = Card("img/heartSymbol.png", "red",
                        "0", "heart", faceUp=True)
        self.putCard(fakeCard, 50, 550)

        # 2
        fakeCard = Card("img/diamondSymbol.png", "red",
                        "0", "diamond", faceUp=True)
        self.putCard(fakeCard, 250, 550)

        # 3
        fakeCard = Card("img/spadeSymbol.png", "black",
                        "0", "spade", faceUp=True)
        self.putCard(fakeCard, 450, 550)

        # 4
        fakeCard = Card("img/clubSymbol.png", "black",
                        "0", "club", faceUp=True)
        self.putCard(fakeCard, 650, 550)

        # put the backwards card on the screen
        self.calculateRemainingCards()  # calculate the remaining cards
        fakeCard = self.extractCard()
        self._fakeCard = fakeCard
        self.putCard(fakeCard, 1100, 550)

    def redrawBoard(self, movingCards, x, y):
        """
            Redraw the board.

            Args:
                movingCards: list of cards that are beeing moved around the board
            Return:
                void
        """

        if type(movingCards) is Card:
            print("E CARD SI O PUN")
            self.putCard(movingCards, x, y, movingCards.isFacedUp())

        for i in range(0, 6):
            # print("Slot " + str(i))
            for index, currentCard in enumerate(self._cardSlots[i]):
                # put on the board all the cards, except the selected one (the one that is being moved)
                # movingCards has only one card
                if type(currentCard) is Card:
                    self.putCard(currentCard, currentCard.ox,
                                 currentCard.oy, currentCard.isFacedUp())

        heartVal = self._finalSlots['heart']
        diamondVal = self._finalSlots['diamond']
        spadeVal = self._finalSlots['spade']
        clubVal = self._finalSlots['club']

        # 1
        if heartVal > 0:
            fakeCard = Card("img/HEART-" + str(heartVal) + ".svg", "red",
                            heartVal, "heart", faceUp=True)
        else:
            fakeCard = Card("img/heartSymbol.png", "red",
                            "0", "heart", faceUp=True)
        self.putCard(fakeCard, 50, 550)

        # 2
        if diamondVal > 0:
            fakeCard = Card("img/DIAMOND-" + str(diamondVal) + ".svg", "red",
                            diamondVal, "diamond", faceUp=True)
        else:
            fakeCard = Card("img/diamondSymbol.png", "red",
                            "0", "heart", faceUp=True)
        self.putCard(fakeCard, 250, 550)

        # 3
        if spadeVal > 0:
            fakeCard = Card("img/SPADE-" + str(spadeVal) + ".svg", "black",
                            spadeVal, "spade", faceUp=True)
        else:
            fakeCard = Card("img/spadeSymbol.png", "black",
                            "0", "spade", faceUp=True)
        self.putCard(fakeCard, 450, 550)

        # 4
        if clubVal > 0:
            fakeCard = Card("img/CLUB-" + str(clubVal) + ".svg", "black",
                            clubVal, "club", faceUp=True)
        else:
            fakeCard = Card("img/clubSymbol.png", "black",
                            "0", "club", faceUp=True)
        self.putCard(fakeCard, 650, 550)

        fakeCard = self.extractCard()
        fakeCard.setFaceUp(True)
        self._fakeCard = fakeCard
        self.putCard(fakeCard, 1200, 550)
       # pygame.display.update()

    def printDeck(self):
        """
            Print all the cards in the deck.
        """
        pass
        # for card in self._cards:
        #     print(card)
        # print("Total cards: " + str(len(self._cards)))

    def putCard(self, card, ox, oy, faceUp=True):
        """
            Place a card on the board on (ox, oy).
            A slot is a place where the player can place a card.

            Args:
                card: the card
                ox: ox position on the screen
                oy: oy position on the screen
                faceUp: boolean value that represents if the card is faced up or down
        """
        # load the image
        card = card

        # if the card is face up, we get the image of the card
        if card.isFacedUp():
            cardImage = card.getPicture()
        else:
            # else we print the back of the card
            cardImage = "img/BACK.png"
        img = pygame.image.load(cardImage).convert_alpha()

        # resize the image
        width = img.get_rect().width
        height = img.get_rect().height
        if faceUp:
            img = pygame.transform.scale(img, (width / 3, height / 3))
            if card.getValue() == "0":
                div = 10
                if card.getSymbol() == "heart":
                    div = 4
                elif card.getSymbol() == "diamond":
                    div = 4
                elif card.getSymbol() == "spade":
                    div = 4
                elif card.getSymbol() == "club":
                    div = 4
                img = pygame.transform.scale(img, (width / div, height / div))
        else:
            img = pygame.transform.scale(img, (width / 6, height / 6))
        # pygame.display.update()
        self._screen.blit(img, (ox, oy))
