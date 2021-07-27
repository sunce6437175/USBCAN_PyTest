import os


class cantype():
    can_type = "VCI_USBCAN_2E_U" #USBCAN设备类型
    TypeDefines1 = 3         #接口卡的类型USBCAN-I-3
    TypeDefines2 = 4         #接口卡的类型USBCAN-II-4
    nDeviceInd = 0           #索引号默认0代表设备个数
    nReserved = 0            #保留参数
    nCANInd = 1              #暂无意义参数
    Filter = 0               #滤波使能0=不使能，1=使能。使能时，请参照SJA1000验收滤波器设置验收码和屏蔽码
    AccCode = 0x00000000     #验收码":"SJA1000的帧率验收码 全部是0即可 0x00000000"
    AccMask = 0xffffffff     #屏蔽码":"SJA1000的帧过滤屏蔽码。屏蔽码推荐设置为0xFFFF FFFF，即全部接收
    baud_rate = 500          #波特率
    Mode = 0                 #模式=0为正常模式，=1为只听模式， =2为自发自收模式
    SendMode = 0             #发送方式=1普通单次模式，=2普通循环模式，=3指定时间发送模式,=4区间发送模式

# 1普通单次循环发送模式
class generalCirculatioMode():
    SendType = 0            #发送帧类型=1时为单次发送,=0为循环发送
    SetCANlist = {
        'CANa':'KL15ONandKLSON'
    }
# 2普通循环发送模式
class generalCirculatioModeAgain():
    SendTheNumber = 1000   #"发送次数":"eg:500次,1000次,无限次：LimitedTime"
    TimeBetweenTransmissions = 100  #"每次发送间隔时间-单位(ms)":"eg:50ms,100ms等"
    SendType = 0            #发送帧类型=1时为单次发送,=0为循环发送
    SetCANlist = {
        'CANa':'KL15ONandKLSON',
        "CANb":"Headlightopen"
    }
# Can信号模拟设备list
class canlist():
    # "车辆点火":"C0 00 43 00"
    KL15ONandKLSON = {
        "ID":0x000003C0,
        "SendType":0,
        "RemoteFlag":0,
        "ExternFlag":0,
        "DataLen":4,
        "Data":(192, 0, 67, 0),
        "Reserved":(0, 0, 0),
        "executivemode":"true"
    }
    # "车门关闭车辆熄火":"80 03 01 00"
    KL15OFFandKLSON = {
        "ID":0x000003C0,
        "SendType":0,
        "RemoteFlag":0,
        "ExternFlag":0,
        "DataLen":4,
        "Data":(128, 3, 1, 0),
        "Reserved":(0, 0, 0),
        "executivemode":"false"
    }
    # "车辆熄火锁车":"81 03 00 00"
    KL15OFFandKLSOFF = {
        "ID":0x000003C0,
        "SendType":0,
        "RemoteFlag":0,
        "ExternFlag":0,
        "DataLen":4,
        "Data":(129, 3, 0, 0),
        "Reserved":(0, 0, 0),
        "executivemode":"false"
    }
    # "大灯开":"FD 8A 0A FF FF 00 00 00"
    Headlightopen = {
        "ID":0x000005F0,
        "SendType":0,
        "RemoteFlag":0,
        "ExternFlag":0,
        "DataLen":8,
        "Data":(253, 138, 10, 255, 255, 0, 0, 0),
        "Reserved":(0, 0, 0),
        "executivemode":"true"
    }
    # "大灯关":"FD 00 0A FF FF 00 00 00"
    HeadlightClosed = {
        "ID":0x000005F0,
        "SendType":0,
        "RemoteFlag":0,
        "ExternFlag":0,
        "DataLen":8,
        "Data":(253, 0, 10, 255, 255, 0, 0, 0),
        "Reserved":(0, 0, 0),
        "executivemode":"false"
    }


'''以下是基本功能demo'''
# DLL通讯
# class Communication():
#     baud_rate_define = CanBaudrateDefines()
#     initconfig = VCI_INIT_CONFIG(0x00000000,0xffffffff, 0, 1, 0x00, 0x14, 0)#
#     vic.AccCode = 0x00000000     # 验收码，SJA1000的帧率验收码 全部是0即可 0x00000000
#     vic.AccMask = 0xffffffff     # 屏蔽码，SJA1000的帧过滤屏蔽码  推荐设置未 0Xffff ffff即为全部接受
#     vic.reserved = 0             # 保留
#     vic.Filter = 0               # 滤波使能。0=不使能，1=使能使能时，/请参照SJA1000验收滤波器设置验收码和屏蔽码。
#     vic.Timing0 = 0x00           # 500Kbps 波特率定时器0
#     vic.Timing1 = 0x1C           # 500Kbps 波特率定时器0
#     vic.Mode = 0                 # 模式。=0为正常模式，=1为只听模式， =2为自发自收模式


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
# vco = CAN_OBJ()
# # vco.ID = 0x00000055  # 帧的ID 默认demo
# vco.ID = 0x000003C0   # 帧的ID KL15,KLS 
# # vco.ID = 0x000005F0   # 帧的ID 大灯 
# vco.SendType = 1  # 发送帧类型，0是正常发送，1为单次发送，这里要选1！要不发不去！
# vco.RemoteFlag = 0
# vco.ExternFlag = 0
# vco.DataLen = 8

# 单独传参数 十六进制 →OK
# 传参数 十六进制  转到 十进制 →OK
#大灯关闭信号 FD 00 0A FF FF 00 00 00	
# vco.Data = (0xfd, 0x00, 0x0a, 0xff, 0xff, 0x00, 0x00, 0x00)
# vco.Data = (253, 0, 10, 255, 255, 0, 0, 0)

#大灯打开信号 FD 8A 0A FF FF 00 00 00  
# vco.Data = (0xfd, 0x8a, 0x0a, 0xff, 0xff, 0x00, 0x00, 0x00)
# vco.Data = (253, 138, 10, 255, 255, 0, 0, 0)    

# 车辆点火 C0 00 43 00
# vco.Data = (0xc0, 0x00, 0x2b, 0x00) 
# vco.Data = (192, 0, 67, 0)
# vco.Reserved = (0, 0, 0)


# 定义报文实例对象，用于接收
# vco2 = VCI_CAN_OBJ()
# vco2.ID = 0x00000001  # 帧的ID 后面会变成真实发送的ID
# vco2.SendType = 0  # 这里0就可以收到
# vco2.RemoteFlag = 0
# vco2.ExternFlag = 0
# vco2.DataLen = 8
# vco2.Data = (0, 0, 0, 0, 0, 0, 0, 0)
# vco2.Data = (0, 0, 0, 0)

'''设备的打开如果是双通道的设备的话，可以再用initcan函数初始化'''
# 步骤一 打开设备
# OpenDevice(设备类型号，设备索引号，参数无意义)
# ret = dll.OpenDevice(nDeviceType, nDeviceInd, nReserved)
# print("opendevice:", ret)

# 步骤二 执行参数初始化
# InitCAN(设备类型号，设备索引号，第几路CAN，初始化参数initConfig)，
# ret = dll.InitCAN(nDeviceType, nDeviceInd, 0, byref(vic))
# print("initcan0:", ret)

# 步骤三 打开对应CAN通道
# StartCAN(设备类型号，设备索引号，第几路CAN)
# ret = dll.StartCAN(nDeviceType, nDeviceInd, 0)
# print("startcan0:", ret)