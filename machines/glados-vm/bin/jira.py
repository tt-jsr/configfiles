#!/usr/bin/python
import requests
import json
import sys


def getData(resp, path):
    parts = path.split('/')
    d = resp
    for p in parts:
        d = d[p]

    return d

def printResult(format, resp):
    fields = {}
    fields['issue'] = getData(resp, 'key')
    fields['summary'] = getData(resp, 'fields/summary')
    fields['description'] = getData(resp, 'fields/description')
    fields['assignee'] = getData(resp, 'fields/assignee/displayName')
    fields['status'] = getData(resp, 'fields/status/name')
    fields['creator'] = getData(resp, 'fields/creator/displayName')
    fields['reporter'] = getData(resp, 'fields/reporter/displayName')
    print format_str.format(**fields)

def getIssue(deb_number):
    url = "http://172.17.250.119/api/jira.php/issue/DEB-{0}?pretty=true".format(deb_number)
    response = requests.get(url)
    return response.json()

if __name__ == "__main__":
    arg = 1
    format_default = "issue: {issue}\nsummary:{summary}\n{description}\nstatus: {status}"
    format_full = "issue: {issue}\nsummary:{summary}\n{description}\nstatus: {status}\nassignee: {assignee}\ncreator: {creator}\nreporter: {reporter}"
    format_summary = "issue: {issue}\nsummary:{summary}"
    format_str = format_default
    if len(sys.argv) == 1 or sys.argv[1] == '--help':
        print "jira.py [issue] [-f format_str]"
        print "format_str: full | summary | default | {field}..."
        print "Fields for format are:"
        print "    issue, summary, description, assignee, status, creator, reporter"
        exit (1)
    while arg < len(sys.argv):
        if sys.argv[arg] == "-f":
            arg+=1
            format_str = sys.argv[arg]
            if format_str == 'full':
                format_str = format_full
            if format_str == 'summary':
                format_str = format_summary
            if format_str == 'default':
                format_str = format_default
            arg+=1
        else:
            issue = sys.argv[arg]
            arg+=1

    resp = getIssue(issue)
    try:
        printResult(format_str, resp)
    except:
        pass

#   "expand": "renderedFields,names,schema,operations,editmeta,changelog,versionedRepresentations",
#   "id": "131133",
#   "self": "https://tradingtech.atlassian.net/rest/api/2/issue/131133",
#   "key": "DEB-49013",
#   "fields": {
#       "fixVersions": [
#           {
#               "self": "https://tradingtech.atlassian.net/rest/api/2/version/27300",
#               "id": "27300",
#               "name": "16.11.1",
#               "archived": false,
#               "released": false
#           }
#       ],
#       "resolution": null,
#       "lastViewed": null,
#       "priority": {
#           "self": "https://tradingtech.atlassian.net/rest/api/2/priority/3",
#           "iconUrl": "https://tradingtech.atlassian.net/images/icons/priorities/major.svg",
#           "name": "Major",
#           "id": "3"
#       },
#       "customfield_14701": {
#           "self": "https://tradingtech.atlassian.net/rest/api/2/customFieldOption/12304",
#           "value": "5 Gallon",
#           "id": "12304"
#       },
#       "labels": [

#       ],
#       "timeestimate": null,
#       "aggregatetimeoriginalestimate": null,
#       "issuelinks": [

