#! python3

import sys

sys.path.append("\\\\10.1.37.5\\国住共享文件夹\\国住设计区\\设计共享区\\BIM项目\\pyRevitExtension\\Lib\\site-packages")

print(sys.path)

import numpy as np
import pandas as pd



mydataset = {
  'cars': ["BMW", "Volvo", "Ford","Nissan"],
  'passings': [3, 7, 2,4]
}

myvar = pd.DataFrame(mydataset)

print(myvar)
