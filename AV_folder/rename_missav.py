import os

def main():
    print("请给我一个folder路径，我将删除底下所有的miss AV下载自带的后缀")
    path = r"D:\download"

    for file in os.listdir(path):
        if file.endswith("-uncensored-leak.mp4"):
            new_file_name = file.replace("-uncensored-leak","")
            file_path = os.path.join(path,file)
            new_file_path = os.path.join(path,new_file_name)

            print(file_path)
            print(new_file_path)
            os.rename(file_path,new_file_path)
            print("========================")

if __name__ == '__main__':
    main()