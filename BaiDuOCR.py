from aip import AipOcr

# API
# 输入自己的三个参数
APP_ID = 'xxxxx'
API_KEY = 'xxxxx'
SECRET_KEY = 'xxxxx'

# 初始化AipFace对象
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)


# 读取图片
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


# 获取图片内容
def img_to_str(image_path):
    # 可选参数 
    # options = {}
    # options["language_type"] = "CHE_ENG"  # 英文混合
    # options["detect_direction"] = "true"  # 检测朝向
    # options["detect_language"] = "true"  # 是否检测语言
    # options["probability"] = "false"  # 是否返回识别结果中每一行的置信度

    # 带参数调用通用文字识别
    # result = client.basicGeneral(get_file_content(filePath), options)
    # 不带参数的数字识别
    result = client.numbers(get_file_content(image_path))

    # 格式化输出-提取需要的部分
    if 'words_result' in result:
        text = ('\n'.join([w['words'] for w in result['words_result']]))
    # print(type(result), "和", type(text))
    # print(result)
    # print(text)
    return text

# if __name__ == '__main__':
#     filePath = './imagevcode.jpg'
#     img_to_str(filePath)
#     print("识别完成。")
