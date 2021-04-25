import requests


# image has to be accessed online.
def image_to_text(image_url):
    # number of keys can send the request via api
    keys = ['b9b5df32f8msh948aa3b15534102p1ad977jsn6e47a84b40d3',
            '7ae890b37fmshe9523cf53d7b361p187537jsn61635bf55d64',
            '5dff3c7d5emshcfb7ca7eadc6111p156ac1jsn1825d021d248',
            'fb2e945d1fmsh1a14cb50e5e9a55p17de56jsnb81aefa62e2a',
            '3a3f154ed4mshab2dac338951432p196979jsn5a87096e7a9f',
            'c63dbfd753msh55284ac72561390p1fa9ddjsn59510c9faf51',
            '248a3c7ad6msh5f147c1d696da48p1d9c47jsnbd815bbf6cc2',
            '8e3563101emsh67b1813e250e8e5p1f5069jsn2f94c8890bd2',
            'e7a7011470msh918b1b4000f9ac4p18fb8bjsn253c915a8ac7',
            'addbae0c4bmshd72190c8418d504p134020jsnf7fa8d67a7af',
            '0c4bdee0eamshcf230e88ab126a0p1697bejsnffad01d3c6c7',
            '05559aab0amsh4c15eac0ff2f4d2p1ef3dfjsn1af89c0cdb48',
            '544764be9fmsh752065920e265a5p16ea8bjsn5ed7bb2693d7',
            'fe8419972fmsh52bbabe303e2d90p12a194jsn33bfd568025a',
            '0b14d9cdfemsh33fd4da7551016cp1b8b90jsn5be9eb1eda7a',
            "cd64c648b4msh8a6d48365b0374bp105766jsne7a29e5dfcb4",
            "0230adc154mshfbc439f7ddde556p17394fjsn0d3957abf5bb",
            "15c0cdeb68msh84cfd07b34f37f2p1e62c5jsn5d996c57049f",
            "b0ab8bf78bmshe29b4cc002d61b8p1f75e3jsnf7891e706414",
            "a90c0d3cc6mshd6b13374e81ca6dp10eee5jsnb3da9d892f76",
            "7a07324785mshd7629a8c8efe4f4p19062ajsn4a1826f8e863",
            "6627d1e7admshc18328b7979defdp16b966jsn4251afccb2be",
            "bdd6d36efamshd8646144399328dp18c730jsnc5719af5f850",
            "d85a671a1amshb80d6d19bb58cbdp119cd8jsnca4c8dc4e36d",
            "fdc37b4e6cmsh441f7cb1ecb529ep19d62bjsnc0789ed68ae7"]
    for i in range(len(keys)):
        url = "https://ocrly-image-to-text.p.rapidapi.com/"
        querystring = {"imageurl": f'{image_url}',
                       "filename": "sample.jpg"}
        headers = {
            'x-rapidapi-key': keys[i],
            'x-rapidapi-host': "ocrly-image-to-text.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        if response.status_code > 200:
            continue
        else:
            return response.text