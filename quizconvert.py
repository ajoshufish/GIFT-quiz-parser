import re  # we need to use regex


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

#setup our output buffer, question counter, and write the file header
buf = '$CATEGORY: IPY Quiz 1 Test\n\n'
c = 1

#each line is a question or possible answer (essentially), so let's loop through them and process each by type
for x in read:
    if re.match("^[0-9][0-9]\.|[0-9]\.", x): #question start, format either:  1.  or 11.
        b = x.split('. ')[1] # break it at the . at the start of the q and take the second half
        
        #sanitize special chars
        b = special(b)
        
        buf = buf + '::IPYQuiz1-' + str(c)+ '::'+ b +'{\n' 
        c = c+1
    elif x.startswith('*'): #correct answer

        #sanitize special chars and add to buffer
        buf = buf + '=' + special(x.split('*')[1].split(') ')[1])

    elif x.startswith('\n'):#blank line  -- close out question, insert blank line
        buf = buf + '}\n\n'  
    else:  #incorrect

        #input processing for special chars
        buf = buf + '~' + special(x.split(') ')[1])

#now we close out the quiz, print it to our output file, and close our files
buf = buf + '}'
write.write(buf)
read.close()
write.close()

