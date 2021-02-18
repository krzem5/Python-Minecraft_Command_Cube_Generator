import clipboard
import random



INIT_CMD="summon falling_block ~ ~1 ~ {Time:1,BlockState:{Name:\"minecraft:redstone_block\"},Passengers:[{id:armor_stand,Health:0,Passengers:[{id:\"minecraft:falling_block\",Time:1,BlockState:{Name:\"minecraft:activator_rail\"},Passengers:[%s{id:\"minecraft:command_block_minecart\",Command:\"setblock ~ ~-2 ~ air\"},{id:\"minecraft:command_block_minecart\",Command:\"setblock ~ ~-2 ~ command_block[facing=up]\"},{id:\"minecraft:command_block_minecart\",Command:\"setblock ~ ~1 ~ command_block{auto:1,Command:\\\"fill ~ ~ ~ ~ ~-2 ~ air\\\"}\"},{id:\"minecraft:command_block_minecart\",Command:\"kill @e[type=command_block_minecart,distance=..1]\"}]}]}]}"
INIT_CMD_LAST="summon falling_block ~ ~1 ~ {Time:1,BlockState:{Name:\"minecraft:redstone_block\"},Passengers:[{id:armor_stand,Health:0,Passengers:[{id:\"minecraft:falling_block\",Time:1,BlockState:{Name:\"minecraft:activator_rail\"},Passengers:[%s{id:\"minecraft:command_block_minecart\",Command:\"setblock ~ ~1 ~ command_block{auto:1,Command:\\\"fill ~ ~ ~ ~ ~-3 ~ air\\\"}\"},{id:\"minecraft:command_block_minecart\",Command:\"kill @e[type=command_block_minecart,distance=..1]\"}]}]}]}"
CMD="{id:\"minecraft:command_block_minecart\",Command:\"%s\"},"
ID_CHARS="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"
ID_LEN=16
CMD_X_OFF=2
MAX_CMD_LEN=32500



def rand_id(x=ID_LEN):
	return "".join([ID_CHARS[random.randint(0,len(ID_CHARS)-1)] for _ in range(0,x)])



def generate(init,main,delete):
	def _next(x,xa,y,z,za,d):
		x+=xa
		if (xa==1 and x==sz-1):
			d=("south" if za==1 else "north")
		elif (xa==1 and x==sz):
			d="west"
			xa=-1
			x=sz-1
			z+=za
		elif (xa==-1 and x==0):
			d=("south" if za==1 else "north")
		elif (xa==-1 and x==-1):
			d="east"
			xa=1
			x=0
			z+=za
		if (za==1 and z==sz-1 and ((xa==1 and x==sz-1) or (xa==-1 and x==0))):
			d="up"
		elif (za==1 and z==sz):
			z=sz-1
			za=-1
			y+=1
			x=min(max(x,0),sz-1)
		elif (za==-1 and z==0 and ((xa==1 and x==sz-1) or (xa==-1 and x==0))):
			d="up"
		elif (za==-1 and z==-1):
			z=0
			za=1
			y+=1
			x=min(max(x,0),sz-1)
		return [x,xa,y,z,za,d]
	ol=init
	x=0
	xa=1
	y=0
	z=0
	za=1
	d="east"
	t="repeating"
	l=len(main)+len(delete)+2
	sz=round(l**(1/3)*10**5)/10**5
	if (int(sz)**3!=l):
		sz=int(sz)+1
	else:
		sz=int(sz)
	ol=init[:]
	for i,k in enumerate(main):
		k=k.replace("\\","\\\\").replace("\"","\\\"")
		ol+=[f"setblock ~{x+CMD_X_OFF} ~{y-2} ~{z} {t}_command_block[facing={d}]{{auto:1b,Command:\"{k}\"}}"]
		t="chain"
		x,xa,y,z,za,d=_next(x,xa,y,z,za,d)
	t=""
	a=[x+0,xa+0,y+0,z+0,za+0,d+""]
	nxa,_,nya,nza,_,_=_next(*a)
	nxb,_,nyb,nzb,_,_=_next(*_next(*a))
	for i,k in enumerate(delete+[f"fill ~{-nxa-1} ~{-nya} ~{-nza} ~{-nxa-1} ~{-nya} ~{-nza+1} air",f"fill ~{-nxb} ~{-nyb} ~{-nzb} ~{-nxb+sz} ~{-nyb+sz} ~{-nzb+sz} air"]):
		k=k.replace("\\","\\\\").replace("\"","\\\"")
		ol+=[f"setblock ~{x+CMD_X_OFF} ~{y-2} ~{z} {t}command_block[facing={d}]{{auto:{('0' if len(t)==0 else '1')}b,Command:\"{k}\"}}"]
		if (len(t)==0):
			ol=[f"fill ~{x+CMD_X_OFF} ~-2 ~ ~{x+CMD_X_OFF+sz-1} ~{sz-3} ~{sz-1} air",f"fill ~{CMD_X_OFF-1} ~-2 ~ ~{CMD_X_OFF-1} ~-2 ~1 air",f"setblock ~{CMD_X_OFF-1} ~-2 ~ dark_oak_wall_sign[facing=west]{{Text1:\"{{\\\"text\\\":\\\"===============\\\",\\\"clickEvent\\\":{{\\\"action\\\":\\\"run_command\\\",\\\"value\\\":\\\"data merge block ~{x+1} ~{y} ~{z} {{auto:1b}}\\\"}},\\\"bold\\\":true,\\\"color\\\":\\\"gray\\\"}}\",Text2:\"{{\\\"text\\\":\\\"Remove\\\",\\\"color\\\":\\\"blue\\\"}}\",Text3:\"{{\\\"text\\\":\\\"Structure\\\",\\\"bold\\\":true,\\\"color\\\":\\\"dark_red\\\"}}\",Text4:\"{{\\\"text\\\":\\\"===============\\\",\\\"bold\\\":true,\\\"color\\\":\\\"gray\\\"}}\"}}"]+ol
		t="chain_"
		x,xa,y,z,za,d=_next(x,xa,y,z,za,d)
	o=[""]
	for k in ol:
		k=k.replace("\\","\\\\").replace("\"","\\\"")
		if (len(o[-1])+len(CMD%(k))+len(INIT_CMD)>=MAX_CMD_LEN):
			o+=[""]
		o[-1]+=CMD%(k)
	return [(INIT_CMD if i<len(o)-1 else INIT_CMD_LAST)%(o[i]) for i in range(0,len(o))]



print(generate(["say Init!"],["say Main!"],["say Delete!"]))
