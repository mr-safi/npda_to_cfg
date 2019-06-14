from sm import PDA ,CFG
filename = 'in.txt'
file = open(filename, 'r')
lines = file.readlines()
file.close()
pda = PDA()
cfg = CFG ()

pda.construct_pda_from_file(lines)
# part 1
filename2 = 'out.txt'
wrfile = open(filename2 ,'w+')
cfg.convert_from_pda(pda , wrfile)

