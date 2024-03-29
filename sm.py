import string
import queue
from util import Queue ,Stack


class PDA:
    def __init__(self):
        self.num_states = 0
        self.states = []
        self.symbols = []
        self.pda_symbols = []
        self.empty_stack_sym = ''
        self.num_accepting_states = 0
        self.accepting_states = []
        self.start_state = 0
        self.transition_functions = []

    def init_states(self):
        self.states = list(range(self.num_states))

    def print_pda(self):
        print(self.num_states)
        print(self.symbols)
        print(self.pda_symbols)
        print(self.empty_stack_sym)

        # print(self.num_accepting_states) #.......
        # print(self.accepting_states) #......
        # print(self.start_state) #........

        for tra in self.transition_functions:
            print(tra)

    def construct_pda_from_file(self, lines):
        self.num_states = int(lines[0])
        self.init_states()

        temp = lines[1].rstrip()
        self.symbols = list(temp.split(","))

        temp = lines[2].rstrip()
        self.pda_symbols = list(temp.split(","))

        temp = lines[3].rstrip()
        self.empty_stack_sym = temp

        for index in range(4, len(lines)):
            temp = lines[index].rstrip()
            temp = temp.replace('q', '')
            transition_func_line = temp.split(",")

            if transition_func_line[0][0:2] == "->":
                transition_func_line[0] = transition_func_line[0][2:]
                self.start_state = int(transition_func_line[0])
            # print(transition_func_line)

            if transition_func_line[0][0] == "*":
                transition_func_line[0] = transition_func_line[0][1:]
                if not self.accepting_states.__contains__(int(transition_func_line[0])):
                    self.accepting_states.append(int(transition_func_line[0]))
                    # self.num_accepting_states += 1

            starting_state = int(transition_func_line[0])
            #
            transition_symbol = transition_func_line[1]
            #
            if transition_func_line[4][0] == "*":
                transition_func_line[4] = transition_func_line[4][1:]
                if not self.accepting_states.__contains__(int(transition_func_line[4])):
                    self.accepting_states.append(int(transition_func_line[4]))
                    # self.num_accepting_states += 1

            pop_elemnt = transition_func_line[2]
            push_elemnt = transition_func_line[3]
            ending_state = int(transition_func_line[4])

            transition_function = (starting_state, transition_symbol, pop_elemnt, push_elemnt, ending_state);
            #
            self.transition_functions.append(transition_function)
            # print(self.accepting_states)


