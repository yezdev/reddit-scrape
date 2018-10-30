import requests



# demo Requests
def demoRequestsGet():
    r = requests.get("http://reddit.com/.json")
    print(r.status_code)
    print(r.headers)
    print(r.text)
    for i in r.json()['data']['children']:
        print(i['data']['title'])


# demo requests passing a form
def demoRequestsPost():
    r = requests.post('http://httpbin.org/post',data = {'key':'value'})
    print(r.text)



import requests.auth



# obtain reddit token
def getRedditToken():
    client_auth = requests.auth.HTTPBasicAuth('USER_AUTH','PASS_AUTH')
    post_data = {"grant_type" : "password", "username" : "USERNAME", "password" : "PASSWORD"}
    headers = {"User-Agent": "APPLICATION_NAME"}
    response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data = post_data,headers=headers)
    return(response.json())


# get reddit user details from obtained token
def getRedditUserDetails(token):
    url = "https://oauth.reddit.com/api/v1/me"
    headers = {"Authorization":"bearer " + token, "User-Agent":"APPLICATION_NAME"}
    response = requests.get(url,headers=headers)
    return(response.json())


token = getRedditToken()
access_token = token['access_token']


# returns html doctype tag
def doctype():
  return "<!DOCTYPE html>\n"

# returns html, head, and title tags
def title(titlestring):
  return "<html>\n<head>\n<title>" + titlestring + "\n</title>\n</head>\n"

# returns html table headers
def tableheader(param):
  row = "<tr>\n"
  for item in param:
    row += "<th>"+item+"</th>\n"
  row += "</tr>\n"
  return row

# returns html table row tags and data
def tablerow(data):
  row = "<tr>\n"
  for item in data:
    row += "<td>"+str(item)+"</td>\n"
  row += "</tr>\n"
  return row


# returns html file of search results
def my_search(token, subreddit, thing):
    url = "https://oauth.reddit.com/r/" + subreddit + "/search?q="+thing+"&restrict_sr=on"
    headers = {"Authorization": "bearer " + token, "User-Agent": "APPLICATION_NAME"}
    response = requests.get(url, headers=headers)

    outfile = open("results.html",'w')

    s = doctype() + title("Results for "+thing)
    s += "<body>\n"
    s += '<table style="width:100%">\n'
    
    titles = []
    titles.append("Title")
    titles.append("url")
    titles.append("author")
    titles.append("date")
    titles.append("upvotes")

    s += tableheader(titles)

    children = response.json()['data']['children']

    for child in children:
        row = []
        row.append(child['data']['title'])
        row.append(child['data']['url'])
        row.append(child['data']['author'])
        row.append(child['data']['created'])
        row.append(child['data']['ups'])
        s += tablerow(row)
    
    s += "</table>\n"
    s += "</body>\n"
    s += "</html>"
    
    outfile.write(s)
    outfile.close()



# call the search function
my_search(access_token,"Showerthoughts","funny")