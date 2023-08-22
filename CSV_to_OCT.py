# -*- coding: utf-8 -*-
"""
Convert "KepServer" CSV file to "OPC Quick Client" OTC file - by Olivier
"""
import binascii, os

def TypeToHex(tipo): #convertire il tipo in un carattere hexadecimale
    if tipo=="Default":
        return "00" #hex(0)[2:].zfill(2)
    elif tipo=="Short":
        return "02" #hex(2)
    elif tipo=="Double":
        return "05" #hex(5)
    elif tipo=="String":
        return "08" #hex(8)
    elif tipo=="Boolean":
        return "0B" #hex(11)
    elif tipo=="Word":
        return "12" #hex(18)
    else:
        print("Tipo "+tipo+" non trovato")
        return
    
def CSVtoOCT(FileAdress):
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
    BlockInizio2 = "000000"
    BlockItem1 = "02000000fffeff00fffeff"
    BlockItem2 = "01"
    BlockItem3 = "0003000000"
        
    with open(FileAdress.replace('.csv','.otc'),"wb") as file_out:  #create a file / "wb" = write Binary / togliere l'estensione CSV e aggiungere OTC invece.
        file_out.write(binascii.unhexlify(BlockInizio1))
        file_out.write(binascii.unhexlify(hex(total_number)[2:].zfill(2))) #(hex(numero totale di elementi) /"[2:]"per togliere "0x" /"zfill(2)"per forzarlo a 2 bits.
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

FolderName = os.getcwd() #get current dir
print(FolderName)    
for FileName in os.listdir(FolderName):
    if FileName.endswith(".csv"): #select a folder and take all csv files in it
        print(FileName)
        CSVtoOCT(FolderName+"\\"+FileName)