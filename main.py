from sqlite3 import Row
from fastapi import FastAPI
import requests
import xmltodict
import json
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


api_urls = [
    "https://www.mymxp.com/x/?CD1BDE28829148FB87E8C6C894F84AAD",
    # "https://www.mymxp.com/x/?9F8DB2899D2F4DC58E01A18EDABC8993",
    # "https://www.mymxp.com/x/?27EF192D027D41D7BB31CF422D037C30",
    # "https://www.mymxp.com/x/?4699EB93DD7C4E43B3AAC7726E597E18",
    # "https://www.mymxp.com/x/?77C7D2F677E740029A0BB053045A313F",
    # "https://www.mymxp.com/x/?CDCA743BC3314EFBA11C128F9992C66A",
    # "https://www.mymxp.com/x/?CDCA743BC3314EFBA11C128F9992C66A",
    # "https://www.mymxp.com/x/?080B5470215D4403B1C3B71E2A4E5A93",
    # "https://www.mymxp.com/x/?9F8DB2899D2F4DC58E01A18EDABC8993",
    # "https://www.mymxp.com/x/?6D38E6E5E56F4A6282CD152B6E24BACB"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def xml_extractor(links):
    return_value = []
    for link in links:
        code = link.split("/",5)[-1]

        xml_link = f"https://www.mymxp.com/cgi-bin/ExportDoc.exe/POInterfaceFile{code}&XML"

        response = requests.get(xml_link)

        data_dict = xmltodict.parse(response.text)
        data_dict = data_dict['DATAPACKET']['ROWDATA']['ROW']
        attribute = ["@Company","@Destination","@PO_Number","@Line_Number","@Item_Code","@Item_Description","@Specification","@General_Spec","@Quality_Spec","@Packing_Specification","@Unit","@Quantity","@Unit_Cost","@Total_Cost","@Comment_By_Purchasing","@Manufacturer_Name","@Manufacturer_Ref_No","@Supplier_Nbr","@GLAccountName","@LineGUID","@PO_Login_Code","@ClientID","@Delivery_Place","@Delivery_Date","@Deliver_Goods_By"]

        counter = 0

        while counter < 25:
            for i in data_dict:
                i[attribute[counter][1:]] = i.pop(attribute[counter])
                # print(counter)
            counter += 1    


        return_value.append(data_dict)
    return return_value


@app.get("/")
async def get_purchase_orders():
    return xml_extractor(api_urls)

@app.get("/get_po/")
async def get_purchase_order(link:str):
    link = [link]
    return xml_extractor(link)




