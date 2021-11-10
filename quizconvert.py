import re  # we use regex

unit = 1
baseCat = 'IPM Quiz '+ str(unit)

#escaping special characters
def special(x):
    spec = ['~', '=', '#', '{', '}']
    for i in spec:
        if x.find(i) !=-1:
            x =x.replace(i, '\\'+i)
    return x

#setup our file i/o with req encoding
read = open("quiz.txt", 'r', encoding="utf8")
write = open("output.txt", 'w', encoding='utf-8')

#setup our initial category/header, question counter, and split between Q and A.
buf = '$CATEGORY: '+baseCat +'\n\n'
qcount = 1 #question number, start at 1
qastate = 0 #are we done with the Q and moving to the A; 0=Q, 1=A
qtype = '' #initialize type of q

#each line is part of a question, an answer, or a transition, so we process each in turn
for x in read:
    if x.startswith('Category'): #line starts a new category
        buf = buf + '$CATEGORY: '+baseCat+ '/'+ x.split(': ')[1]+'\n' 

    elif x.startswith('TYPE:'): #line starts a new Q
        #set q type
        qtype = x.split(':', 1)[1][0:2]

        #now get the q writing
        buf = buf + '::IPMQuiz' + str(unit) + '-' + str(qcount)+ '::'+ special(x.split(':', 1)[1][3:])

    elif x.startswith('@@'): #line signals transition from Q to A
        qastate = 1
        if qtype == 'NM':
            buf = buf + '{#\n'
        elif qtype == 'TF':
            buf = buf
        else:
            buf = buf + '{\n'
    
    elif x.startswith('\n'):#blank line=close out question, insert blank line, increment q count
        if qtype == 'TF':
            buf = buf + '\n\n'
        else:
            buf = buf + '}\n\n'  
        qastate = 0
        qcount = qcount+1

    else: #continued Q or A. Write it clean if Q, conditional write if A
        if qastate == 0: #writing Q so just write the line
            if x.startswith('TYPE:'): #first line
                buf = buf + special(x.split(':', 1)[1][3:])
            else: #bonus line
                buf = buf + special(x)
        else: #writing an answer line
            if qtype == 'MC':
                if x.startswith('*'): 
                    buf = buf + '=' + special(x.split(') ', 1)[1]) #regular correct answer, add a = in place of the *
                elif x.startswith('#'):
                    buf = buf + '#' + special(x.split('#', 1)[1]) #comment line, strip the #, add it back plus the remainder so it isn't escaped
                elif re.match('^.*\%[A-Z]\)', x): #percent right or wrong, add ~% to the start
                    buf = buf + '~%' + special(x.split(') ', 1)[0][:-1]) + special(x.split(') ', 1)[1])
                elif re.match('^[A-Z]\)', x): #regular incorrect answer, add ~ to start
                    buf = buf + '~' + special(x.split(') ', 1)[1])
                else: #continued answer line
                    buf = buf + special(x)

            elif qtype == 'MR': #either a % line or a continued line
                if re.match('^.*\%[A-Z]\)', x): #% line
                    buf = buf + '~%' + special(x.split(') ', 1)[0][:-1]) + special(x.split(') ', 1)[1])
                else: #continued line
                    buf = buf + special(x)

            elif qtype == 'TF': #just write t or f
                if x.startswith('TRUE'):
                    buf = buf + '{T}'
                else:
                    buf = buf + '{F}'
            
            elif qtype == 'MA': #need to swap out = for arrow and add = to start
                buf = buf + '=' + special(x.split('=', 1)[0]) + ' ->' + special(x.split('=', 1)[1])
            
            elif qtype == 'NM': #either starts with a percent or does not
                if re.match('^.*%', x):
                    buf = buf + '=%' + special(x)
                else:
                    buf = buf + '=' + special(x)

            else: #qtype wrong? we have an error
                buf = 'error in qtype'
                break

#now we close out the quiz, print it to our output file, and close our files
buf = buf + '\n}'
write.write(buf)
read.close()
write.close()