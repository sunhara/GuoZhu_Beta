# dependencies
import clr
clr.AddReference('System.Windows.Forms')
clr.AddReference('IronPython.Wpf')



from Autodesk.Revit.DB import * #Loading Revit's API classes
from Autodesk.Revit.UI import * #Loading Revit's API UI classes  


app = __revit__.Application
doc = __revit__.ActiveUIDocument.Document

t = Transaction(doc,"Start a new Transaction")


def createList(r1, r2):
    return list(range(r1, r2+1))
     


# Place your code below this line
all_Sheets = FilteredElementCollector(doc)
all_Sheets.OfCategory(BuiltInCategory.OST_Sheets)
all_Sheets.WhereElementIsNotElementType()
all_Sheets_Ele = all_Sheets.ToElements()

indicat = all_Sheets_Ele[0].get_Parameter(BuiltInParameter.SHEET_NUMBER).AsString()
indicator = indicat.startswith("FB")

sheetsNum = []

for i in all_Sheets_Ele:
    num = i.get_Parameter(BuiltInParameter.SHEET_NUMBER)
       
    numValue = num.AsString()
    
    if  indicator:
        numValue1 = numValue.strip("FB") 
        
        sheetsNum.append(float(numValue1))
    else:
        sheetsNum.append(float(numValue))


# Get the sheets number as index
indices = sorted(range(len(sheetsNum)), key = lambda index: sheetsNum[index])
renumber = createList(1,len(indices))  #rename with the renumber


t.Start()

for i,j in zip(indices,renumber):
     num2 = all_Sheets_Ele[i].get_Parameter(BuiltInParameter.SHEET_NUMBER)
     numstr = str(j)
     
     if indicator:
        num2.Set(numstr)
     else:
        num2.Set("FB"+numstr)
     

t.Commit()
# Assign your output to the OUT variable.
#print( indicator,indicat,sheetsNum)