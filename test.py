videosDict = {}
videosDict['sample01.mp4']= 'isan:aa111aa'
videosDict['sample02.mov']= 'isan:bb222bb'
videosDict['sample03.mp4']= 'isan:cc333cc'

videoToPlay = videosDict.get('sample01.mp4')

f = open('./reports/report.txt', 'w')
# python will convert \n to os.linesep
f.write(userID+'\n')
f.write(videoToPlay+'\n')
f.write(DeliveryModality+'\n')
f.write(date.today().strftime("%Y-%m-%d")+'\n')
f.write(CounUser+'-'+LangUser+'\n')
f.write('REJECTED: User not in any contract')
f.close()