import os

def CountTabs(line):
    return len(line) - len(line.lstrip("\t"))

def GetLevelList(Text, Title=True):
    LevelList = []
    Level = [0]
    if(Title):
        PrevTabNum = 1
        Text = Text[1:]
        LevelList.append("T")
    else:
        PrevTabNum = 0
    
    for line in Text:
        TabNum = CountTabs(line)
        DifTab = TabNum - PrevTabNum
        if(DifTab == 0):
            Level[-1] += 1
        elif(DifTab > 0):
            Level.append(1)
        else:
            Level = Level[:DifTab]
            Level[-1] += 1

        LevelList.append(Level.copy())
        PrevTabNum = TabNum
    
    return LevelList

def ListToText(list):
    newlist = []
    for L in list:
        newlist.append("-".join(map(str, L)))
    return newlist

def AddChild(Tree, level, name, text, tab=4*" "):
    child = "\n" + level*tab + f"child{{ node ({name}) {{{text}}} }}"
    Tree = Tree[:-level] + child + Tree[-level:]
    return Tree

def Text2Tree(Text):
    LevelList = GetLevelList(Text)
    NameList = ListToText(LevelList)

    # Para el título
    Tree = f"\\node ({NameList[0]}) {{{Text[0]}}} ;"

    for i in range(1,len(Text)):
        line = Text[i]
        level = CountTabs(line)
        name = NameList[i]
        text = line.strip()

        Tree = AddChild(Tree, level, name, text)

    return Tree




# SOLICITUD DEL ARCHIVO

direction = input("Ingrese el nombre del archivo: ")
if(not direction):
    direction = "Example.txt"

# LECTURA DEL ARCHIVO

with open(direction) as File:
    Text = [ line.rstrip("\n") for line in File.readlines()]

# CREACIÓN DE LA SALIDA

with open("template.tex") as Template:
    Output = Template.read()

OutputDir = "./Output/" + direction[:-4] + "Output.tex"

with open(OutputDir, "w") as OutputFile:
    Output = Output.replace("%::NODE_VAR::", Text2Tree(Text))
    OutputFile.write(Output)


# CREACIÓN DEL PDF
os.system(f"latexmk {OutputDir} -synctex=1 -interaction=nonstopmode -file-line-error -pdf -outdir=./Output" )