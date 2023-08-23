from pdf2image import convert_from_path
from dotenv import dotenv_values
import os
import requests
import sys
import time
from pymongo import MongoClient
from bson.objectid import ObjectId
import hashlib
import hmac
from stack import upload_custom
from datetime import datetime


config = dotenv_values(".env")

password_mg_db = config["MONGODB_PWD"]

connection_string = f"mongodb+srv://herman:{password_mg_db}@production.4d02xna.mongodb.net/?retryWrites=true&w=majority&authSource=admin"
client = MongoClient(connection_string)
# dbs = client.list_database_names()
# print(dbs)
db = client.packinglist
order_collection = db.lsorders
last_order_collection = db.lastorder

# # COLORLAB
COLORLAB_SHOP_ID = config["COLORLAB_SHOP_ID"]
COLORLAB_API_KEY = config["COLORLAB_API_KEY"]
COLORLAB_API_SECRET = config["COLORLAB_API_SECRET"]

POPPLER_PATH = r"C:\Users\herma\Downloads\Release-23.01.0-0\poppler-23.01.0\Library\bin"


def get_customization():

    # order = order_collection.find_one({"number": "350401"})
    while True:
        order = order_collection.find_one({"flagCustomDownloaded": False})
        if order:
            for product in order["products"]:
                if product["customizationString"] != "":

                    customization_id = product["customizationId"]
                    customization_token = product["customizationToken"]
                    pdf_file_name = product["pdfFileName"]
                    jpeg_file_name = product["jpgFileName"]

                    verificationString = COLORLAB_SHOP_ID+customization_id+customization_token

                    hash = hmac.new(COLORLAB_API_SECRET.encode('utf-8'), verificationString.encode(
                        'utf-8'), hashlib.sha256).hexdigest()

                    colorlab_url = f"https://api.colorlab.io/v1/configuration/{customization_id}/{customization_token}/export"

                    headers = {"content-Type": "application/pdf", "X-Colorlab-Shop": COLORLAB_SHOP_ID,
                               "X-Colorlab-Api-Key": COLORLAB_API_KEY, "X-Colorlab-Api-Signature": hash}
                    response = requests.get(url=colorlab_url, headers=headers)
                    customization_file = response.content
                    file_size = response.headers["Content-Length"],

                    # check if the request was successful
                    if response.status_code == 200:
                        # open a file to write the contents of the PDF local
                        with open(f"./customizations/{pdf_file_name}", 'wb') as f:
                            f.write(customization_file)
                            print(
                                f"{pdf_file_name} saved successfully", datetime.now())

                        # upload_custom(customization_file,
                        #               file_size, pdf_file_name)
                    else:
                        print("Error: could not receive PDF file")

                    time.sleep(2)

                    img_pages = convert_from_path(f"./customizations/{pdf_file_name}",
                                                  poppler_path=POPPLER_PATH)
                    for page in img_pages:
                        page.save(f"./prints/{jpeg_file_name}", "JPEG")

                # SLEEP : 6 colorlab requests per minute
                time.sleep(10)

            objInstance = ObjectId(order["_id"])
            order_collection.update_one({"_id": objInstance}, {
                "$set": {"flagCustomDownloaded": True}})

        else:
            print("ALL CUSTOMIZATIONS DONE")
            break


if __name__ == "__main__":
    print(__name__, ": VAN FETCH LIFGTSPEED")
    # get_customization()


# inputpath = r"my_pdf_file.pdf"
# outputpath = r""
# result = pdf2jpg.convert_pdf2jpg(inputpath, outputpath, pages="ALL")

# const getCustomizationsAndStore = async function(
#   orderNumber,
#   customizationId,
#   customizationToken,
#   productTitle
# ) {
#   try {
#     const verificationString =
#       process.env.SHOP_ID + customizationId + customizationToken;
#     // Calling createHmac method
#     const hash = await crypto
#       .createHmac("sha256", process.env.API_SECRET)
#       .update(verificationString)
#       .digest("hex");

#     const result1 = await axios({
#       method: "get",
#       url: `https://api.colorlab.io/v1/configuration/${customizationId}/${customizationToken}/export`,
#       responseType: "stream",
#       headers: {
#         "content-Type": "application/pdf",
#         "X-Colorlab-Shop": process.env.SHOP_ID,
#         "X-Colorlab-Api-Key": process.env.API_KEY,
#         "X-Colorlab-Api-Signature": hash,
#       },
#     });

#     const afbeelding = result1.data;
#     console.log("PRINT OPGEHAALD BIJ COLORLAB", Date());

#     await afbeelding.pipe(
#       fs.createWriteStream(
#         `${fileLocation2}${orderNumber}-${customizationId}-${productTitle}.pdf`
#       ),
#       (err) => {
#         if (err) {
#           console.log(err);
#         }
#       }
#     );

#     await sleep(2000);

#     await convertToPng(
#       `${fileLocation2}${orderNumber}-${customizationId}-${productTitle}.pdf`
#     );
#     console.log("png aangemaakt");
#   } catch (error) {
#     console.log(
#       "FOUT MET FETCHDATA/COLORLAB OR WRITE TO FILE// FETCHDATA/COLORLAB"
#     );
#   }
# };

# const saveCustomToDb = async () => {
#   try {
#     const order = await Lsorder.findOne({ flagCustomDownloaded: false });
#     //const order = await Lsorder.findOne({ number: 350517 });

#     if (order == null) {
#       console.log("All Customizations done");
#       return;
#     }
#     const orderNumber = order.number;
#     const productsArray = order.products;

#     for (let index = 0; index < productsArray.length; index++) {
#       const { customizationId, customizationToken, productTitle } =
#         productsArray[index];
#       const productTitleN = productTitle.replaceAll(" ", "-");
#       console.log(orderNumber, productTitleN, customizationId);

#       if (customizationToken !== "") {
#         getCustomizationsAndStore(
#           orderNumber,
#           customizationId,
#           customizationToken,
#           productTitleN
#         );
#       }
#       await sleep(5000);
#     }

#     await Lsorder.findOneAndUpdate(
#       { number: order.number },
#       //{ lastname: "naam107" },
#       { flagCustomDownloaded: true },
#       { returnDocument: "after" }
#     ).then((res) => {
#       console.log(res.flagCustomDownloaded);
#     });
#   } catch (error) {
#     console.log("FOUT BIJ SAVEDATA/CUSTOTODB");
#   }
# };
