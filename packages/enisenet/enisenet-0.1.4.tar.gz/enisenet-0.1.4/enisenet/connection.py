#!/usr/bin/python3
# coding: utf-8

import enisenet.client as client
from enisenet.server import *

# import client
# from server import *

LIST  = SERVERLIST
START = SERVERSTART
STOP  = SERVERSTOP

PORT = 5000

def connect(host='localhost',pseudo='yo',closeCallback=lambda:None):
    return ConnectionManager(host,pseudo,closeCallback)

def server(nbPlayers,verbose=False):
    Server(PORT,nbPlayers,verbose)

class ConnectionManager:
    def __init__(self,host='localhost',pseudo='yo',closeCallback=lambda:None):
        ''' initialise quelques paramètres et démarre le serveur '''
        self.__actions       = {}
        self.__conn          = False
        self.__connectedlist = []
        self.__me            = SERVERNOB
        self.__host          = host
        self.__pseudo        = pseudo
        self.__closeCallback = closeCallback

    def __enter__(self):
        return self

    def __exit__(self,type,value,traceback):
        self.hello(self.__host,self.__pseudo,self.__closeCallback)

    def __list(self):
        ''' retourne la liste des clients connectés '''
        return self.__connectedlist

    def __updatelist(self,sender,pseudo,data):
        ''' met à jour la liste des clients connectés '''
        self.__connectedlist = data
        
    def __updatewhoami(self,sender,pseudo,data):
        ''' met à jour le numéro de port du client '''
        self.__me = data

    def __lostconn(self,callback):
        ''' handler de fermeture de la connexion (volontaire ou non) '''
        self.__conn          = False
        self.__connectedlist = []
        self.__me            = SERVERNOB
        callback()
        
    def hello(self,host,pseudo='yo',closeCallback=lambda:None):
        ''' démarre un nouveau client '''
        # on crée la connexion avec le serveur
        self.__conn   = client.Connect(self,host,PORT,pseudo,
                                       lambda:self.__lostconn(closeCallback))
        # on lie les événements aux callbacks de traitement
        # chaque callback reçoit 3 arguments, dans l'ordre :
        #    1. le numéro du joueur (entier)
        #    2. le pseudo de l'expéditeur (chaîne)
        #    3. les données associées au message (type quelconque)
        # on place le callback de mise à jour de la liste des connectés
        self.__conn.on(LIST,self.__updatelist)
        # on place le callback de mise à jour du numéro de port personnel
        self.__conn.on(SERVERIDENT,self.__updatewhoami)
        # on place les callbacks de l'appli
        for event,actions in self.__actions.items():
            for action in actions:
                self.__conn.on(event,action)
        # on peut démarrer l'écoute des messages entrants
        self.__conn.listen()
    
    def goodbye(self):
        ''' arrêt du client '''
        self.__conn.close()

    def who(self):
        ''' retourne la liste des pseudos
            dans l'ordre des numéros de joueurs '''
        return [player[1] for player in self.__list()]

    def whoami(self):
        ''' retourne le numéro de joueur (si connecté)
            ou -1 (sinon) '''
        for player in self.__list():
            if self.__me == player[0]:
                return player[2]
        return -1

    def player(self,client):
        ''' retourne le numéro de joueur 
            à partir d'un numéro de client '''
        for player in self.__list():
            if client == player[0]:
                return player[2]
        return -1

    def client(self,joueur):
        ''' retourne le numéro de client
            à partir d'un numéro de joueur '''
        for player in self.__list():
            if joueur == player[2]:
                return player[0]
        return -1

    def on(self,event,action):
        ''' mémorise l'action associée à un événement '''
        if event in self.__actions:
            self.__actions[event].append(action)
        else:
            self.__actions[event] = [action]
        
    def off(self,event,action=None):
        ''' oublie l'action associée à un événement '''
        if action:
            if action in self.__actions[event]:
                if len(self.__actions)>1:
                    self.__actions[event].pop(self.__actions[event].index(action))
                else:
                    del self.__actions[event]
        else:
            del self.__actions[event]
        
    def all(self,event,data=None):
        ''' diffuse un événement vers tous les joueurs '''
        if self.__conn:
            self.__conn.all(event,data)
        
    def broadcast(self,event,data=None):
        ''' diffuse un événement vers les autres joueurs '''
        if self.__conn:
            self.__conn.broadcast(event,data)
 
    def emit(self,player,event,data=None):
        ''' émet un événement vers un joueur particulier '''
        if self.__conn:
            self.__conn.emit(self.client(player),event,data)
 
 