#       ],
#       "assignee": {
#           "self": "https://tradingtech.atlassian.net/rest/api/2/user?username=jeff.richards",
#           "name": "jeff.richards",
#           "key": "jeff.richards",
#           "emailAddress": "Jeff.Richards@tradingtechnologies.com",
#           "avatarUrls": {
#               "48x48": "https://tradingtech.atlassian.net/secure/useravatar?ownerId=jeff.richards&avatarId=16100",
#               "24x24": "https://tradingtech.atlassian.net/secure/useravatar?size=small&ownerId=jeff.richards&avatarId=16100",
#               "16x16": "https://tradingtech.atlassian.net/secure/useravatar?size=xsmall&ownerId=jeff.richards&avatarId=16100",
#               "32x32": "https://tradingtech.atlassian.net/secure/useravatar?size=medium&ownerId=jeff.richards&avatarId=16100"
#           },
#           "displayName": "Jeff Richards (TT)",
#           "active": true,
#           "timeZone": "America/Chicago"
#       },
#       "status": {
#           "self": "https://tradingtech.atlassian.net/rest/api/2/status/10607",
#           "description": "",
#           "iconUrl": "https://tradingtech.atlassian.net/images/icons/statuses/generic.png",
#           "name": "In Development",
#           "id": "10607",
#           "statusCategory": {
#               "self": "https://tradingtech.atlassian.net/rest/api/2/statuscategory/4",
#               "id": 4,
#               "key": "indeterminate",
#               "colorName": "yellow",
#               "name": "In Progress"
#           }
#       },
#       "components": [
#           {
#               "self": "https://tradingtech.atlassian.net/rest/api/2/component/12201",
#               "id": "12201",
#               "name": "OC",
#               "description": "It is the equivalent of a 7.x Gateway. When an order connector initializes, it has no information on which connections it has to run with. The order connectors talk to each other (through Zoo Keeper) and elect a leader. The leader connects to TTUS and downloads all connections for that market and distributes it to order connectors in the cluster for that market."
#           }
#       ],
#       "aggregatetimeestimate": null,
#       "creator": {
#           "self": "https://tradingtech.atlassian.net/rest/api/2/user?username=jeff.richards",
#           "name": "jeff.richards",
#           "key": "jeff.richards",
#           "emailAddress": "Jeff.Richards@tradingtechnologies.com",
#           "avatarUrls": {
#               "48x48": "https://tradingtech.atlassian.net/secure/useravatar?ownerId=jeff.richards&avatarId=16100",
#               "24x24": "https://tradingtech.atlassian.net/secure/useravatar?size=small&ownerId=jeff.richards&avatarId=16100",
#               "16x16": "https://tradingtech.atlassian.net/secure/useravatar?size=xsmall&ownerId=jeff.richards&avatarId=16100",
#               "32x32": "https://tradingtech.atlassian.net/secure/useravatar?size=medium&ownerId=jeff.richards&avatarId=16100"
#           },
#           "displayName": "Jeff Richards (TT)",
#           "active": true,
#           "timeZone": "America/Chicago"
#       },
#       "subtasks": [

#       ],
#       "reporter": {
#           "self": "https://tradingtech.atlassian.net/rest/api/2/user?username=jeff.richards",
#           "name": "jeff.richards",
#           "key": "jeff.richards",
#           "emailAddress": "Jeff.Richards@tradingtechnologies.com",
#           "avatarUrls": {
#               "48x48": "https://tradingtech.atlassian.net/secure/useravatar?ownerId=jeff.richards&avatarId=16100",
#               "24x24": "https://tradingtech.atlassian.net/secure/useravatar?size=small&ownerId=jeff.richards&avatarId=16100",
#               "16x16": "https://tradingtech.atlassian.net/secure/useravatar?size=xsmall&ownerId=jeff.richards&avatarId=16100",
#               "32x32": "https://tradingtech.atlassian.net/secure/useravatar?size=medium&ownerId=jeff.richards&avatarId=16100"
#           },
#           "displayName": "Jeff Richards (TT)",
#           "active": true,
#           "timeZone": "America/Chicago"
#       },
#       "aggregateprogress": {
#           "progress": 0,
#           "total": 0
#       },
#       "customfield_13704": "2016-10-06T08:30:00.000-0500",
#       "customfield_13706": "2016-10-21T17:53:00.000-0500",
#       "customfield_13705": "2016-10-08T10:30:00.000-0500",
#       "progress": {
#           "progress": 0,
#           "total": 0
#       },
#       "votes": {
#           "self": "https://tradingtech.atlassian.net/rest/api/2/issue/DEB-49013/votes",
#           "votes": 0,
#           "hasVoted": false
#       },
#       "worklog": {
#           "startAt": 0,
#           "maxResults": 20,
#           "total": 0,
#           "worklogs": [

