import time
import re
from itertools import repeat

BlueResource =("Blue resource"  ,"41d400f6-e161-4bd5-8d31-c1cd2265e6ab")
BrownResource =("Brown resource" ,"78046ffd-5cc4-4302-b888-363cc1deb970")
YellowResource =("Yellow resource","f35e8287-9cdf-4a76-96df-dd022fbd73d6")
GreenResource =("Green resource" ,"c0bf6be1-0e75-4c2a-9f71-26928842c7d1")
LifePoint=("Life point"    ,"55f9aa93-3c04-4252-be76-c305020ea157")
NormalShield =("Normal shield"  ,"99245f78-2c7b-4cb6-80c3-bdaafb973420")
SkullShield =("Skull shield"   ,"18d254a4-dcea-4299-9732-de4685b16603")
TimeShield =("Time shield"    ,"0fd97d30-4b30-4f3e-ada0-108b93572fc5")
LifeShield=("Life shield"  ,"8881d2fb-1d3f-43ec-a87b-366bac3f1310")
SpecialShield=("Special shield" ,"ea978eb5-1e96-483f-8bed-46f0bddc8577")
Lock = ("Lock", "0171d5b3-4fe0-468f-b323-25b0ff3ab3d5")

locationAx = -471
locationBx = -400
planTLx = -470
planTLy = -240
planTRx = -364
planTRy = -240
planBLx = -470
planBLy = -178
planBRx = -364
planBRy = -178
locationy = 6
TUSixtyX = -488.5
TUSixtyY = -40
TUZeroX = -478.5
TUZeroY = -60
TUGapX = 18.35
CaptainDieX = -200
CaptainDieY = -180
AdventureDieX = -150
AdventureDieY = -180
SetupX = -400
SetupY = 250
ShieldSpotX = -380
ShieldSpotY = 125
showDebug = True #Can be changed to turn on debug - we don't care about the value on game reconnect so it is safe to use a python global

def captainDie():
    return shared.piles['Captain die']

def elementPile():
    return shared.piles['Elements']
    
def locationPile():
    return shared.piles['Locations']
    
def planPile():
    return shared.piles['Plan']

def adventureDie():
    return shared.piles['Adventure die']
    
def setupPile():
    return shared.piles['Setup']

def removedPile():
    return shared.piles['Removed card']

def debug(str):
    if showDebug:
        whisper(str)

def toggleDebug(group, x=0, y=0):
    global showDebug
    showDebug = not showDebug
    if showDebug:
        notify("{} turns on debug".format(me))
    else:
        notify("{} turns off debug".format(me))

        
def num(s):
   if not s: return 0
   try:
      return int(s)
   except ValueError:
      return 0

def moveCard(model, x, y):
    for c in table:
        if c.model == model:
            c.moveToTable(x, y)
            return c
    return table.create(model, x, y)


def getPlayer(id):
    for p in getPlayers():
        if playerID(p) == id:
            return p
    return None




def cardDoubleClicked(args):
    # args = card, mouseButton, keysDown
    mute()
    card = args.card
    if hasattr(card, 'Type'):
        if card.Type == "CaptainDieThrow": # Roll captain die
            rollCaptainDieForPlayer(me, [])
        elif card.Type == "AdventureDieThrow": # Discard Chaos Token
            rollAdventureDieForPlayer(me, card, [])
        elif card.Type == "Element": 
            flipcard(card)
        elif card.Type == "Location": 
            flipcard(card)
        elif card.Type == "Codex 1": 
            flipcard(card)
        elif card.Type == "Codex 2": 
            flipcard(card)
        elif card.Type == "Codex 3": 
            flipcard(card)
        elif card.Type == "Codex 4": 
            flipcard(card)
        elif card.Type == "Codex 5": 
            flipcard(card)
        elif card.Type == "Codex 6": 
            flipcard(card)
        elif card.Type == "Receptacle": 
            flipcard(card)
        elif card.Type == "Conclusion": 
            flipcard(card)
        elif card.Type == "TUMarker": 
            spendTU()
        elif card.Type == "ShieldSpot": 
            removeNormalShield(card)
            removeSkullShield(card)
            removeTimeShield(card)
            removeLifeShield(card)
            removeSpecialShield(card)