class CFG:

    def __init__(self):
        self.num_states = 0
        self.states = []
        self.symbols = []
        self.pda_symbols = []
        self.empty_stack_sym = ''
        self.num_accepting_states = 0
        self.accepting_states = []
        self.start_state = 0
        self.transition_functions = {}
        self.q = []


    def convert_from_pda(self, pda , file):
        self.symbols = pda.symbols
        self.start_state = pda.start_state
        self.num_states = pda.num_states

        pda_transition_dict = {}
        cfg_transition_dict = {}
        cfg_single_trans_dict = {}

        listBikhod = []

        filename = file
        # file = open(filename, 'w+')

        for transition in pda.transition_functions:
            starting_state = transition[0]
            transition_symbol = transition[1]
            popelement = transition[2]
            pushelement = transition[3]
            ending_state = transition[4]

            if (starting_state, popelement, ending_state) in pda_transition_dict:
                pda_transition_dict[(starting_state, popelement, ending_state)].append((transition_symbol, pushelement))
            else:
                pda_transition_dict[(starting_state, popelement, ending_state)] = [(transition_symbol, pushelement)]

        for cond in pda_transition_dict:
            start_temp = cond[0]  # always fixe
            stack_temp = cond[1]  # always fixe
            ends_temp = str(cond[2])  # always fixe

            for elm in pda_transition_dict.get(cond):
                header_temp = elm[0]
                push_temp = str(elm[-1])
                if push_temp == '_':
                    if cond in cfg_single_trans_dict:
                        cfg_single_trans_dict[cond].append(header_temp)
                    else:
                        cfg_single_trans_dict[cond] = header_temp
                else:
                    for i in range(0, self.num_states):
                        newcond = (start_temp, stack_temp, i)
                        tempRes = "(q" + str(newcond[0]) + newcond[1] + "q" + str(newcond[2]) + ")->"
                        flag2 = True
                        for k in range(0, self.num_states):
                            res = header_temp + "(q" + ends_temp + push_temp[0] + "q" + str(k) + ")(q" + str(k) + \
                                  push_temp[1] + "q" + str(i) + ")"
                            res2 = ("(q" + str(newcond[0]) + newcond[1] + "q" + str(newcond[2]) + ")->" + res)
                            if flag2:
                                listBikhod.append(res)
                                output = tempRes + res
                            else:
                                listBikhod.append(res)
                                output = res
                                if newcond in cfg_transition_dict:
                                    cfg_transition_dict[newcond].append(list(listBikhod))
                                else:
                                    cfg_transition_dict[newcond] = list(listBikhod)
                                listBikhod.clear()

                            if k + 1 != self.num_states:
                                file.write(output + "|")
                            else:
                                file.write(output + "\n")
                            flag2 = False

        templist = []

        for index in cfg_transition_dict:
            if cfg_single_trans_dict.__contains__(index):
                templist.append(cfg_single_trans_dict.get(index))
            for klm in cfg_transition_dict.get(index):
                if (len(klm) > 1 and len(klm) < 10):
                    for itr in klm:
                        templist.append(itr)
                else:
                    templist.append(klm)

            cfg_transition_dict[index] = list(templist)
            templist.clear()

        # ............test
        # print()
        # print(cfg_single_trans_dict)
        # print()
        # print(cfg_transition_dict)

        # for iok in cfg_transition_dict.items():
        #     print(iok)

        self.transition_functions = cfg_transition_dict
        for pe in cfg_single_trans_dict.items():
            # print(pe[1])
            strt = "(q" + str(pe[0][0])
            end = "q" + str(pe[0][2]) + ")"
            stackk = str(pe[0][1])
            res = strt + stackk + end + "->" + pe[1]
            file.write(res + "\n")
            # print(res)

    def detect_word(self, text ,file):

        cf_trans = self.transition_functions
        cfg_trans = {}

        # convert to standard  model
        te = []
        for a in cf_trans:
            for bb in cf_trans.get(a):
                bb = bb.replace("q","")
                bb =  bb.replace(")(" , "),(")
                te.append(bb)
            cfg_trans[a] = list(te)
            te.clear()
        

        #....dfs for find sol
        ways = Stack()
        header = Queue()
        result = []
        whichState = 0
        topstack = '$'
        tempStack =Stack()
        # initialize stack
        for a in text:
             header.push(a)
        
        hed = header.list[0]
        for Cond in cfg_trans:
            if Cond[0] == whichState and Cond[1] == topstack:
                for transAction in cfg_trans.get(Cond):
                    symbol = transAction[0]

                    if hed == symbol:
                        if not ways.list.__contains__(Cond):
                            ways.push(Cond)

        path =""
        level = 0
        seen = True
        decre = 0
        notfond = False
        trceSol =""

        if len(text) ==1 :
            if not ways.isEmpty() :
                print("accept")
                exit(0)
            else:
                print("NO")
                exit(0)
        #..................... main Loop.......................
        while not ways.isEmpty():
            flag = False
            CurrentCond = ways.pop()
            result.append(CurrentCond)

            if seen:
                if decre < len(text):
                    hed = text[decre]
                    decre = decre +1
                else:
                    hed = '_'

            # print("hedd -- ====================================  ",hed ,decre)
            # print("now --------------------- ",CurrentCond)
            # print("ways ",ways.list)
            if ways.isEmpty() :
                path = path.replace("_","")
                if path == text:
                    notfond = False
                    break
                else:
                    notfond = True
                    break
            empty=CurrentCond[1]
            sol = path

            if sol.replace("_","") == text and empty == topstack:
                notfond = False
                trceSol += path+str(CurrentCond) +"=>" +text
                break

            # if not cfg_trans.__contains__(CurrentCond):
            #     if ways.isEmpty():
            #         notfond = True
            #         flag = True
            #         break
            #     else:
            #         CurrentCond = ways.pop()

            seen = False
            for transAction in cfg_trans.get(CurrentCond):
                symbol = transAction[0]

                if symbol == hed :
                    seen = True
                    if not flag :
                        trceSol += path +str(CurrentCond)+"=>"
                        path += hed

                        flag =True

                    if ways.isEmpty():
                        level += 1

                    if len(transAction) > 2 :
                        # path += symbol
                        goSt = transAction[1:]
                        goSt = goSt.split(",")
                        for st in goSt:
                            newCond = int(st[1]) , str(st[2]) ,int(st[3])
                            #  ,,....................pruning Cond.......
                            if not cfg_trans.__contains__(newCond):
                                while not  tempStack.isEmpty():
                                    tempStack.pop()
                                break
                            #  ..........................................
                            tempStack.push(newCond)

                    while not tempStack.isEmpty():
                        t = tempStack.pop()
                        ways.push(t)

            if not seen:
                notfond = True
                break
                # decre +=1

        if notfond:
            file.write("\nInput : "+text)
            file.write("\nOutPut:\nFalse\n")
            # print("Not Accept")
        else:
            # print(trceSol)
            file.write("\nInput : "+text)
            file.write("\nOutPut:\nTrue\n")
            file.write(trceSol+"\n")
            # print("Accept")
