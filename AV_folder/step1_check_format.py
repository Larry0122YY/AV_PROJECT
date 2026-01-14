from genericpath import isdir
import os,sys

from pydantic import FilePath
from torch import le
import re


def main():
    folder_path = r'G:\japan'
    # folder_path = r'G:\japan\DDDDDDDDDATE'
    all_video_count,file_dict,folder_dict = _get_all_file_path(folder_path)

    print('++++++++++++++++++++++++++++++++++++++++++++++++')
    print(f"当前root路径'{folder_path}'下，一共有{all_video_count}个对象文件")
    print('++++++++++++++++++++++++++++++++++++++++++++++++')
    print()
    print()

    # result_file_check = check_file(file_dict)
    # fix_file(result_file_check)

    result_folder_check = check_folder(folder_dict)
    # fix_folder(result_folder_check)


def check_file(file_dict):
    '''
        1.每个视频文件，只会有一个点(.) ,只要不是一个点的，就打印出来
        目标是为了，让所有文件格式只有一个.

        2.每个视频文件，只会有一个横杠(-) ,只要不是一个横杠的，就打印出来
        目标是为了，让所有文件格式只有一个横杠

        这里，2没有错误才会执行下面的检查

            3.每个视频文件，横杠左边必须全是小写字母

            4.每个视频文件，横杠右边，必须全是数字

    '''

    print('\t以下是file的check结果')

    point_list = []
    haifu_list = []

    left_wrong_list = []
    left_upper_wrong_list = []
    right_wrong_list = []

    for file_name in file_dict.keys():

        file_path = file_dict[file_name]

        # 1.check 点
        count_point = file_name.count('.')
        if count_point != 1:
            point_list.append(file_path)

        # 2.check 横杠
        count_hifu = file_name.count('-')
        if count_hifu != 1:
            haifu_list.append(file_path)
        else:
            try:
            # 这里，2没有错误才会执行下面的检查

                # 分离横杠，check左边是否都是小写的英文字母，右边都是数字
                # 分离出的list只有2个元素，例：jul 001

                # 3.每个视频文件，横杠左边必须全是小写字母
                file_left_right = os.path.basename(file_name).split('.')[0].split('-')
                
                # 拿到左右两把的值
                left_info = file_left_right[0]
                right_info = file_left_right[1]

                check_code_left = _format_check_left(left_info)
                if check_code_left == 1:
                    left_wrong_list.append(file_path)
                elif check_code_left == 2:
                    left_upper_wrong_list.append(file_path)

                # 4.每个视频文件，横杠右边，必须全是数字
                check_code_right = _format_check_right(right_info)
                if check_code_right ==3:
                    right_wrong_list.append(file_path)
            except Exception as e:
                print('!!!!!!!!!!!!!!!!!!!')
                
                print(f'error file is {file_name}')
                print(f'path file is {file_path}')
                print('!!!!!!!!!!!!!!!!!!!')
                # print(e)
                sys.exit(3)
    
    _print_not_good(point_list,"点",2)
    _print_not_good(haifu_list,"横杠",2)

    _print_not_good(left_wrong_list,"左边不是字母",2)
    _print_not_good(left_upper_wrong_list,"左边是字母，但不是小写的",2)
    _print_not_good(right_wrong_list,"右边不是数字的",2)

    print()
    print('-------------------')
    print(f'这次，文件check的对象一共有{len(file_dict)}个')
    print('-------------------')
    print()

    return {
        'point_list':point_list,
        'haifu_list':haifu_list,
        'left_wrong_list':left_wrong_list,
        'left_upper_wrong_list':left_upper_wrong_list,
        'right_wrong_list':right_wrong_list
        }


def fix_file(result_file_check):
    '''
        将横杠左边的大写字母全部变成小写的
    '''

    need_to_be_lower_list = result_file_check['left_upper_wrong_list']
    print(need_to_be_lower_list)

    for need_to_be_lower_file in need_to_be_lower_list:

        folder_target = os.path.dirname(need_to_be_lower_file)
        file_taget = os.path.basename(need_to_be_lower_file)

        new_file = file_taget.lower()  # 全部变小写
        new_path = os.path.join(folder_target, new_file)

        os.rename(need_to_be_lower_file, new_path)

        print("已重命名为：", new_path)


