import re  # we need to use regex

unit = 2
baseCat = 'IPY Quiz '+ str(unit) + ' Testing'


#escape special characters
def special(x):
    spec = ['~', '=', '#', '{', '}']
    for i in spec:
        if x.find(i) !=-1:
            x =x.replace(i, '\\'+i)
    return x

#setup our file i/o
read = open("quiz.txt", 'r', encoding="utf8")
write = open("output.txt", 'w', encoding='utf-8')

#setup our initial category/header, question counter, and split between Q and A.
buf = '$CATEGORY: '+baseCat +'\n\n'
c = 1
qasplit = 0 #are we done with the Q and moving to the A

#each line is a question or possible answer (essentially), so let's loop through them and process each by type
for x in read:
    if x.startswith('Category'):
        buf = buf + '$CATEGORY: '+baseCat+ '/'+ x.split(': ')[1]+'\n' #write new category

    elif re.match("^[0-9][0-9]\.|[0-9]\.", x): #question start, format either:  1.  or 11.
        b = x.split('. ')[1] # break it at the . at the start of the q and take the second half
        
        #sanitize special chars
        b = special(b)
        
        buf = buf + '::IPYQuiz' + str(unit) + '-' + str(c)+ '::'+ b  
        c = c+1
    
    elif x.startswith('[html]'): #q start, with special formatting   

        b = x.split('. ')[1] # break it at the . at the start of the q and take the second half
        
        #sanitize special chars
        b = special(b)
        
        buf = buf + '::IPYQuiz1-' + str(c)+ '::[html]'+ b  
        c = c+1

    elif re.match("^[*][A-Z][)]", x): #correct answer
        if qasplit == 0: #we haven't started the answer section yet
            buf = buf + '{\n'
            qasplit = 1
        #sanitize special chars and add to buffer
        buf = buf + '=' + special(x.split('*')[1].split(') ')[1])

    elif re.match("^[A-Z][)]", x):  #incorrect answer
        if qasplit == 0: #we haven't started the answer section yet
            buf = buf + '{\n'
            qasplit = 1
        buf = buf + '~' + special(x.split(') ')[1])
    
    elif x.startswith('\n'):#blank line  -- close out question, insert blank line
        buf = buf + '}\n\n'  
        qasplit = 0
    
    else:  #continued Q or answer block
        buf = buf + special(x)
        #input processing for special chars
        

#now we close out the quiz, print it to our output file, and close our files
buf = buf + '\n}'
write.write(buf)
read.close()
write.close()

