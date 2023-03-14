import os,sys,glob

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
    if level==1:
        child = "\n" + level*tab + f"child{{ node[MainTopic] ({name}) {{{text}}} }}"
    else:
        child = "\n" + level*tab + f"child{{ node ({name}) {{{text}}} }}"
    Tree = Tree[:-level] + child + Tree[-level:]
    return Tree

def Text2Tree(Text):
    LevelList = GetLevelList(Text)
    NameList = ListToText(LevelList)

    # Para el título
    Tree = f"\\node[MainTitle] ({NameList[0]}) {{{Text[0]}}} ;"

    for i in range(1,len(Text)):
        line = Text[i]
        level = CountTabs(line)
        name = NameList[i]
        text = line.strip()

        Tree = AddChild(Tree, level, name, text)

    return Tree


def AddExtension(d, ext=".tmm"):
    return d if d.endswith(ext) else d + ext


# SOLICITUD DEL LOS ARCHIVOS A LEER
if (len(sys.argv)==1) or (sys.argv[1] == "*"):
    direction = glob.glob("./Input/*.tmm")
else:
    direction = [ "./Input/" + AddExtension(d) for d in sys.argv[1:]]

for d in direction:
    with open(d) as TextFile:
        Text = [ line.rstrip("\n") for line in TextFile.readlines()]

    with open("template.tex") as TemplateFile:
        Template = TemplateFile.read()
    
    OutputDir = "./Output/" + os.path.basename(d).rstrip(".tmm") + ".tex"

    with open(OutputDir, "w") as OutputFile:
        Output = Template.replace("%::NODE_VAR::", Text2Tree(Text))
        OutputFile.write(Output)

    # Creación del PDF
    os.system(f"latexmk -synctex=1 -interaction=nonstopmode -file-line-error -lualatex -outdir=./Output/ {OutputDir}" )