def check_folder(folder_dict):
    '''
        1.每个视频分段文件夹，只会有一个横杠(-) ,只要不是一个横杠的，就打印出来
        目标是为了，让所有文件格式只有一个横杠

        这里，1没有错误才会执行下面的检查

            2.每个视频分段文件夹，横杠左边必须全是小写字母

            3.每个视频分段文件夹，横杠右边，必须全是数字

    '''
    haifu_list = []

    left_wrong_list = []
    left_upper_wrong_list = []
    right_wrong_list = []

    for file_name in folder_dict.keys():

        file_path = folder_dict[file_name]

        # 2.check 横杠
        count_hifu = file_name.count('-')
        if count_hifu != 1:
            haifu_list.append(file_path)
        else:
            try:
            # 这里，1没有错误才会执行下面的检查

                # 分离横杠，check左边是否都是小写的英文字母，右边都是数字
                # 分离出的list只有2个元素，例：jul 001

                # 2.每个视频文件，横杠左边必须全是小写字母
                file_left_right = os.path.basename(file_name).split('.')[0].split('-')
                
                # 拿到左右两把的值
                left_info = file_left_right[0]
                right_info = file_left_right[1]

                check_code_left = _format_check_left(left_info)
                if check_code_left == 1:
                    left_wrong_list.append(file_path)
                elif check_code_left == 2:
                    left_upper_wrong_list.append(file_path)

                # 3.每个视频文件，横杠右边，必须全是数字
                check_code_right = _format_check_right(right_info)
                if check_code_right ==3:
                    right_wrong_list.append(file_path)
            except Exception as e:
                print('!!!!!!!!!!!!!!!!!!!')
                print(f'error file is {file_name}')
                print('!!!!!!!!!!!!!!!!!!!')
                print(e)
        
    _print_not_good(haifu_list,"横杠",2)

    _print_not_good(left_wrong_list,"左边不是字母",2)
    _print_not_good(left_upper_wrong_list,"左边是字母，但不是小写的",2)
    _print_not_good(right_wrong_list,"右边不是数字的",2)

    print()    
    print('-------------------')
    print(f'这次，文件夹视频分段的check的对象一共有{len(folder_dict)}个')

    return {
        'haifu_list':haifu_list,
        'left_wrong_list':left_wrong_list,
        'left_upper_wrong_list':left_upper_wrong_list,
        'right_wrong_list':right_wrong_list
    }


def fix_folder(result_folder_check):
    '''
        将横杠左边的大写字母全部变成小写的
    '''

    need_to_be_lower_list = result_folder_check['left_upper_wrong_list']
    print(need_to_be_lower_list)

    for need_to_be_lower_folder in need_to_be_lower_list:

        parent = os.path.dirname(need_to_be_lower_folder)  # 父目录
        folder_name = os.path.basename(need_to_be_lower_folder)  # 文件夹名

        new_folder = os.path.join(parent, folder_name.lower())

        os.rename(need_to_be_lower_folder, new_folder)

        print("改名完成：", new_folder)


def _format_check_left(left_info):
    '''
        进行check，如果：
            左边不是字母，返回1
            左边是字母，但是不是全小写的，返回2
            正常，返回0
    '''
    # 首先对左边进行判断,是否全是英文字母，不是的话，找出来
    if re.fullmatch(r"[A-Za-z]+", left_info):
        # 如果不是小写的，找出来
        if not re.fullmatch(r"[a-z]+", left_info):
            return 2
    else:
        return 1
    
    return 0


def _format_check_right(right_info):
    '''
        进行check，如果：
            右边不是数字，返回3
            正常，返回0
    '''
    # 对右边的进行判断，是否是数字，不是的话，找出来
    if not re.fullmatch(r"[0-9]+",right_info):
        return 3

    return 0


def _print_not_good(error_list,name,level):
    '''
        给你一个不符合标准的list，如果list里有东西，说明有错误，没有则说明没有
    '''
    print('\t'*level + '-------------------------')
    print('\t'*level + f'以下是{name}的不符合规定的文件路径')
    error_count = len(error_list)
    if error_count > 0:
        for point in error_list:
            print(point)
        print()
        print('\t'*level + f'{name}的，不符合的个数是{error_count}')
    else:
        print('\t'*level + f'{name}的错误list没有')
    

def _get_all_file_path(folder_path):
    '''
        获取所有文件的路径，默认为从下面的路径中获取
            root dir
                zone dir
                    file/folder(一个视频文件分段的)
        
        获取后的格式，例：
            file_list: {jul-034.mp4,c://XXXX//XXX//jul-034.mp4}
            folder_list: {jul-035,c://XXXX//XXX//jul-034}
        
    '''

    # 初始化
    # 所有视频文件个数(包括文件夹分段的视频)
    all_video_count = 0
    # 所有单个视频文件
    file_dict = {}
    # 所有分段的文件夹视频
    folder_dict = {}

    # 获取所有文件的路径
    for zone_folder_name in os.listdir(folder_path):
        zone_folder_path = os.path.join(folder_path,zone_folder_name)

        # root文件夹下，只能有各个分区的文件夹，不能有文件，root文件夹下，只要有文件存在，就shut down
        # 各个分区的文件夹下，才是视频
        if not os.path.isdir(zone_folder_path):
            print(zone_folder_path)
            print('root路径下，居然有不是folder 的文件！程序结果，你自己检查下吧')
            sys.exit(1)
        
        # 遍历分区文件夹下的所有文件 这里应该每个都是视频文件(或者分段视频文件夹)
        for video_file_path in os.listdir(zone_folder_path):

            all_video_count += 1
            cur_file = os.path.join(zone_folder_path,video_file_path)

            if os.path.isfile(cur_file):
                file_dict[video_file_path] = cur_file
            else:
                folder_dict[video_file_path] = cur_file
    
    return all_video_count,file_dict,folder_dict


if __name__ == '__main__':
    main()