def getElement(player, group, x = 0, y = 0):      
    elementNb = askInteger("Which element to get?", 0) 
    if elementNb == None: return
    mute()
    notify("{} grabbed element #{}!".format(me,elementNb))
    card = [card for card in elementPile() if (card.ElementNumber == str(elementNb))]
    for cardToGet in card:
        cardToGet.controller = me
        cardToGet.moveTo(me.hand)

def setPhase(player, group, x = 0, y = 0):      
    phaseNb = askInteger("Set game to which phase?", 1)   
    if phaseNb == None: return
    setGlobalVariable("phase", str(phaseNb))
    notify("{} set phase to {}!".format(me,phaseNb))
    openPlan()

def openLocationAsk(player, group, x = 0, y = 0):    
    locationName = askString("Open which location?", "Base")
    if locationName == None: return
    openLocation(locationName)
    
def openLocation(locationName):     
    phase = getGlobalVariable("phase")
    table_location = [card for card in table if (card.Type == 'Location')]
    for card in table_location:
        card.controller = me
        card.moveTo(locationPile())
    locationCard = [card for card in locationPile() if (card.LocationName == locationName and (card.phase == phase or card.phase == ""))]
    for card in locationCard:
        card.controller = me
        if(card.LocationSpace == 'a'):
            card.moveToTable(locationAx,locationy)
        if(card.LocationSpace == 'b'):
            card.moveToTable(locationBx,locationy)
        if(card.LocationSpace == 'c'):
            card.moveToTable(locationBx+(1*62),locationy)
        if(card.LocationSpace == 'd'):
            card.moveToTable(locationBx+(2*62),locationy)
        if(card.LocationSpace == 'e'):
            card.moveToTable(locationBx+(3*62),locationy)
        if(card.LocationSpace == 'f'):
            card.moveToTable(locationBx+(4*62),locationy)
        if(card.LocationSpace == 'g'):
            card.moveToTable(locationBx+(5*62),locationy)
        if(card.LocationSpace == 'h'):
            card.moveToTable(locationBx+(6*62),locationy)

def openPlan():
    phase = getGlobalVariable("phase")
    table_plan = [card for card in table if (card.Type == 'Plan')]
    for card in table_plan:
        card.controller = me
        card.moveTo(planPile())
    planCard = [card for card in planPile() if (card.phase == phase or card.phase == "")]
    for card in planCard:
        card.controller = me
        if(card.LocationSpace == 'tl'):
            card.moveToTable(planTLx,planTLy)
            flipcard(card)
            card.orientation = 1
        if(card.LocationSpace == 'tr'):
            card.moveToTable(planTRx,planTRy)
            flipcard(card)
            card.orientation = 1
        if(card.LocationSpace == 'bl'):
            card.moveToTable(planBLx,planBLy)
            flipcard(card)
            card.orientation = 1
        if(card.LocationSpace == 'br'):
            card.moveToTable(planBRx,planBRy)
            flipcard(card)
            card.orientation = 1

def resetRun(group, x=0, y=0):
    choiceList = ['Yes', 'No']
    colorsList = ['#FF0000', '#000000'] 
    choice = askChoice("Are you sure you want to reset the run (make sure to have set \"keep\" on all card you need to keep:", choiceList, colorsList)
    if(choice == 1 ):
        cards = [card for card in table if (card.Keep != '1' or card.alternate)]
        for card in cards:
            replaceInDeck(card)
        cards = [card for card in removedPile() if (card.Keep != '1')]
        for card in cards:
            replaceInDeck(card)
        for player in getPlayers():
            remoteCall(player, "clearHand", [])
        openLocation("Base")
        createSetup(table)
        openPlan()



def clearHand():
    cards = [card for card in me.hand if (card.Keep != '1')]
    for card in cards:
        replaceInDeck(card)

