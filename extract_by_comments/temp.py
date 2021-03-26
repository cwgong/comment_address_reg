import re

punctuation = '\！\，\；\：\？\。!,;:?".'


def removePunctuation(text):
    text = re.sub(r'[{}]+'.format(punctuation), '。', text)
    return text.strip().lower()

if __name__ == "__main__":
    # text = "women,一起，吃饭？好了吗！快点。吧,momo层层啊?快点吧!lll"
    # text_ = removePunctuation(text)
    # print(text_)
    # s = "作业帮App"
    # print(s.lower())
    tmp_tuple = (3,1)
    print(tmp_tuple[0])