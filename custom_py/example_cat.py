## script has access to ALL global variables from main script!!
## table catfacts and message_ functions do not need to be defined

# pattern to trigger: #CMDSTRING!cat
# #CMDSTRING is replaced with either ": !" or ":  !", depending on if script was launched with tf or cs argument

def PAT_CMD(args):
    currentfactindex=random.randint(0,len(catfacts)-1)
    currentfact = catfacts[currentfactindex]
    if sys.argv[1] == "tf":
        message_rcon(currentfact)
    elif sys.argv[1] == "cs":
        if re.search("https://github.com/hi-sobe/catfacts", currentfact):
            currentfactindex=random.randint(0,len(catfacts)-1)
            currentfact = catfacts[currentfactindex]
        message_cs(currentfact)