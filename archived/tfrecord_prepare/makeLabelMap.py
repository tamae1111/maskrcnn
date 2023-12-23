label_map_path = "./output_label_map.pbtxt" #保存パス
categories = ["vehicle","truck","c_vehicle","person"] #ラベルの配列

def makeLabelMap():

    end = '\n'
    s = ' '
    class_map = {}
    for ID, name in enumerate(categories):
        out = ''
        out += 'item' + s + '{' + end
        out += s*2 + 'id:' + ' ' + (str(ID+1)) + end
        out += s*2 + 'name:' + ' ' + '\'' + name + '\'' + end
        out += '}' + end*2


        with open(label_map_path, 'a') as f:
            f.write(out)

        class_map[name] = ID+1
    

if __name__ == '__main__':
    makeLabelMap()