def replaceInDeck(card):
    if(card.type == "Location"):
        card.moveTo(locationPile())
    if(card.type == "Element"):
        card.moveTo(elementPile())
    if(card.type == "Plan"):
        card.moveTo(shared.piles['Plan'])
    if(card.type == "Receptacle"):
        card.moveTo(shared.piles['Receptacle'])
    if(card.type == "Conclusion"):
        card.moveTo(shared.piles['Conclusion'])
    if(card.type == "Codex 1"):
        card.moveTo(shared.piles['Codex 1'])
    if(card.type == "Codex 2"):
        card.moveTo(shared.piles['Codex 2'])
    if(card.type == "Codex 3"):
        card.moveTo(shared.piles['Codex 3'])
    if(card.type == "Codex 4"):
        card.moveTo(shared.piles['Codex 4'])
    if(card.type == "Codex 5"):
        card.moveTo(shared.piles['Codex 5'])
    if(card.type == "Codex 6"):
        card.moveTo(shared.piles['Codex 6'])
    if(card.type == "ColorMarker"):
        card.moveTo(shared.piles['Color Marker'])
    if(card.type == "TUMarker"):
        card.moveTo(shared.piles['Setup'])
    if(card.type == "TUMarker"):
        card.moveTo(shared.piles['Setup'])
    if(card.type == "PlayerMarker"):
        card.moveTo(shared.piles['Setup'])
    if(card.type == "LocationMarker"):
        card.moveTo(shared.piles['Setup'])
    if(card.type == "ShieldSpot"):
        card.moveTo(shared.piles['Setup'])

def setKeep(card, x = 0, y = 0):
    notify("{} set keep to card {}!".format(me,card.name))
    card.controller = me
    card.keep = str(1)

def removeKeep(card, x=0, y=0):
    notify("{} remove keep to card {}!".format(me,card.name))
    card.controller = me
    card.keep = str(0)
    
def rollCaptainDieForPlayer(player, group, x = 0, y = 0):           
    mute()
    notify("{} rolled the captain die!".format(me))
    table_captain_die = [card for card in table if (card.Type == 'CaptainDie')]
    for token in table_captain_die:
        if token.controller == me:
            delete(token)
        else:
            remoteCall(token.controller, "delete", [token])
    if captainDie().controller == me:
        die = captainDie().random()
        table.create(die.model, CaptainDieX, CaptainDieY+50, 1, False)
    else:
        remoteCall(captainDie().controller, "rollCaptainDieForPlayer", [me, captainDie(), x, y])

def rollAdventureDieForPlayer(player, groupe, x = 0, y = 0, count = 0):
    if count == 0:
        count = askInteger("Throw how many adventure dice?", 1)
    if count == None: return
    table_adventure_die = [card for card in table if (card.Type == 'AdventureDie')]
    for token in table_adventure_die:
        if token.controller == me:
            delete(token)
        else:
            remoteCall(token.controller, "delete", [token])
    if adventureDie().controller == me:
        for i in range(0,count):
            die = adventureDie().random()
            table.create(die.model, AdventureDieX + i*50, AdventureDieY+50, 1, False)
    else:
        remoteCall(adventureDie().controller, "rollAdventureDieForPlayer", [me, adventureDie(), x, y, count])

#Triggered event OnLoadDeck
# args: player, groups
def deckLoaded(args):
    mute()
    if args.player != me:
        return
    
    #If we are loading into the shared piles we need to become the controller of all the shared piles   
    notify("{} Takes control of the shared decks".format(me))
    for p in shared.piles:
        if shared.piles[p].controller != me:
            shared.piles[p].controller = me
    update()
            
    #Cards for the encounter deck and player deck are loaded into the discard pile because this has visibility="all"    
    #Check for cards with a Setup effects and move other cards back into the correct pile
    for pile in args.groups: 
        notify("{} Takes control of the shared decks".format(pile.name))
        if pile.name == "Adventure die":
            createAdventureDie(table)
        elif pile.name == "Captain die":
            createCaptainDie(table)
        elif pile.name == "Setup":
            createSetup(table)       
        elif pile.name == "Locations":
            openLocation("Base")           
        elif pile.name == "Plan":
            openPlan()             
    update()

def createAdventureDie(table):
    table.create("8d413e42-b400-4395-9044-4b02d401ef5c", AdventureDieX, AdventureDieY, 1, False)

def createCaptainDie(table):
    table.create("d1f5b4a0-c8b0-4c13-b53f-f9ab4a8f3d01", CaptainDieX, CaptainDieY, 1, False)
    
def createSetup(table):
    shieldSpotNo = 0
    setupNo = 0
    for card in setupPile():
        if(card.Type == "ShieldSpot"):
            card.moveToTable(ShieldSpotX+(shieldSpotNo/3*62),ShieldSpotY+(shieldSpotNo%3*40))
            shieldSpotNo +=1
        else:
            card.moveToTable(SetupX+(setupNo*40),SetupY)
            setupNo +=1
    
