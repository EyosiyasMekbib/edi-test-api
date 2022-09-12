from fastapi import FastAPI
import requests
import xmltodict
import json

app = FastAPI()


api_urls = [
    "https://www.mymxp.com/x/?CD1BDE28829148FB87E8C6C894F84AAD",
    "https://www.mymxp.com/x/?9F8DB2899D2F4DC58E01A18EDABC8993",
    "https://www.mymxp.com/x/?27EF192D027D41D7BB31CF422D037C30",
    "https://www.mymxp.com/x/?4699EB93DD7C4E43B3AAC7726E597E18",
    "https://www.mymxp.com/x/?77C7D2F677E740029A0BB053045A313F",
    "https://www.mymxp.com/x/?CDCA743BC3314EFBA11C128F9992C66A",
    "https://www.mymxp.com/x/?CDCA743BC3314EFBA11C128F9992C66A",
    "https://www.mymxp.com/x/?080B5470215D4403B1C3B71E2A4E5A93",
    "https://www.mymxp.com/x/?9F8DB2899D2F4DC58E01A18EDABC8993",
    "https://www.mymxp.com/x/?6D38E6E5E56F4A6282CD152B6E24BACB"
]

def xml_extractor(links):
    return_value = []
    for link in links:
        code = link.split("/",5)[-1]

        xml_link = f"https://www.mymxp.com/cgi-bin/ExportDoc.exe/POInterfaceFile{code}&XML"

        response = requests.get(xml_link)
        data_dict = xmltodict.parse(response.text)
        
        return_value.append(data_dict)
       
    return return_value

@app.get("/")
async def get_purchase_orders():
    return xml_extractor(api_urls)