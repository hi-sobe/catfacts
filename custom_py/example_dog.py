## script has access to ALL global variables from main script!!
## dependencies and cat_message() function do not need to be defined

# pattern to trigger is defined in example_dog.txt: #CMDSTRING!dog
# #CMDSTRING is replaced with either ": !" or ":  !", depending on if script was launched with tf or cs argument

if not "catfacts" in globals(): # we only need to define this once
    catfacts = []
    with open('custom_py/kitties', 'r') as file: # this is executed from main script so subdirectory must be specified
        for line in file:
            catfacts.append(line.strip())

def PAT_CMD(args):
    currentfactindex=random.randint(0,len(catfacts)-1)
    currentfact = catfacts[currentfactindex]
    if re.search("https://github.com/hi-sobe/catfacts", currentfact): # try not to advertise github repo /dogfacts because it does not exist
        currentfactindex=random.randint(0,len(catfacts)-1)
        currentfact = catfacts[currentfactindex]
    currentfact = currentfact.replace("cat", "dog")
    currentfact = currentfact.replace("kitten", "puppy")
    currentfact = currentfact.replace("kitty", "puppy")
    currentfact = currentfact.replace("Cat", "Dog")
    currentfact = currentfact.replace("Kitten", "Puppy")
    currentfact = currentfact.replace("Kitty", "Puppy")
    cat_message(currentfact)