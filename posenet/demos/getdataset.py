import requests
import base64
import json

### Parameters ###
username = '4Dpeteacher'
password = 'Ab123456'
#server_url = "https://sipatdev.eastasia.cloudapp.azure.com" for development
server_url = "https://api.funtomove-jc.hk"

### HELPER FUNCTIONS ###
def constructUrl(path):
    return server_url+path

#### FUNCTIONS ###
def login(username, password):
    print("Getting token...")
    url = constructUrl("/mobile/api/authentication/login")
    data = {'username': username, 'password': password}
    headers = {'ContentType': 'application/json'}
    r = requests.post(url, data=data, headers=headers, verify=False)
    if r.ok:
        data = r.json()
        #print(data['token'])
        return data['token']
    else:
        print("HTTP %i - %s, Message %s" % (r.status_code, r.reason, r.text))
        return 0

### Main program    
login_token = login(username, password)
if(login_token != 0):
    url = constructUrl("/mobile/api/exercise/listExercises")
    headers = {'ContentType': 'application/json',
               'Authorization': "Bearer " + login_token}
    r = requests.post(url, data={}, headers=headers, verify=False)
    if r.ok:
        data = r.json()
        totalN = len(data)
        score_dic = {}
        video_dic = {}
        n = 0
        while (n<totalN):
            skillCode = "skillCode"
            if 'skillCode' in data[n]:
                skillCode = data[n]['skillCode']
            score = "score"
            if 'score' in data[n]:
                score = data[n]['score']
            else:
                n = n+1
                continue
            video = "videoFileUrl"
            if 'videoFileUrl' in data[n]:
                video = data[n]['videoFileUrl']
            else:
                n = n+1
                continue
            #print(data[n])
            if skillCode in score_dic:
                score_dic[skillCode] = score_dic[skillCode] + str(score) + ','
                video_dic[skillCode] = video_dic[skillCode] + video + ','
            else:
                #add the key to score dictionary and video dictionary
                score_dic[skillCode] = str(score) + ','
                video_dic[skillCode] = video + ','
            print(skillCode + " " + str(score) + " " + video)
            n = n+1

    else:
        print("HTTP %i - %s, Message %s" % (r.status_code, r.reason, r.text))

    #save txt file for both score and video
    for key in score_dic:
        filepath_score = "video_label\\"+key+"_score.txt"
        score_file = open(filepath_score,"w")
        score_file.write(score_dic[key][:-1])
        score_file.close()

        filepath_video = "video\\"+key+"_video.txt"
        video_file = open(filepath_video, "w")
        video_file.write(video_dic[key][:-1])
        video_file.close()
        
