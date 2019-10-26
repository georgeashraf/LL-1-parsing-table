# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 17:31:08 2019

@author: Lenovo
"""
import itertools
import argparse
import pandas as pd 
import matplotlib.pyplot  as plt
from pandas.plotting import table as tbl
def table(rules,first,follow):
    ll1={}
    for key,value in rules.items():
        for i in value:  
          if i[0] =='epsilon':
                fol=follow[key]
                for j in fol:
                  if (key,j) not in ll1.keys():  
                    ll1[(key,j)]=i[0]
                  else:
                      return
                break
          else:  
              for ii in i: 
                if ii in rules.keys():
                  f=first[ii]
                  for j in f:
                     if (key,j) not in ll1.keys(): 
                         ll1[(key,j)]=i
                     else:
                         return
                  if i.index(ii)==len(i)-1 and 'epsilon' in f:  
                      fol=follow[key]
                      for j in fol:
                         if (key,j) not in ll1.keys(): 
                             ll1[(key,j)]=i 
                         else:
                             return
                      break
                  if 'epsilon' not in f:
                      break
    
                elif ii in terminals :
                     if (key,i[0]) not in ll1.keys(): 
                        ll1[(key,i[0])]=i
                        break
                     else:
                         return
    #print(ll1)        
    return ll1        
     
        
def trace(user_input,parsingTable,start_symbol):
	flag = 0
	#appending dollar to end of input
	user_input .append( "$")
	stack = []	
	stack.append("$")
	stack.append(start_symbol)
	input_len = len(user_input)
	index = 0
	while len(stack) > 0:
		#element at top of stack
		top = stack[len(stack)-1]
		#current input
		current_input = user_input[index]
		if top == current_input:
			stack.pop()
			index = index + 1	
		else:	
			#finding value for key in table
			key = (top , current_input)
			#top of stack terminal => not accepted
			if key not in parsingTable.keys():
				flag = 1		
				break
			value = parsingTable[key]
			if value !='epsilon':
				value = value[::-1]
				value = list(value)				
				#poping top of stack
				stack.pop()
				#push value chars to stack
				for element in value:
					stack.append(element)
			else:
				stack.pop()		
	if flag == 0:
		return True
	else:
		return False



def visualize(ll1_table,rules):
    non_terminals=[]
    terminals=[]
    for k in rules:
        non_terminals.append(k)
    for key,val in rules.items():
        for i in val:
            for ii in i:
                if (ii not in non_terminals) and (ii not in terminals) and (ii !="epsilon"):
                    terminals.append(ii)
    terminals.append("$")                
    df_ = pd.DataFrame(index=non_terminals, columns=terminals)
    df_ = df_.fillna("") 
    for k,val in ll1_table.items():
        if val!= "epsilon":
           li = ' '.join(map(str, val)) 
        else:
           li="epsilon" 
        df_.at[k[0], k[1]] = li
    # set fig size
    fig, ax = plt.subplots(figsize=(12, 7)) 
    # no axes
    ax.xaxis.set_visible(False)  
    ax.yaxis.set_visible(False)  
    # no frame
    ax.set_frame_on(False)  
    # plot table
    tab = tbl(ax, df_, loc='center',colWidths=[0.1 for x in terminals])  
    # set font manually
    tab.auto_set_font_size(False)
    tab.set_fontsize(12) 
    # save the result
    tab.scale(1,2)
    plt.savefig('table.png')
if __name__ == '__main__':
        
  parser = argparse.ArgumentParser(add_help=True, description='Sample Commandline')

  parser.add_argument('--grammar', action="store", help="path of file to take as input to read grammar", nargs="?", metavar="dfa_file")
  parser.add_argument('--input', action="store", help="path of file to take as input to test strings on LL table", nargs="?", metavar="input_file")
    
  args = parser.parse_args()
  rules={}
  first={}
  follow={}
  with open(args.grammar, mode='r', encoding='utf-8-sig') as file:
        first_line = file.readline()
        start=first_line[0]
  with open(args.grammar, mode='r', encoding='utf-8-sig') as file:
       for line in file:
          x=line.split(':')
          fi=x[2].strip()
          first[x[0].strip(' ')]=fi.split(' ')
          fo=x[3].strip()
          follow[x[0].strip(' ')]=fo.split(' ')
          y=x[1]
          z=y.split('|')
          l=[]
          for i in z:
                p=i.strip('\n')
                j=[p]
                l.append(j)
          kk=x[0].strip(' ')  
          rules[kk]=l
    
  for k, v in rules.items():
                li=[]
                for o in v:
                    l=[]
                    if o[0] !=" epsilon":
                        j=o[0].split(' ')
                        for jj in j:
                            if jj!='':
                                l.append(jj)
                        li.append(l)
                    else: 
                       str1= o[0].strip(' ')
                       li.append([str1])
                rules[k]=li    
    
  terminals=[]
  for k,v in rules.items():
        for i in v:
            for ii in i:
                if ii not in terminals and ii not in rules.keys():
                    terminals.append(ii)
  table=table(rules,first,follow)
  M=args.grammar.split('_')[0]
  if table is None:
      output_file=open(M+"_table.txt","w+")
      output_file.write("invalid LL(1) grammar")
      output_file.close()
  else:
      output_file=open(M+"_table.txt","w+")
      t=list( set(terminals)-{"epsilon"} )
      t.append("$")
      c = list(itertools.product(rules.keys(), t))
      for i in c:
          if i not in table.keys():
            for ii in i:  
              output_file.write(ii+" : ")
            output_file.write("\n")
          else:
            for iii in i : 
              output_file.write(iii+" : ")
             
            if table[i] !="epsilon" :   
                for j in  table[i]:   
                   output_file.write(j+" ")
                output_file.write("\n")
            else:
                output_file.write("epsilon")
                output_file.write("\n")
      output_file.close()
      vis= visualize(table,rules)
      with open(args.input, mode='r', encoding='utf-8-sig') as file:
         for line in file:
             a=line
         parsing=a.strip()
         parsing=parsing.split(' ')
      trace=trace(parsing,table,start)
      N=args.input.split('_')[0]
      if trace==True:
                output_file=open(N+"_output.txt","w+") 
                output_file.write("Yes")
                output_file.close()
      else:
                output_file=open(N+"_output.txt","w+") 
                output_file.write("No")
                output_file.close()

 

          