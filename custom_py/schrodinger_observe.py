if not "schrodinger_state" in globals():
	schrodinger_state=False #cat die lol
if not "schrodinger_first" in globals():
	schrodinger_first=True
if not "schrodinger_lives" in globals():
	schrodinger_lives=0
if not "schrodinger_deads" in globals():
	schrodinger_deads=0
def PAT_CMD(args):
	global schrodinger_first
	global schrodinger_state
	global schrodinger_lives
	global schrodinger_deads
	if schrodinger_first == True:
		if random.randint(0,99)>=50:
			schrodinger_state=True
			schrodinger_lives+=1
		else:
			schrodinger_state=False
			schrodinger_deads+=1
		console_log("Rolled Schrodinger cat state")
		schrodinger_first = False
	cat_message("Schrodinger's cat is: " + ((schrodinger_state==True and "ALIVE!") or "DEAD!"))
	cat_message(str(schrodinger_lives)+"/"+str(schrodinger_deads))