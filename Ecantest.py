from ctypes import *
import time,ctypes,os,sys


'''
通过灯来判断状态00:58 power can1 can2    
DLL库 基于vb.net 开发

函数库调用流程
openDecice 打开设备 → InitCan 初始化某一路CAN → StartCAN 启动某一路CAN → Transmit (发送CAN帧) → Close Device 关闭设备
                                                                      Receive （读取CAN帧）
'''

# nDeviceType = 3 # 设备类型USBCAN-2E-U 单通道3 双通道4
# nDeviceInd = 0  # 索引号0，代表设备个数
# nReserved = 0  # 无意义参数
# # nCANInd = 1  # can通道号
class keydll:

    dllName = "ECANVCI库文件64位/ECanVci64.dll"
    # 配置项地址获取(获取当前文件的绝对路径)
    dllPath = os.path.join(os.path.abspath(os.path.dirname(__file__)),dllName).replace("\\",'/')

# 调用dll文件
dll = windll.LoadLibrary(keydll.configJsonPath)  

# 1.3.5 INIT_CONFIG定义一个python的'结构体'，使用ctypes继承Structure，内容是初始化需要的参数，依据产品手册
class VCI_INIT_CONFIG(Structure):
    _fields_ = [("AccCode", c_ulong),  # 验收码，后面是数据类型
                ("AccMask", c_ulong),  # 屏蔽码
                ("Reserved", c_ulong),  # 保留
                ("Filter", c_ubyte),  # 滤波使能。0=不使能，1=使能使能时，/
                # 请参照SJA1000验收滤波器设置验收码和屏蔽码。
                ("Timing0", c_ubyte),  # 波特率定时器0（BTR0）
                ("Timing1", c_ubyte),  # 波特率定时器1（BTR1）
                ("Mode", c_ubyte)    # 模式。=0为正常模式，=1为只听模式， =2为自发自收模式
                ]  

# 定义发送报文的结构体 CAN_OBJ 结构体表示帧的数据结构。在发送函数Transmit和接收函数Receive中被用来传送CAN信息帧。
class VCI_CAN_OBJ(Structure):
    _fields_ = [("ID", c_uint),  # 报文帧ID'''
                ("TimeStamp", c_uint),  # 接收到信息帧时的时间标识
                ("TimeFlag", c_ubyte),  # 是否使用时间标识， 为1时TimeStamp有效
                # 工作模式
                ("SendType", c_ubyte),  # 发送帧类型。=0时为正常发送,=1时为单次发送（不自动重发)，/
                # =2时为自发自收（用于测试CAN卡是否损坏） ， =3时为单次自发自收（只发送一次， 用于自测试），/
                # 只在此帧为发送帧时有意义。

                #工具：帧类型
                ("RemoteFlag", c_ubyte),  # 是否是远程帧。=0时为数据帧，=1时为远程帧。
                #工具：帧格式
                ("ExternFlag", c_ubyte),  # 是否是扩展帧。=0时为标准帧（11位帧ID），=1时为扩展帧（29位帧ID）。
                # 工具：长度
                ("DataLen", c_ubyte),  # 数据长度DLC(<=8)， 即Data的长度
                # 工具：数据
                ("Data", c_ubyte * 8),  # CAN报文的数据。 空间受DataLen的约束。
                ("Reserved", c_ubyte * 3)      # 系统保留
                ] 
  
class VCI_CAN_OBJ_SEND(Structure):
    _fields_ = [("ID", c_uint),
                ("TimeStamp", c_uint),
                ("TimeFlag", c_byte),
                ("SendType", c_byte),
                ("RemoteFlag", c_byte),
                ("ExternFlag", c_byte),
                ("DataLen", c_byte),
                ("Data",  c_ubyte*8),
                ("Reserved", c_ubyte*3)
                ]

# 接口卡设备类型定义类
class CanBoardTypeDefines:
    VCI_USBCAN1 = 3     # 设备类型号3
    VCI_USBCAN2 = 4     # 设备类型号4
    group1 = [VCI_USBCAN1, VCI_USBCAN2]

# 波特率可以定义类
class CanBoardTypeDefines:
    def group1_baud_rate3(self,baud_rate: int):
        try:
            if baud_rate == 500:
                timing0 = 0x00
                timing1 = 0x1c
                return timing0,timing1
            elif baud_rate == 666:
                timing0 = 0x80
                timing1 = 0xb6
                return timing0,timing1
            elif baud_rate == 800:
                timing0 = 0x00
                timing1 = 0x16
                return timing0,timing1
            elif baud_rate == 1000:
                timing0 = 0x00
                timing1 = 0x14
                return timing0,timing1
            else:
                raise Exception("group1 CAN卡所设置的波特率暂不被支持 波特率为"+ str(baud_rate))
        except Exception as e:
            raise e


