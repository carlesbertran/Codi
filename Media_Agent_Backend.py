#!/usr/bin/python
import os
import re
import glob
import shutil
import sys
import json
from urllib.request import urlopen
from MPEG21_Parsing_API import *
from datetime import date
from mediaplayer import *


def checkCredentials (userID, videoToPlay, DeliveryModality, MeanUser, CounUser, LangUser):
    #check if the userID is present in any contract
    contractsRefered = []
    checkUser = False
    for contract in os.listdir("./Contracts"):
        contract = ("./Contracts/"+contract)
        print (contract)
        partiesInContract = getIdParties(contract)
        
        for partyID in partiesInContract:
            party = getParty(contract, partyID)
            idInContract = party.get(partyID+'Identifier')
            if userID == idInContract:
                checkUser = True
                #check if the video is an object of the contract
                permissionsInContract = getPermissions(contract)
                checkObject = False

                for permissionID in permissionsInContract:
                    objectInContract = getObject(contract, permissionID)
                    if objectInContract.get(permissionID+'idObject') == videosDict.get(videoToPlay):
                        checkObject = True
                        constrain = getConstraint(contract, permissionID)

                        #Check delivery method
                        deliverModality = constrain.get(permissionID+'deliveryMethod').split('#')
                        checkDeliver = False
                        if deliverModality[1] == DeliveryModality:
                            checkDeliver = True
                            checkMean = True

                            #Broadcasting means check
                            if DeliveryModality == "Broadcasting":
                                checkMean = False
                                mean = getMeans(contract, permissionID).split('#')
                                if mean[1] == MeanUser:
                                    checkMean = True                            
                            
                            #date time check
                            checkDate = False
                            today = date.today()
                            m = today.strftime("%Y-%m-%d")
                            dateList = m.split('-')
                            afterdateAll = constrain.get(permissionID+'afterdate').split('T')
                            beforedateAll = constrain.get(permissionID+'beforedate').split('T')
                            afterdate = afterdateAll[0].split('-')
                            beforedate = beforedateAll[0].split('-')

                            if int(beforedate[0]) < int(dateList[0]) < int (afterdate[0]):
                                checkDate=True
                            elif int(beforedate[0]) == int(dateList[0]) and int(dateList[0]) < int (afterdate[0]):
                                if int(beforedate[1]) < int(dateList[1]):
                                    checkDate=True
                                elif int(beforedate[1]) == int(dateList[1]):
                                    if int(beforedate[2]) <= int(dateList[2]):
                                        checkDate=True
                            elif int(beforedate[0]) < int(dateList[0]) and int(dateList[0]) == int (afterdate[0]):
                                if int(dateList[1]) < int (afterdate[1]):
                                    checkDate=True
                                elif int(dateList[1]) == int (afterdate[1]):
                                    if int(dateList[2]) <= int (afterdate[2]):
                                        checkDate=True
                            elif int(beforedate[0]) == int(dateList[0]) and int(dateList[0]) == int (afterdate[0]):
                                if int(beforedate[1]) < int(dateList[1]) < int (afterdate[1]):
                                    checkDate = True
                                elif int(beforedate[1]) == int(dateList[1]) and int(dateList[1]) < int (afterdate[1]):
                                    if int(beforedate[2]) <= int(dateList[2]):
                                        checkDate = True
                                elif int(beforedate[1]) < int(dateList[1]) and int(dateList[1]) == int (afterdate[1]):
                                    if int(dateList[2]) <= int (afterdate[2]):
                                        checkDate = True
                                elif int(beforedate[1]) == int(dateList[1]) and int(dateList[1]) == int (afterdate[1]):
                                    if int(beforedate[2]) <= int(dateList[2]) and int(dateList[2]) <= int (afterdate[2]):
                                        checkDate = True

                            #CountryCheck
                            checkCountry = False
                            if CounUser == constrain.get(permissionID+'country'):
                                checkCountry = True
                            
                            #LanguageCheck
                            checkLanguage = False
                            if constrain.get(permissionID+'language') == LangUser:
                                checkLanguage = True

                            if checkLanguage and checkCountry and checkDate and checkMean:
                                #########APPROVED SECTION###################
                                #Clean public videos folder
                                files = glob.glob('./PublicVideos/*')
                                for f in files:
                                    os.remove(f)
                                #Store video to play in public videos folder
                                shutil.copy('./Videos/'+videoToPlay, './PublicVideos/')
                                
                                #Update the report.txt
                                writeReport(userID, videoToPlay, DeliveryModality, CounUser, LangUser, 'APPROVED')

                                #Launch the Video Player
                                executePlayer("./PublicVideos")
                                #Kill the process
                                sys.exit(1)
                            elif not checkDate:
                                #OUTDATED REQUEST
                                #Update the report.txt
                                writeReport(userID, videoToPlay, DeliveryModality, CounUser, LangUser, 'REJECTED: The request is outdated')
                                return ("The request is outdated by the contract")
                            elif not checkCountry and checkDate:
                                #COUNTRY NOT ALLOWED
                                #Update the report.txt
                                writeReport(userID, videoToPlay, DeliveryModality, CounUser, LangUser, 'REJECTED: country declared not allowed')
                                return ("Error country declared not allowed")
                            elif not checkLanguage and checkCountry and checkDate:
                                #LANGUAGE INCORRECT
                                #Update the report.txt
                                writeReport(userID, videoToPlay, DeliveryModality, CounUser, LangUser, 'REJECTED: Error language declared not allowed')
                                return ("Error language declared not allowed")
                            elif not checkMean and checkLanguage and checkCountry and checkDate:
                                #Broadcasting Mean incorrect
                                #Update the report.txt
                                writeReport(userID, videoToPlay, DeliveryModality+'-'+MeanUser, CounUser, LangUser, 'REJECTED: Broadcasting Mean declared not allowed')
                                return ("Error Broadcasting Mean declared not allowed")
                                                            
                if not checkObject:
                    #UserID and videoID have no relation in a contract
                    #Update the report.txt
                    writeReport(userID, videoToPlay, DeliveryModality, CounUser, LangUser, 'REJECTED: Video not related to user')
                    return ("You do not have a contract related to the specified video")
                elif not checkDeliver and checkObject:
                    #Delivery Method incorrect
                    #Update the report.txt
                    writeReport(userID, videoToPlay, DeliveryModality, CounUser, LangUser, 'REJECTED: delivery method declared not allowed')
                    return ("Error delivery method declared not allowed")                 
                   
    if not checkUser:
        #userId not in any contract
        #Update the report.txt
        writeReport(userID, videoToPlay, DeliveryModality, CounUser, LangUser, 'REJECTED: User not in any contract')
        return ("User not in any contract")


def writeReport(userID, videoToPlay, deliverModality, CounUser, LangUser, reqResult):
    f = open('./reports/report.txt', 'w')
    # python will convert \n to os.linesep
    f.write(userID+'\n')
    f.write(videoToPlay+'\n')
    f.write(deliverModality+'\n')
    f.write(date.today().strftime("%Y-%m-%d")+'\n')
    f.write(CounUser+'-'+LangUser+'\n')
    f.write(reqResult)
    f.close()

#generate a dict that relates the video data with the isan identifier imitating a Database with this information
videosDict = {}
videosDict['sample01.mp4']= 'isan:aa111aa'
videosDict['sample02.mov']= 'isan:bb222bb'
videosDict['sample03.mp4']= 'isan:cc333cc'