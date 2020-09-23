import os
import re

patchFolder = 'www'

patchedWPTemplatesOptionsCnt = 0
patchedWPPluginsOptionsCnt = 0
patchedWPCacheExistCnt = 0

def patchStr(str, ranges):
    strLen = len(str)
    l = len(ranges)
    if l % 2 != 0:
      raise AssertionError('ranges len % 2 == 0 ')  
    patchedStr = ''
    sliceFrom = 0
    for i in range(0, l, 2):
        beg = ranges[i]
        end = ranges[i+1]

        if i + 2 < l:
            sliceTo = ranges[i+2]
        else:
            sliceTo = strLen

        if strLen > end and beg < end:
            patchedStr += str[sliceFrom:beg] + str[end:sliceTo]
        else:
            raise AssertionError('begin after ')
    return patchedStr

def createCopy(path, content):
    file = open(path, "w") 
    file.write(content) 
    file.close() 

def removeIncludedFile(path):
    fname = os.path.basename(path)
    d = os.path.dirname(path)
    base = os.path.basename(d)
    full = os.path.join(d, '.'+base+'.php')
    removeFile(full, 'Include at ' + fname)
   
        
def writeToOpenFile(f, content):
    f.seek(0)
    f.write(content)
    f.truncate()

def removeFile(path, cause):
    try:
        file_stats = os.stat(path)
        os.remove(path)
        print('File ' + path + ' removed cause ' +  cause + ' ' + str(file_stats.st_size / 1024) + 'Kb')
    except FileNotFoundError:
        print('File '+ path +' not found, skipping')


def removeFileIsFoundAtBeginning(needle, fileContent, path):
    index = fileContent.find(needle, 0, 100)
    if index > 0:
       removeFile(path, needle)
    return index > 0

def patchIsWPTemplatesOptionsFile(content, path):
    global patchedWPTemplatesOptionsCnt 
    patchedWPTemplatesOptionsCnt += 1
    return removeFileIsFoundAtBeginning('WPTemplatesOption', content, path)
    

def patchIsWPPluginsOptionsFile(content, path):
    global patchedWPPluginsOptionsCnt 
    patchedWPPluginsOptionsCnt += 1
    return removeFileIsFoundAtBeginning('WPPluginsOptions', content, path)


def patchIsWPCacheExistFile(content, path):
    global patchedWPCacheExistCnt 
    patchedWPCacheExistCnt += 1
    return removeFileIsFoundAtBeginning('WPCacheExist', content, path)

def patchIsIncludeFile(content, path, file):
    matches = matchExp.finditer(content)
    ranges = []
    for m in matches:
        ranges.append(m.start())
        ranges.append(m.end())
    
    l = len(ranges)
    
    if l > 0:
        patchedStr = patchStr(content, ranges)
        #createCopy(path+'.bak', patchedStr)
        writeToOpenFile(file, patchedStr)
        removeIncludedFile(path)
    return l > 0

def patchFile(path):
    patched = False
    with open(path, 'r+') as f:
        try:
            file_contents = f.read()
            
            patched = patchIsWPTemplatesOptionsFile(file_contents, path) or \
                patchIsWPPluginsOptionsFile(file_contents, path) or \
                patchIsWPCacheExistFile(file_contents, path) or \
                patchIsIncludeFile(file_contents, path, f)

            f.close()
        except UnicodeDecodeError:
            print('Ошибка декодирования ' + path)
    return patched



matchExp = re.compile(r"if.*?\(.*?file_exists.*class_exists.*?\(.*?'WPTemplatesOptions'.*?{[\S\s]*?}")

totalPatched = 0

for dp, dn, fs in os.walk(patchFolder):
    for f in fs:
        path = os.path.join(dp, f)
        if ".php" in path and patchFile(path):
           totalPatched+=1

print('Всего пропатчено ' + str(totalPatched))