def delete(card, x=0, y=0):
    mute()
    if card.controller != me:
        whisper("{} does not control '{}' - delete cancelled".format(me, card))
        remoteCall (card.controller, "setControllerRemote", [card, me])
               
    if card.Type == "CaptainDie" or card.Type == "AdventureDie":
        card.delete()
    
def activePlayers():
    count=0
    for p in getPlayers():
        count+=1
#       if not eliminated(p):
#           count+=1
    return count

def spendTU(group, x=0, y=0):
    if(int(getGlobalVariable("temporalUnit")) > 0):
            setGlobalVariable("temporalUnit",int(getGlobalVariable("temporalUnit")) - 1)
            notify("Temporal unit spent! {} temporal unit remaining".format(getGlobalVariable("temporalUnit")))
            moveTU()

def addTU(group, x=0, y=0):
    if(int(getGlobalVariable("temporalUnit")) < 60):
        setGlobalVariable("temporalUnit",int(getGlobalVariable("temporalUnit")) +1)
        moveTU()
        notify("Temporal unit added! {} temporal unit remaining".format(getGlobalVariable("temporalUnit")))



def moveTU():
    table_TU_marker = [card for card in table if (card.Type == 'TUMarker')]
    for token in table_TU_marker:
        if token.controller == me:
            TU = int(getGlobalVariable("temporalUnit"))
            if(TU >= 30):
                token.moveToTable(TUSixtyX+(60-TU)*TUGapX,TUSixtyY)
            else:
                token.moveToTable(TUZeroX+(TU)*TUGapX,TUZeroY)
        else:
            remoteCall(token.controller, "moveTU", [])

def setTU(group, x=0, y=0): 
    count = askInteger("Set temporal unit to which value?", 30)
    if count < 0:
        count = 0
    elif count > 60:
        count = 60
    setGlobalVariable("temporalUnit",str(count))
    notify("Temporal unit set to {}".format(getGlobalVariable("temporalUnit")))
    moveTU()


def cardX(card):
    x, y = card.position
    return x

def cardY(card):
    x, y = card.position
    return y


def findCard(group, model):
    for c in group:
        if c.model == model:
            return c
    return None


#------------------------------------------------------------
# Global variable manipulations function
#------------------------------------------------------------

def getLock():
    lock = getGlobalVariable("lock")
    if lock == str(me._id):
        return True

    if len(lock) > 0: #Someone else has the lock
        return False

    setGlobalVariable("lock", str(me._id))
    if len(getPlayers()) > 1:
        update()
    return getGlobalVariable("lock") == str(me._id)

def clearLock():
    lock = getGlobalVariable("lock")
    if lock == str(me._id):
        setGlobalVariable("lock", "")
        update()
        return True
    debug("{} id {} failed to clear lock id {}".format(me, me._id, lock))
    return False


#Store this player's starting position (his ID for this game)
#The first player is 0, the second 1 ....
#These routines set global variables so should be called within getLock() and clearLock()
#After a reset, the game count will be updated by the first player to setup again which invalidates all current IDs
def myID():
    if me.getGlobalVariable("game") == getGlobalVariable("game") and len(me.getGlobalVariable("playerID")) > 0:
        return playerID(me) # We already have a valid ID for this game
        
    g = getGlobalVariable("playersSetup")
    if len(g) == 0:
        id = 0
    else:
        id = num(g)
    me.setGlobalVariable("playerID", str(id))
    game = getGlobalVariable("game")
    me.setGlobalVariable("game", game)
    setGlobalVariable("playersSetup", str(id+1))
    update()
    debug("Player {} sits in position {} for game {}".format(me, id, game))
    return id

def playerID(p):    
    return num(p.getGlobalVariable("playerID"))

#In phase management this represents the player highlighted in green
def setActivePlayer(p):
   if p is None:
       setGlobalVariable("activePlayer", "-1")
   else:
       setGlobalVariable("activePlayer", str(playerID(p)))
   update()

def setPlayerDone():
    done = getGlobalVariable("done")
    if done:
        playersDone = eval(done)
    else:
        playersDone = set()
    playersDone.add(me._id)
    setGlobalVariable("done", str(playersDone))
    #notify("done {}".format(str(playersDone)))
    update()

def deckLocked():
    return me.getGlobalVariable("deckLocked") == "1"

def lockDeck():
    me.setGlobalVariable("deckLocked", "1")
    
