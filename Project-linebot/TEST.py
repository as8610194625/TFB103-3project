import json
with open (r"C:\Users\Tibame\Desktop\TFB103-3project\Project-linebot\recommand_youmaybelike.json","r",encoding="utf-8") as f:
    a = json.loads(f.read())

    for key,valus in a.items():
        with open ("recommand.json","a",encoding="utf-8") as ff:
            s = json.dumps({key:valus})
            ff.write(s+',')
            print('1')
    print('OK')