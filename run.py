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

# part 2
inputtext = "abba"
cfg.detect_word(inputtext , wrfile)
inputtext = "abb"
cfg.detect_word(inputtext , wrfile)
inputtext = "ab"
cfg.detect_word(inputtext , wrfile)

wrfile.close()