def unlockDeck():
    me.setGlobalVariable("deckLocked", "0")
        
#---------------------------------------------------------------------------
# Workflow routines
#---------------------------------------------------------------------------

#Triggered event OnGameStart
def startOfGame(): 
    unlockDeck()
    setActivePlayer(None)   
    if me._id == 1:    
        setGlobalVariable("game", str(num(getGlobalVariable("game"))+1))
        notify("Starting Game {}".format(getGlobalVariable("game")))

    #---------------------------------------------------------------------------
    # NEW
    #---------------------------------------------------------------------------
    setGlobalVariable("timeCaptain",str([]))
    setGlobalVariable("temporalUnit",str(60))


        
# #Triggered event OnPlayerGlobalVariableChanged
# #We use this to manage turn and phase management by tracking changes to the player "done" variable            
def globalChanged(args):
    debug("globalChanged(Variable {}, from {}, to {})".format(args.name, args.oldValue, args.value))
    if args.name == "done":
        checkPlayersDone()
    elif args.name == "phase":
        notify("Phase: {}".format(args.value))
        


#---------------------------------------------------------------------------
# Table group actions
#---------------------------------------------------------------------------

def addToTable(card):
    x = AgendaX - 45.5
    y = -96
    blocked = overlapPartialCard(x, y)
    while blocked is not None:
        x += 16
        blocked = overlapPartialCard(x, y)
    card.moveToTable(x, y)  
  

    
def toggleLock(group, x=0, y=0):
    if deckLocked():
        unlockDeck()
        if len(me.deck) > 0:
            if isLocked(me.deck.top()):
                lockCard(me.deck.top())
        notify("{} Unlocks his deck".format(me))
    else:
        lockDeck()
        if len(me.deck) > 0:
            lockCard(me.deck.top())
        notify("{} Locks his deck".format(me))
    
#---------------------------------------------------------------------------
# Table card actions
#---------------------------------------------------------------------------

def defaultAction(card, x = 0, y = 0):
    mute()
    flipcard(card, x, y)

        

def inspectCard(card, x = 0, y = 0):
    whisper("{} - model {}".format(card, card.model))
    for k in card.properties:
        if len(card.properties[k]) > 0:
            whisper("{}: {}".format(k, card.properties[k]))
                                
def flipcard(card, x = 0, y = 0):
    mute()
    
    if card.controller != me:
        notify("{} gets {} to flip card".format(me, card.controller()))
        remoteCall(card.controller, "flipcard", card)
        return

    cardx, cardy = card.position

    #Card Alternate Flip
    if card.alternates is not None and "b" in card.alternates:
        keep = card.keep
        if card.alternate == "b":
            card.alternate = ''
        else:
            card.alternate = 'b'
        card.keep = keep
        #if card.Type != "Location": questSetup(card) #Don't do setup for double-sided locations
    elif card.isFaceUp:
        card.isFaceUp = False     
    else:
        card.isFaceUp = True


def rotateRight(card, x = 0, y = 0):
    # Rot90, Rot180, etc. are just aliases for the numbers 0-3
    mute()
    if card.controller == me:
        card.orientation = (card.orientation + 1) % 4
        if card.isFaceUp:
            notify("{} Rotates '{}'".format(me, card.Name))
        else:
            notify("{} Rotates a card".format(me))


def rotateLeft(card, x = 0, y = 0):
    # Rot90, Rot180, etc. are just aliases for the numbers 0-3
    mute()
    if card.controller == me:
        card.orientation = (card.orientation - 1) % 4
        if card.isFaceUp:
            notify("{} Rotates '{}'".format(me, card.Name))
        else:
            notify("{} Rotates a card".format(me))

        
def addBlue(card, x = 0, y = 0):
    addToken(card, BlueResource)

def addGreen(card, x = 0, y = 0):
    addToken(card, GreenResource)

def addYellow(card, x = 0, y = 0):
    addToken(card, YellowResource)

def addBrown(card, x = 0, y = 0):
    addToken(card, BrownResource)

def addLife(card, x = 0, y = 0):
    addToken(card, LifePoint)

def addNormalShield(card, x = 0, y = 0):
    addToken(card, NormalShield)

def addSkullShield(card, x = 0, y = 0):
    addToken(card, SkullShield)

def addTimeShield(card, x = 0, y = 0):
    addToken(card, TimeShield)

