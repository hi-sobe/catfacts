if not "schrodinger_state" in globals():
	schrodinger_state=False #cat die lol
if not "schrodinger_first" in globals():
	schrodinger_first=True
def PAT_CMD(args):
	global schrodinger_state
	global schrodinger_first
	schrodinger_first=True
	console_log("Unrolled Schroedinger cat state")
	random.seed(time.time()*1000)