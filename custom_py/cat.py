def PAT_CMD(args):
    currentfactindex=random.randint(0,len(catfacts)-1)
    currentfact = catfacts[currentfactindex]
    if sys.argv[1] == "tf":
        message_rcon(currentfact)
    elif sys.argv[1] == "cs":
        if re.search("https://github.com/hi-sobe/catfacts", currentfact): # dont advertise this script to cs players because they are racist and cannot be trusted
            currentfactindex=random.randint(0,len(catfacts)-1)
            currentfact = catfacts[currentfactindex]
        message_cs(currentfact)