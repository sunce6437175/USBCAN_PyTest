from _typeshed import Self
from ctypes import *
# from posix import PRIO_PGRP
import time,ctypes,os,sys,json
import setting
'''
通过灯来判断状态00:58 power can1 can2    
DLL库 基于vb.net 开发
config.json 配置参数
函数库调用流程
openDecice 打开设备 → InitCan 初始化某一路CAN → StartCAN 启动某一路CAN → Transmit (发送CAN帧) → Close Device 关闭设备
                                                                       Receive (读取CAN帧)
'''

# dll库类
class keydll:
    dllName = "ECANVCI库文件64位/ECanVci64.dll"
    # 配置项地址获取(获取当前文件的绝对路径)
    dllPath = os.path.join(os.path.abspath(os.path.dirname(__file__)),dllName).replace("\\",'/')
# 调用dll文件
dll = ctypes.windll.LoadLibrary(keydll.dllPath)  

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

# 1.3.2 定义发送报文的结构体 CAN_OBJ 结构体表示帧的数据结构。在发送函数Transmit和接收函数Receive中被用来传送CAN信息帧。
class VCI_CAN_OBJ(Structure):
    _fields_ = [("ID", c_uint),  # 报文帧ID'''
                ("TimeStamp", c_uint),  # 接收到信息帧时的时间标识
                ("TimeFlag", c_ubyte),  # 是否使用时间标识， 为1时TimeStamp有效
                # 工作模式
                ("SendType", c_ubyte),  # 发送帧类型。=0时为正常发送,=1时为单次发送（不自动重发)，/
                # =2时为自发自收（用于测试CAN卡是否损坏） ， =3时为单次自发自收（只发送一次， 用于自测试），/ 只在此帧为发送帧时有意义。

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

# 基于1.3.2 父类自创子类 定义发送报文的结构体 CAN_OBJ_SEND
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
# Can板类型定义
class CanBoardTypeDefines:
    VCI_USBCAN1 = 3
    VCI_USBCAN2 = 4

# 波特率可以定义
class CanBaudrateDefines:
    def get_baud_rate_group_3(self, baud_rate: int):
            try:
                if baud_rate == 10:
                    timing0 = 0x31
                    timing1 = 0x1c
                    return timing0,timing1
                elif baud_rate == 20:
                    timing0 = 0x18
                    timing1 = 0x1c
                    return timing0,timing1
                elif baud_rate == 40:
                    timing0 = 0x87
                    timing1 = 0xff
                    return timing0,timing1
                elif baud_rate == 50:
                    timing0 = 0x09
                    timing1 = 0x1c
                    return timing0,timing1
                elif baud_rate == 80:
                    timing0 = 0x83
                    timing1 = 0xff
                    return timing0,timing1
                elif baud_rate == 100:
                    timing0 = 0x04
                    timing1 = 0x1c
                    return timing0,timing1
                elif baud_rate == 125:
                    timing0 = 0x03
                    timing1 = 0x1c
                    return timing0,timing1
                elif baud_rate == 200:
                    timing0 = 0x81
                    timing1 = 0xfa
                    return timing0,timing1
                elif baud_rate == 250:
                    timing0 = 0x01
                    timing1 = 0x1c
                    return timing0,timing1
                elif baud_rate == 400:
                    timing0 = 0x80
                    timing1 = 0xfa
                    return timing0,timing1
                elif baud_rate == 500:
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
                    raise Exception("group3 group1 CAN卡所设置的波特率暂不被支持 波特率为"+ str(baud_rate))
            except Exception as e:
                raise e
    

class VcoV():
    def __init__(self,ID,SendType,RemoteFlag,ExternFlag,DataLen,Data,Reserved,executivemode):

        self.ID = ID
        self.SendType = SendType
        self.RemoteFlag = RemoteFlag
        self.ExternFlag = ExternFlag
        self.DataLen = DataLen
        self.Data = Data
        self.Reserved = Reserved
        self.executivemode = executivemode
    def go_1(self):
        return self.ID,self.SendType,self.RemoteFlag,self.ExternFlag,self.DataLen, \
            self.Data,self.Reserved,self.executivemode

class Communication():
    baud_rate_define = CanBoardTypeDefines()
    initconfig = VCI_INIT_CONFIG(0x00000000,0xffffffff, 0, 1, 0x00, 0x1c, 0)
    CanInfor = VCI_CAN_OBJ()
    setCantype = setting.cantype()

    def __init__(self,can_type=21,tds=3,ved=0,ind=0,Fr=0,AC=0x00000000,AM=0xffffffff,md=0):
        super().__init__()
        self.CanType = can_type    #USBCAN设备类型
        self.TypeDefines = tds     #接口卡的类型USBCAN-I-3,nDeviceType1 = 3 
        self.nDeserved = ved       #*保留参数
        self.nDeviceInd = ind      #*索引号默认0代表设备个数
        self.Filter = Fr           #*滤波使能0=不使能，1=使能。使能时，请参照SJA1000验收滤波器设置验收码和屏蔽码
        self.AccCode = AC          #*验收码":"SJA1000的帧率验收码 全部是0即可 0x00000000"
        self.AccMask = AM          #*屏蔽码":"SJA1000的帧过滤屏蔽码。屏蔽码推荐设置为0xFFFF FFFF，即全部接收
        self.config1,self.config2 = baud_rate_define.get_baud_rate_group_3(setCantype.baud_rate)   #*波特率解析time1和time2
        self.Mode = md             #*模式=0为正常模式，=1为只听模式， =2为自发自收模式
        self.run_flag = False      #用于控制运行线程

    def _error_msg(self,msg:str):
        return msg
    def _trans_can_type(self, typename: str):
        if typename.lower() == "usb_can_2eu":  # 姝ゅ搴斿綋鐢� re 鍘昏В鏋�
            return True, CanBoardTypeDefines.VCI_USBCAN_2E_U, "ok"

    def set_can_board_configuraion(self,can_type:str,can_idx:int,chn:int,baud_rate:int):
        try:
            if type(can_type) != str or type(chn) != int or type(baud_rate) != int:
                return False, self._error_msg(" InputType is not satisfied! At GetCANBoardConfigurtaion Function")
            if self.can_
        except Exception as e:
            raise e
            print(e)

class Configuraion():

    # 读取setting.py文件中的cantype
    def readConfig_cantype(self):
        setCantype = setting.cantype()
        self.nDeviceType1 = setCantype.nDeviceType1
        self.AccCode = setCantype.AccCode
        self.AccMask = setCantype.AccMask
        self.nReserved = setCantype.nReserved
        self.Fitter = setCantype.Filter
        self.nDeviceInd = setCantype.nDeviceInd
        self.baud_rate = setCantype.baud_rate
        self.Mode = setCantype.Mode

        return self.nDeviceType1,self.AccCode,self.AccMask,self.nReserved,self.Fitter,self.nDeviceInd,self.baud_rate,self.Mode

    # 定义一个用于初始化的实例对象vic
    def InitVic(self):
        self.vic = VCI_INIT_CONFIG()
        config = Configuraion()

        self.nDeviceType1,self.AccCode,self.AccMask,self.nReserved,self.Fitter,nDeviceInd,self.baud_rate,self.Mode = config.readConfig_cantype()
        baud_rateS = Configuraion.CanBoardTypeDefines()
        self.vic.Timing0,self.vic.Timing1 = baud_rateS.group1_baud_rate3(int(self.baud_rate))

        return self.vic

    # 读取config.json文件中的实现单次发送
    def Normal_one_Transmission_Mode(self):
        setMode = setting.generalCirculatioMode()
        setcanlist = setting.canlist()
        sMode = setMode.SendType
        # 单次模式判断sendMode =1 
        exmode = ''
        try:
            if sMode == 0:
                # # 发送帧类型，1为单次发送
                # self.SendType = sMode.SendType
                # self.SetCANlist = sMode.SetCANlist


                # tmp = self.SetCANlist.values()
                vcoKey = setcanlist.KL15ONandKLSON
                print(vcoKey)
                vco = VCI_CAN_OBJ()
                vco.ID = vcoKey['ID']
                vco.SendType = vcoKey['SendType']
                vco.RemoteFlag = vcoKey['RemoteFlag']
                vco.ExternFlag = vcoKey['ExternFlag']
                vco.DataLen =  vcoKey['DataLen']
                vco.Data = vcoKey['Data']
                vco.Reserved = vcoKey['Reserved']
                exmode = vcoKey['executivemode']
                # vco.ID,vco.SendType,vco.RemoteFlag,vco.ExternFlag,vco.DataLen,vco.Data,vco.Reserved,exmode = vcox.go_1()


                i = 1
                while i:
                    art = dll.Transmit(self.nDeviceType1,self.nDeviceInd, 0, byref(vco), 1)  # 发送vco

                    # ret = dll.Receive(nDeviceType, nDeviceInd, 0, byref(vco2), 1, 0)  # 以vco2的形式接收报文
                    time.sleep(1)  # 设置一个循环发送的时间
                    # if ret > 0:
                    #     print(i)
                    #     print(list(vco2.Data))  # 打印接收到的报文
                    i += 1

                ret = dll.CloseDevice(self.nDeviceType1,self.nDeviceInd)
                    # ret = dll.CloseDevice(int(nDeviceType1), int(DeviceInd))
                print("closedevice:", ret)



            else:
                print("SetCANlist中的can信号不在Can信号模拟设备list当中！")

                pass


            # elif sMode.SendType == 2:
            #     print("ERROR =2普通循环模式")
            #     # return timing0,timing1
            # elif sMode.SendType == 3:
            #     print("ERROR =3指定时间发送模式")
            #     # return timing0,timing1
            # else:
            #     raise Exception("发送模式为"+ str(sMode.SendType))

        except Exception as e:
            raise e
    # 关闭发送帧
    def Close(self):
        dll.CloseDevice(self.nDeviceType1,self.nDeviceInd)






if __name__ == "__main__":


    config = Configuraion()
    nDeviceType1,AccCode,AccMask,Reserved,Fitter,DeviceInd,baud_rate,Mode = config.readConfig_cantype()
    # 步骤一 打开设备 OpenDevice(设备类型号，设备索引号，参数无意义)
    print("下面执行操作返回“1”表示操作成功！")
    ret1 = dll.OpenDevice(int(nDeviceType1), int(DeviceInd), int(Reserved))
    print("打开设备状态码:", ret1)
    # 步骤二 执行参数初始化 InitCAN(设备类型号，设备索引号，第几路CAN，初始化参数initConfig)，
    vic = config.InitVic()
    ret2 = dll.InitCAN(int(nDeviceType1),int(DeviceInd), 0, byref(vic))
    print("初始化状态码:", ret2)
    # 步骤三 打开对应CAN通道 StartCAN(设备类型号，设备索引号，第几路CAN)
    ret3 = dll.StartCAN(int(nDeviceType1), int(DeviceInd), 0)
    print("启动状态码:", ret3)
    # 定义报文实例对象，用于发送

    config.Normal_one_Transmission_Mode()