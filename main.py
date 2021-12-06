from playsound import playsound

from src.config import config_init

if __name__ == '__main__':
    # 初始化配置
    config_init()
    print('1')
    playsound("./voice/error.wav", False)
    print('2')
    print('3')
