# LL(1) parser
 implement the LL(1) parsing table for any given grammar then check whether the input string belongs to the language or not.
 
 ## input files:
 ### 1. ﬁrst input ﬁle 
  * will contain the grammar and the ﬁrst & follow.
  * format: non terminal colon set of production rules then colon first then colon follow.
  * Example:
   A : B c | D a c | epsilon : a b ( + : $ + b
  
 ### 2. second input ﬁle 
  * the second input ﬁle will contain the input to be parsed .

 ## output files:
 ### 1. ﬁrst output ﬁle 
  * will contain text representation of the parsing table if the grammar is valid ll(1) grammar, 
  contain "invalid LL(1) grammar" if invalid grammar.
  
 ### 2. second output ﬁle 
  * will contain "yes" if  input string belongs to the language, contain "no" if not .
 
##### How to run:-

   from command line:
   python "script_name" --grammar "grammar file name" --input "input file name"

   Example:
   python LL(1)_parser.py --grammar ll1sample01_grammar.txt --input ll1sample01_input.txt