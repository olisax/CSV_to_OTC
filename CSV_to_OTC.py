# -*- coding: utf-8 -*-
"""
Convert "KepServer" CSV file to "OPC Quick Client" OTC file - by Olivier
"""
import binascii, os, sys

def display_help(): #descrizione del programma.
    help_text = """
    Convert "KepServer" CSV file to "OPC Quick Client" OTC file for a quick visualization of all tags in a datalogger.
    
    Usage:
    - In KepServer, go to Data Logger, select Data Map and click on "Export CSV..."
    - Save this CSV file to a folder on your local computer.
    - Run CSV_to_OTC in this folder to generate an OTC file. If older OTC files exist, they will be overwritten.
    - Open "OPC Quick Client". File, Open... and select the OTC file.

    Options:
    - No arguments: Process all .csv files in the current directory.
    - 1 argument:
      * If it's a .csv filename: Process the specific file in the current directory.
      * If it's a directory: Process all .csv files in the directory.
    - 2 arguments:
      * Arguments can be in any order: .csv filename and directory.
      * Process the specific file in the specified directory.
    """
    print(help_text)
    
def is_directory(path): #check if the path is a directory by checking if it contains '/' or '\\'.
    return '/' in path or '\\' in path

def TypeToHex(tipo): #convertire il tipo in un carattere hexadecimale
    if tipo=="Default":
        return "00" #hex(0)[2:].zfill(2)
    elif tipo=="Short":
        return "02" #hex(2)
    elif tipo=="Long":
        return "03" #hex(3)
    elif tipo=="Float":
        return "04" #hex(4)
    elif tipo=="Double":
        return "05" #hex(5)
    elif tipo=="String":
        return "08" #hex(8)
    elif tipo=="Boolean":
        return "0B" #hex(11)
    elif tipo=="Char":
        return "10" #hex(16)
    elif tipo=="Word":
        return "12" #hex(18)
    elif tipo=="Dword":
        return "13" #hex(19)
    else:
        print("Tipo "+tipo+" non trovato")
        return
    
def CSVtoOTC(FileAdress):
    LogItems=[]
    LenItems=[]
    TipoItems=[]
    total_number=0
    
    file_in = open(FileAdress,"r",encoding="utf8") #leggere il file CSV di KepServer
    for line in file_in:
        if line.startswith('"'): #per tagliare le prime 4 righe nel file CSV 
            line2=line.replace('"','')
            List_line2=line2.split(",")
            if (List_line2[0].count("Data_Ora_PC"))==0: #eliminare il Timestamp "Data_Ora_PC"
                total_number+=1
                LogItems.append(List_line2[0])
                LenItems.append(len(List_line2[0]))
                TipoItems.append(TypeToHex(List_line2[2]))
            
    #Scrivere un file binario in hex
    BlockInizio1 = "0100000002000000fffeff0c51007500690063006b00200043006c00690065006e007400fffeff164b006500700077006100720065002e004b0045005000530065007200760065007200450058002e0056003600fffeff00000000000100000001000000fffeff06470072006f00750070003000e8030000090400000000000000000000010000000200000000000000"
    BlockInizio2 = "0000"
    BlockItem1 = "02000000fffeff00fffeff"
    BlockItem2 = "01"
    BlockItem3 = "0003000000"
        
    with open(FileAdress.replace('.csv','.otc'),"wb") as file_out:  #create a file / "wb" = write Binary / togliere l'estensione CSV e aggiungere OTC invece.
        file_out.write(binascii.unhexlify(BlockInizio1))
        file_out.write(binascii.unhexlify(hex(total_number%256)[2:].zfill(2))) #(hex(numero totale di elementi) /"[2:]"per togliere "0x" /"zfill(2)"per forzarlo a 2 bits.
        file_out.write(binascii.unhexlify(hex(total_number//256)[2:].zfill(2))) # "%"= modulo, "//"=divisione intera
        file_out.write(binascii.unhexlify(BlockInizio2))
        for i in range(total_number-1,-1,-1): #si va al contrario
            file_out.write(binascii.unhexlify(BlockItem1))
            file_out.write(binascii.unhexlify(hex(LenItems[i])[2:].zfill(2))) #len
            for c in LogItems[i]:
                file_out.write(binascii.unhexlify(hex(ord(c))[2:])) #elem, un carattere alla volta
                file_out.write(binascii.unhexlify("00")) #aggiungere spazio tra ogni caratteri
            file_out.write(binascii.unhexlify(BlockItem2))
            file_out.write(binascii.unhexlify(TipoItems[i])) #tipo 
            file_out.write(binascii.unhexlify(BlockItem3))

FileName = None
FolderName = None           
args = sys.argv[1:] #Get command-line arguments
            
if len(args) == 1:
    if sys.argv[1].endswith(".csv"):
        if os.path.isfile(sys.argv[1]):
            FileName = sys.argv[1]
        else:
            print(f"File '{sys.argv[1]}' not found in the current directory.")
            exit()
    elif is_directory(sys.argv[1]):
        FolderName = sys.argv[1]
    else:
        display_help()
        exit()
            
elif len(args) == 2:
    for arg in args:
        if arg.endswith(".csv"):
            FileName = arg
        elif is_directory(arg):
            FolderName = arg
    if FileName and FolderName:
        if os.path.isfile(FolderName+"\\"+FileName) == False:
            print(f"File '{FileName}' not found in directory '{FolderName}'.")
            exit()
    else:
        display_help()
        exit()
    
if FolderName == None:        
    FolderName = os.getcwd() #get current dir     
            
if FileName:   #if a filename is provided as an argument, open that file
    CSVtoOTC(FolderName+"\\"+FileName)  
else:  #if no argument is provided, open all CSV in the current directory
    for FileName in os.listdir(FolderName):
        if FileName.endswith(".csv"): #select a folder and take all csv files in it
            print(FileName)
            CSVtoOTC(FolderName+"\\"+FileName)
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
