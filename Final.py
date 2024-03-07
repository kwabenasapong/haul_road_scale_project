import serial
import openpyxl
from datetime import date,datetime
import SQL
import  PrinterConnect

#Setting scale port parameters

def Auto(ScalePort,PrinterPort,id):
    ConnectScale= serial.Serial(port=ScalePort,baudrate=9600,timeout=2)
    if id==1 and ConnectScale.is_open:
        
        print("Connection established")
        #Check to see if the COM6 port is open, if true then code the while loop will run
        while ConnectScale.is_open:

            SerialData=ConnectScale.read(120)
            if len(SerialData)>5:
                InputD=SerialData.decode().splitlines()
                print(InputD)
                dataSize=len(SerialData)
                
                #WeighIn Mode
                if dataSize >1 and dataSize <90:
                    #set weigh in mode 
                    printerDataIn=SerialData
                    Gross=""
                    Mode="WEIGH IN"
                    print("Weigh In")
                    for item in range(len(InputD)+1):
                        match item:
                            case 1:
                                TruckId=InputD[item][11:]

                            case 3:
                                start=InputD[item]

                                for letter in range(len(start)):
                                    word=str(start[letter])
                                    search=word.isnumeric()

                                    if search:
                                        Gross+=word

                            case 5:
                                Date=InputD[item][0:7]
                                Time=InputD[item][8:]
                    ExData=[TruckId,Gross,Date,Time]

                    SetSQL=SQL.SQL_IN(ExData)
                    SetPrinterIn=PrinterConnect.Printer(PrinterPort,True,printerDataIn)
                    print(TruckId)
                    print(Gross)
                    print(Date)
                    print(Time)
                    return Mode
                #WeigghOut Mode
                elif dataSize>100:
                    #set weighout mode
                    printerDataOut=SerialData
                    print("Weigh Out")
                    Gross=""
                    Net=""
                    Tare=""
                    Mode="WEIGH OUT"
                    for item in range(len(InputD)+1):
        
                        match item:
                            case 0:
                                TruckId=InputD[item][10:]    
                            
                            case 2:
                                start=InputD[item]

                                for letter in range(len(start)):
                                    word=str(start[letter])
                                    #print(middle)
                                    search=word.isnumeric()
                                    if search:
                                        Gross+=word

                            case 3:
                                start=InputD[item]

                                for letter in range(len(start)):
                                    word=str(start[letter])
                                    #print(middle)
                                    search=word.isnumeric()
                                    if search:
                                        Tare+=word
                            
                            case 4:
                                start=InputD[item]

                                for letter in range(len(start)):
                                    word=str(start[letter])
                                    #print(middle)
                                    search=word.isnumeric()
                                    if search:
                                        Net+=word
                            
                            case 6:
                                Date=InputD[item][0:7]
                                Time=InputD[item][8:]
                    ExData=[TruckId,Gross,Tare,Net,Date,Time]

                    SetSQL=SQL.SQL_OUT(ExData)
                    SetPrinterOut=PrinterConnect.Printer(PrinterPort,True,printerDataOut)

                    print(TruckId)
                    print(Gross)
                    print(Tare)
                    print(Net)
                    print(Date)
                    print(Time)

                    return Mode

            
        
            # Remove all data in the read buffer
            ConnectScale.reset_input_buffer() 

    #Close Scale and Excel file
    ConnectScale.close










