import os


class cantype():
    can_type = "usb_can_2eu" #USBCAN设备类型
    nDeviceType1 = 3         #接口卡的类型USBCAN-I-3
    nDeviceType2 = 4         #接口卡的类型USBCAN-II-4
    nDeviceInd = 0           #索引号默认0代表设备个数
    nReserved = 0            #保留参数
    nCANInd = 1              #暂无意义参数
    Filter = 0               #滤波使能0=不使能，1=使能。使能时，请参照SJA1000验收滤波器设置验收码和屏蔽码
    AccCode = 0x00000000     #验收码":"SJA1000的帧率验收码 全部是0即可 0x00000000"
    AccMask = 0xffffffff     #屏蔽码":"SJA1000的帧过滤屏蔽码。屏蔽码推荐设置为0xFFFF FFFF，即全部接收
    baud_rate = 500          #波特率
    Mode = 0                 #模式=0为正常模式，=1为只听模式， =2为自发自收模式
    SendMode = 0             #发送方式=1普通单次模式，=2普通循环模式，=3指定时间发送模式,=4区间发送模式

class generalCirculatioMode():
    SendType = 0            #发送帧类型=1时为单次发送,=0为循环发送
    SetCANlist = {
        'CANa':'KL15ONandKLSON'
    }
class canlist():
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