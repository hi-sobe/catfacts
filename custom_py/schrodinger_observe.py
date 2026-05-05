if not "schrodinger_state" in globals():
	schrodinger_state=False #cat die lol
if not "schrodinger_first" in globals():
	schrodinger_first=True
def PAT_CMD(args):
	global schrodinger_first
	global schrodinger_state
	if schrodinger_first == True:
		if random.randint(0,99)>=50:
			schrodinger_state=True
		else:
			schrodinger_state=False
		console_log("Rolled Schrodinger cat state")
		schrodinger_first = False
	cat_message("Schrodinger's cat is: " + ((schrodinger_state==True and "ALIVE!") or "DEAD!"))