def addLifeShield(card, x = 0, y = 0):
    addToken(card, LifeShield)

def addSpecialShield(card, x = 0, y = 0):
    addToken(card, SpecialShield)    




def addToken(card, tokenType):
    mute()
    card.markers[tokenType] += 1
    notify("{} adds a {} to '{}'".format(me, tokenType[0], card))
    
    
def removeBlue(card, x = 0, y = 0):
    subToken(card, BlueResource)

def removeGreen(card, x = 0, y = 0):
    subToken(card, GreenResource)

def removeYellow(card, x = 0, y = 0):
    subToken(card, YellowResource)

def removeBrown(card, x = 0, y = 0):
    subToken(card, BrownResource)

def removeLife(card, x = 0, y = 0):
    subToken(card, LifePoint)

def removeNormalShield(card, x = 0, y = 0):
    subToken(card, NormalShield)

def removeSkullShield(card, x = 0, y = 0):
    subToken(card, SkullShield)

def removeTimeShield(card, x = 0, y = 0):
    subToken(card, TimeShield)

def removeLifeShield(card, x = 0, y = 0):
    subToken(card, LifeShield)

def removeSpecialShield(card, x = 0, y = 0):
    subToken(card, SpecialShield)    
 

def subToken(card, tokenType):
    mute()
    card.markers[tokenType] -= 1
    notify("{} removes a {} from '{}'".format(me, tokenType[0], card))


def lockCard(card, x=0, y=0):
    mute()
    if isLocked(card):
        card.markers[Lock] = 0
    else:
        card.markers[Lock] = 1

def isLocked(card):
    return card.markers[Lock] > 0
    
def setControllerRemote (card, player):
		card.controller=player
    

def shuffleIntoDeck(card, x=0, y=0, player=me):
    mute()
    if card.controller != me:
        whisper("{} does not control '{}' - shuffle cancelled".format(me, card))
        return
        
    if card.Type == "Agenda":
        whisper("Invalid operation on a {} card".format(card.Type))
        return
    if card.Type == "Act":
        whisper("Invalid operation on a {} card".format(card.Type))
        return


    if isPlayerCard(card):
        pile = card.owner.deck
    else:
        pile = encounterDeck()

    who=pile.controller
    notify("{} moves '{}' to '{}'".format(me, card, pile.name))     
    if who != me:
        card.controller = who
        remoteCall(who, "doMoveShuffle", [me, card, pile])
    else:
        doMoveShuffle(me, card, pile)
        
def doMoveShuffle(player, card, pile):
    mute()
    card.moveTo(pile)
    shuffle(pile)
    


#------------------------------------------------------------------------------
# Pile Actions
#------------------------------------------------------------------------------

def draw(group, x = 0, y = 0):
    mute()
    if len(group) == 0: return
    if deckLocked():
        whisper("Your deck is locked, you cannot draw a card at this time")
        return
    card = group[0]
    card.moveTo(me.hand)
    notify("{} draws '{}'".format(me, card))

def shuffle(group):
    mute()
    if len(group) > 0:
        update()
        group.shuffle()
        notify("{} shuffles {}".format(me, group.name))


def search(group, count = None):
    mute()
    if len(group) == 0: return
    if count is None:
        count = askInteger("Search how many cards?", 5)
    if count is None or count <= 0:
        whisper("search: invalid card count")
        return
        
    notify("{} searches top {} cards".format(me, count))    
    moved = 0
    for c in group.top(count):
        c.moveTo(me.piles['Discard Pile'])
        moved += 1
    me.piles['Discard Pile'].lookAt(moved)
    
    
def moveToRemote (token, pile):
   token.moveTo(pile)	
	  

def createCard(group=None, x=0, y=0):
	cardID, quantity = askCard()
	cards = table.create(cardID, x, y, quantity, True)
	try:
		iterator = iter(cards)
	except TypeError:
		# not iterable
		notify("{} created {}.".format(me, cards))
	else:
		# iterable	
		for card in cards:
			notify("{} created {}.".format(me, card))


def drawUnrevealed(group=None, x=0, y=0):
    mute()
    if len(group) == 0:
        notify("{} is empty.".format(group.name))
        return

    card = group[0]
    card.moveToTable(EncounterX, EncounterY, True)
    notify("{} draws an unrevealed card from the {}.".format(me, card.name, group.name))
    return card
    