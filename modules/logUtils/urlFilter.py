'''
@File    :   urlFilter.py
@Time    :   2020/12/03 15:49:32
@Author  :   Chengze Zhang 
@Contact :   chengze1996@gmail.com
@License :   Copyright (c) 2020 Chengze Zhang
'''

# here put the import lib


class TemplateUrl(object):
    def __init__(self, s):
        self.template = s
        self.memIdx = []
# num > THRESHOULD，这就是一个固定模板 
 # TODO:
    
def urlConvert(url: str, users, instituteIds, names)->str:
    # filter url
    subs = url.split('/')
    if len(subs) > 4:
        subs = subs[:4]
    for i, sub in enumerate(subs):
        if sub == "" or i == 0: continue
        if sub in users: subs[i] = "userId"
        elif sub.split("-")[0] in instituteIds: subs[i] = "userId"
        elif sub in instituteIds: subs[i] = "institutionId"
        elif sub in names: subs[i] = "name"
        elif len(sub) == 32: subs[i] = "hash"
        elif 'By' in subs[i-1]:
            subs[i] = subs[i-1].split('By')[-1]
        elif 'code' in subs[i-1] or 'Code' in subs[i-1]:
            subs[i] = 'code'
        elif 'Id' in subs[i-1]:
            subs[i] = 'id'
        elif subs[i-1] == 'assetTag':
            for j in range(i, len(subs)):
                subs[j] = "tag"
            break
            
#         elif subs[i-1] == "queryMidAllActivities":
#             subs[i] = "activity"
#         elif subs[i-1] == "queryThroughLastActor":
#             subs[i] = "actor"

        elif subs[i-1].startswith("get"):
            subs[i] = subs[i-1].split('get')[-1]
        elif subs[i-1].startswith("update"):
            subs[i] = subs[i-1].split('update')[-1]
        elif subs[i-1].startswith("query"):
            subs[i] = subs[i-1].split('query')[-1]

        elif subs[i-1] == "changeExeBudgetUseState":
            subs[i] = "state"
        
        elif "manualActivity" in sub:
            subs[i] = "manualActivity"

        elif subs[i-1] == "arBillType":
            subs[i] = "type"
        elif subs[i-1] == "isAlreadyEndAcpt":
            subs[i] = "userId"
        
        elif subs[i-1] == "updateTHOrgUnit" or subs[i-1] == "updateTHrAssignmentsNew":
            for j in range(i, len(subs)):
                subs[j] = "unit"
            break

            
        elif subs[i-1] == "role":
            subs[i] = "role"
        elif subs[i-1] == "tOdOfficeTemplates":
            subs[i] = "id"
    return "/".join(subs)