# DLL通讯
class Communication():
    baud_rate_define = CanBaudrateDefines()
    initconfig = VCI_INIT_CONFIG(0x00000000,0xffffffff, 0, 1, 0x00, 0x14, 0)#
    vic.AccCode = 0x00000000     # 验收码，SJA1000的帧率验收码 全部是0即可 0x00000000
    vic.AccMask = 0xffffffff     # 屏蔽码，SJA1000的帧过滤屏蔽码  推荐设置未 0Xffff ffff即为全部接受
    vic.reserved = 0             # 保留
    vic.Filter = 0               # 滤波使能。0=不使能，1=使能使能时，/请参照SJA1000验收滤波器设置验收码和屏蔽码。
    vic.Timing0 = 0x00           # 500Kbps 波特率定时器0
    vic.Timing1 = 0x1C           # 500Kbps 波特率定时器0
    vic.Mode = 0                 # 模式。=0为正常模式，=1为只听模式， =2为自发自收模式







# 定义一个用于初始化的实例对象vic
# vic = VCI_INIT_CONFIG()
# vic.AccCode = 0x00000000     # 验收码，SJA1000的帧率验收码 全部是0即可 0x00000000
# vic.AccMask = 0xffffffff     # 屏蔽码，SJA1000的帧过滤屏蔽码  推荐设置未 0Xffff ffff即为全部接受
# vic.reserved = 0
# vic.Filter = 0
# vic.Timing0 = 0x00  # 500Kbps 波特率定时器0
# vic.Timing1 = 0x1C  # 500Kbps 波特率定时器0
# vic.Mode = 0        # 模式。=0为正常模式，=1为只听模式， =2为自发自收模式



# 定义报文实例对象，用于发送
vco = VCI_CAN_OBJ()
# vco.ID = 0x00000055  # 帧的ID 默认demo
vco.ID = 0x000003C0   # 帧的ID KL15,KLS 
# vco.ID = 0x000005F0   # 帧的ID 大灯 

vco.SendType = 1  # 发送帧类型，0是正常发送，1为单次发送，这里要选1！要不发不去！
vco.RemoteFlag = 0
vco.ExternFlag = 0
vco.DataLen = 8

# 单独传参数 十六进制 →OK
# 传参数 十六进制  转到 十进制 →OK
#大灯关闭信号 FD 00 0A FF FF 00 00 00	
# vco.Data = (0xfd, 0x00, 0x0a, 0xff, 0xff, 0x00, 0x00, 0x00)
# vco.Data = (253, 0, 10, 255, 255, 0, 0, 0)

#大灯打开信号 FD 8A 0A FF FF 00 00 00  
# vco.Data = (0xfd, 0x8a, 0x0a, 0xff, 0xff, 0x00, 0x00, 0x00)
# vco.Data = (253, 138, 10, 255, 255, 0, 0, 0)    

# 车辆点火 C0 00 43 00
vco.Data = (0xc0, 0x00, 0x2b, 0x00) 
# vco.Data = (192, 0, 67, 0)
vco.Reserved = (0, 0, 0)


# 定义报文实例对象，用于接收
vco2 = VCI_CAN_OBJ()
vco2.ID = 0x00000001  # 帧的ID 后面会变成真实发送的ID
vco2.SendType = 0  # 这里0就可以收到
vco2.RemoteFlag = 0
vco2.ExternFlag = 0
vco2.DataLen = 8
vco2.Data = (0, 0, 0, 0, 0, 0, 0, 0)
# vco2.Data = (0, 0, 0, 0)

'''设备的打开如果是双通道的设备的话，可以再用initcan函数初始化'''
# 步骤一 打开设备
# OpenDevice(设备类型号，设备索引号，参数无意义)
ret = dll.OpenDevice(nDeviceType, nDeviceInd, nReserved)
print("opendevice:", ret)

# 步骤二 执行参数初始化
# InitCAN(设备类型号，设备索引号，第几路CAN，初始化参数initConfig)，
ret = dll.InitCAN(nDeviceType, nDeviceInd, 0, byref(vic))
print("initcan0:", ret)

# 步骤三 打开对应CAN通道
# StartCAN(设备类型号，设备索引号，第几路CAN)
ret = dll.StartCAN(nDeviceType, nDeviceInd, 0)
print("startcan0:", ret)


# i = 1
# while i:
#     art = dll.Transmit(nDeviceType, nDeviceInd, 0, byref(vco), 1)  # 发送vco
#     ret = dll.Receive(nDeviceType, nDeviceInd, 0, byref(vco2), 1, 0)  # 以vco2的形式接收报文
#     time.sleep(1)  # 设置一个循环发送的时间
#     if ret > 0:
#         print(i)
#         print(list(vco2.Data))  # 打印接收到的报文
#     i += 1

# ret = dll.CloseDevice(nDeviceType, nDeviceInd)
# print("closedevice:", ret)


if __name__ == "__main__":
    pass

