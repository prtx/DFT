# -*- coding: utf-8 -*-


import argparse
import pdb
#import networkx as nx
import math
import time
from random import randint

from circuit import Circuit
from modelsim_simulator import Modelsim

import sys
sys.path.insert(1, "../data/netlist_behavioral")
from c432_logic_sim import c432_sim
import config
from checker_logicsim import *
from regular_tp_gen import *
#from checker_dfs import *
from fault_sim import *
from deductive_fs import DFS
from d_alg import *


import os

def check_gate_netlist(circuit, total_T=1):

    for t in range(total_T):
        PI_dict = dict()
        PI_list = []
        
        PI_num = [x.num for x in circuit.PI]
        for pi in PI_num:
            val = randint(0,1)
            PI_dict["in" + str(pi)] = val
            PI_list.append(val)

        res_beh = c432_sim(PI_dict)
        circuit.logic_sim(PI_list)
        res_ckt = circuit.read_PO()
        if res_beh != res_ckt:
            print("Wrong")
            return False
    print("all test patterns passed")
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-ckt", type=str, required=True, help="circuit name, c17, no extension")
    parser.add_argument("-tp", type=int, required=False, help="number of tp for random sim")
    parser.add_argument("-cpu", type=int, required=False, help="number of parallel CPUs")
    args = parser.parse_args()

    print("\n======================================================")
    print("Run | circuit: {} | Test Count: {} | CPUs: {}".format(args.ckt, args.tp, args.cpu))
    print("======================================================\n")

    #Ting-Yu
    
    # for c in ['c17','c432','c499','c880','c1355','c1908','c2670','c3540','c5315','c6288','c7552']:
    #     checker = Checker(c, args.tp)
    #     if checker.check_PI_PO() == False:
    #         print('#################################')
    #         continue
    #     checker.modelsim_wrapper()
    #     checker.check_ckt_verilog('verilog')
    #     checker.check_ckt_verilog('ckt')
    #     print('#################################')
    # #exit()
    

    # circuit = Circuit(args.ckt)
    # circuit.read_verilog()
    # # circuit.read_ckt()
    # circuit.lev()

    """ Testing DFS """
    print("DFS starts")
    # dfs = DFS(circuit)
    # # for i in range(1, 11):
    # #     dfs.fs_exe_golden(tp_num=1, t_mode='rand', no=i, r_mode='b')
    
    # dfs.fs_exe(tp_num=args.tp, t_mode='rand', r_mode='b')
    # print(dfs.return_rest_fault())

    """ Testing D alg """
    print("*****************************************************")
    print("***********        START D-ALG         **************")
    print("*****************************************************")
    
    circuit = Circuit(args.ckt)
    # circuit.read_verilog()
    circuit.read_ckt()
    circuit.lev()
    d_alg = D_alg(circuit, '6', 0)
    if d_alg.dalg() == True:
        IPI_list = d_alg.return_IPI()
    else:
        print("Not found!!")
    # ignore all print()!!!!!!!!!
    # old_stdout = sys.stdout # backup current stdout
    # sys.stdout = open(os.devnull, "w")

    # sys.stdout = old_stdout # reset old stdout


    """
    for ckt in ['c1']:
        circuit = Circuit(ckt)
        LoadCircuit(circuit, "ckt")
        # circuit.read_verilog()
        circuit.lev()
        # in fault: ('14',0): node 14 SA0
        # but we need to gives D to the node in dalg!!!!!!!!!!!!!!!!!!############
        for fault in [('6', 0)]:
            print("******************* start DALG at ", fault, " *************************")
            d_alg = D_alg(circuit, fault[0], fault[1])
            # fault_val = 1: 1^12=D'    fault_val = 0: 0^12=D
            ######################## needs to be changed!!!! put in dalg!!!!!!
            # if fault[1] == 1:
            #     fault_val = 15
            # else:
            #     fault_val = 0
            # fault_val = fault_val ^ 12
            ###########################################
            if d_alg.dalg() == True:
                IPI_list = d_alg.return_IPI()
                IPI_binary_list = []
                for x in IPI_list:
                    if x == 9 or x == 15 or x == 12:
                        IPI_binary_list.append(1)
                    else:
                        IPI_binary_list.append(0)
                    # if x == 9 or x == 0 or x == 3:
                    #     IPI_binary_list.append(0)
                    # else:
                    #     IPI_binary_list.append(1)
                dfs_test = DFS(circuit)
                fault_list = dfs_test.single(IPI_binary_list)
                
                print('fault >> ',fault)
                print('D_alg generates input pattern >> ',IPI_binary_list)
                print('fault_list >> ', fault_list)
                if fault in fault_list:
                    print('result is correct')
                else:
                    print('result is not correct')
            else:
                print('can not find test')
    """
    """
    # for ckt in ['c499','c432']:     
    # for ckt in ['c1', 'c2', 'c3', 'FA', 'FA_NAND', 'add2']:
    for ckt in ['c1']:
        print("******************* start DALG at ", ckt, " *************************")
        circuit = Circuit(ckt)
        LoadCircuit(circuit, "ckt")
        circuit.lev()
        flag = 0
        total_fault_list = []
        for node in circuit.nodes_lev:
            total_fault_list.append((node.num,0))
            total_fault_list.append((node.num,1))
        
        #print(total_fault_list)
        
        #total_fault_list = [('N4-1',1)]
        #default
        # podem = Podem(circuit, 'N1', 0)#TODO
        # d_alg = D_alg(circuit, fault[0], fault[1])
        i = 0
        #seed(1)
        list_not_correct = []
        list_no_test = []    
        for fault in total_fault_list:
        #while(i<20):
            #print(len(total_fault_list))

            #index = randint(0,len(total_fault_list)-1)
            #print('start',index)
            #fault = total_fault_list[index]
            #print(fault)
            
            
            # ignore all print()!!!!!!!!!
            # old_stdout = sys.stdout # backup current stdout
            # sys.stdout = open(os.devnull, "w")

            # podem.reset_and_get_fault(fault[0], fault[1])#TODO
            print("******************* start DALG at ", fault, " *************************")
            d_alg = D_alg(circuit, fault[0], fault[1])
            if d_alg.dalg() == True:
                # sys.stdout = old_stdout # reset old stdout

                IPI_list = d_alg.return_IPI()
                IPI_binary_list = []
                #print(IPT_list)
                for x in IPI_list:
                    if x == 15 or x == 12 or x == 9: 
                        IPI_binary_list.append(1)
                    else:
                        IPI_binary_list.append(0)

                #print(IPT_binary_list)
                dfs_test = DFS(circuit)
                fault_list = dfs_test.single(IPI_binary_list)
                #print('fault >> ',fault)
                #print('fault_list >> ', fault_list)
                if fault in fault_list:
                    # print('result is correct')
                    pass
                else:
                    list_not_correct.append(fault)
                    print('result is not correct')
                    #print(fault)
                    #print(IPT_binary_list)
                    #print(fault_list)
                    flag = 1
            else:
                # sys.stdout = old_stdout # reset old stdout
                #print(fault)
                #print(IPT_binary_list)
                list_no_test.append(fault)
                print('############can not find test##############')
            # print(podem.count)
            # podem.count = 0
            #print('#########################')
            i += 1
        print('###############################################')
        
        if flag == 1:
            print('result is not correct')
        else:
            print('result is correct')
        print('list_not_correct >>',list_not_correct)
        print('list_no_test >>',list_no_test)
        print(len(list_no_test))
    """
    exit()




def parallel_graph():
    netlists = ["c17", "c432", "c499", "c880", "c1355", "c1908", "c2670",
            "c3540", "c5315", "c6288", "c7552"]

if __name__ == "__main__":
    main()