#           ]
#       },
#       "issuetype": {
#           "self": "https://tradingtech.atlassian.net/rest/api/2/issuetype/4",
#           "id": "4",
#           "description": "An improvement or enhancement to an existing feature or task.",
#           "iconUrl": "https://tradingtech.atlassian.net/secure/viewavatar?size=xsmall&avatarId=14910&avatarType=issuetype",
#           "name": "Improvement",
#           "subtask": false,
#           "avatarId": 14910
#       },
#       "timespent": null,
#       "project": {
#           "self": "https://tradingtech.atlassian.net/rest/api/2/project/12602",
#           "id": "12602",
#           "key": "DEB",
#           "name": "Debesys",
#           "avatarUrls": {
#               "48x48": "https://tradingtech.atlassian.net/secure/projectavatar?pid=12602&avatarId=12700",
#               "24x24": "https://tradingtech.atlassian.net/secure/projectavatar?size=small&pid=12602&avatarId=12700",
#               "16x16": "https://tradingtech.atlassian.net/secure/projectavatar?size=xsmall&pid=12602&avatarId=12700",
#               "32x32": "https://tradingtech.atlassian.net/secure/projectavatar?size=medium&pid=12602&avatarId=12700"
#           },
#           "projectCategory": {
#               "self": "https://tradingtech.atlassian.net/rest/api/2/projectCategory/10600",
#               "id": "10600",
#               "description": "",
#               "name": "ENG"
#           }
#       },
#       "aggregatetimespent": null,
#       "resolutiondate": null,
#       "workratio": -1,
#       "watches": {
#           "self": "https://tradingtech.atlassian.net/rest/api/2/issue/DEB-49013/watchers",
#           "watchCount": 0,
#           "isWatching": false
#       },
#       "created": "2016-09-21T09:23:16.703-0500",
#       "updated": "2016-10-26T10:38:01.698-0500",
#       "timeoriginalestimate": null,
#       "description": "Need to perform some validation of AOTC in the dev environment, loadbalancing, performance and book management.\r\n\r\nThis jira is to cover any code that may need to be written has well as the time it will take.\r\n",
#       "customfield_10010": [
#           "com.atlassian.greenhopper.service.sprint.Sprint@10c576b[id=2239,rapidViewId=63,state=CLOSED,name=Sprint 116 OC,goal=,startDate=2016-09-21T10:48:04.322-05:00,endDate=2016-09-28T10:48:00.000-05:00,completeDate=2016-09-28T10:38:34.868-05:00,sequence=2239]",
#           "com.atlassian.greenhopper.service.sprint.Sprint@1eb4ad0[id=2262,rapidViewId=63,state=CLOSED,name=Sprint 117 OC,goal=,startDate=2016-09-28T10:48:46.011-05:00,endDate=2016-10-05T10:48:00.000-05:00,completeDate=2016-10-05T10:38:15.375-05:00,sequence=2262]",
#           "com.atlassian.greenhopper.service.sprint.Sprint@1bef548[id=2306,rapidViewId=63,state=CLOSED,name=Sprint 118 OC,goal=,startDate=2016-10-05T10:45:24.090-05:00,endDate=2016-10-12T10:45:00.000-05:00,completeDate=2016-10-12T10:40:10.360-05:00,sequence=2306]",
#           "com.atlassian.greenhopper.service.sprint.Sprint@5831c7[id=2328,rapidViewId=63,state=CLOSED,name=Sprint 119 OC,goal=,startDate=2016-10-12T10:51:38.831-05:00,endDate=2016-10-19T10:51:00.000-05:00,completeDate=2016-10-19T10:39:19.776-05:00,sequence=2328]",
#           "com.atlassian.greenhopper.service.sprint.Sprint@1628ea8[id=2333,rapidViewId=63,state=CLOSED,name=Sprint 120 OC,goal=,startDate=2016-10-19T10:44:19.044-05:00,endDate=2016-10-26T10:44:00.000-05:00,completeDate=2016-10-26T10:38:00.828-05:00,sequence=2333]",
#           "com.atlassian.greenhopper.service.sprint.Sprint@76ef1e[id=2362,rapidViewId=63,state=ACTIVE,name=Sprint 121 OC,goal=,startDate=2016-10-26T10:45:32.107-05:00,endDate=2016-11-02T10:45:00.000-05:00,completeDate=<null>,sequence=2362]"
#       ],
#       "customfield_15700": "",
#       "customfield_10006": "9223372036854775807",
#       "customfield_10801": "Not started",
#       "attachment": [

#       ],
#       "summary": "Test and validate AOTC",
#       "customfield_14200": "eurex_otc:678.0.0,ice:762.0.0,btec:381.0.0,kcg:623.0.0,cme:798.0.0,ndaq_eu:372.0.0,nfx:626.0.0,cfe:735.0.0,sgx_titan:280.0.0,eex_derivative_otc:677.0.0,espeed:725.0.0,lme:100.0.0,euronext:60.0.0,eex_derivative:729.0.0,sgx:287.0.0,cme_otc:164.0.0,ice_l:542.0.0,fex:319.0.0,eris:695.0.0,order_connector:582.0.0,asx:623.0.0,asx_ntp:197.0.0,dgcx:191.0.0,eurex:740.0.0,bankalgo:612.0.0,exchange_compliance:126.0.0",
#       "customfield_10004": 2,
#       "environment": null,
#       "duedate": null,
#       "comment": {
#           "comments": [

#           ],
#           "maxResults": 0,
#           "total": 0,
#           "startAt": 0
#       }
#   }
#

