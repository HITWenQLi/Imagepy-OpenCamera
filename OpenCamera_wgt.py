import numpy as np             # 数据处理的库numpy
import cv2                     # 图像处理的库OpenCv
import wx                      # 构造显示界面的GUI
from imagepy import root_dir
#from widgets import ViewPort as ViewPortCtrl
import time

COVER = root_dir + '/data' + '/camera.png'
class Plugin ( wx.Panel ):
    title = 'Open Camera'
    single = None
    def __init__(self, parent, app):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(700, 700))
        self.app = app
        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        self.image_cover = wx.Image(COVER, wx.BITMAP_TYPE_ANY).Scale(350, 300)
        # 显示图片在panel上
        self.bmp = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(self.image_cover))
        self.start_button = wx.Button(self, wx.ID_ANY, u"Start", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT)
        self.close_button = wx.Button(self, wx.ID_ANY, u"close", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT)
        self.photo_button = wx.Button(self, wx.ID_ANY, u"photo", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT)
        self.startrecord_button = wx.Button(self, wx.ID_ANY, u"start record", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT)
        self.endrecord_button = wx.Button(self, wx.ID_ANY, u"end record", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT)
        self.grid_bag_sizer = wx.GridBagSizer(hgap=5, vgap=5)
        # 注意pos里面是先纵坐标后横坐标
        self.grid_bag_sizer.Add(self.bmp, pos=(0, 0), flag=wx.ALL | wx.EXPAND, span=(4, 4), border=5)
        self.grid_bag_sizer.Add(self.start_button, pos=(4, 1), flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, span=(1, 1), border=5)
        self.grid_bag_sizer.Add(self.close_button, pos=(4, 2), flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, span=(1, 1), border=5)
        self.grid_bag_sizer.Add(self.photo_button, pos=(4, 3), flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, span=(1, 1), border=5)
        self.grid_bag_sizer.Add(self.startrecord_button, pos=(5, 1), flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, span=(1, 1), border=5)
        self.grid_bag_sizer.Add(self.endrecord_button, pos=(5, 2), flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, span=(1, 1), border=5)
        self.grid_bag_sizer.AddGrowableCol(0, 1)
        # grid_bag_sizer.AddGrowableCol(0,2)

        self.grid_bag_sizer.AddGrowableRow(0, 1)
        self.SetSizer(self.grid_bag_sizer)
        self.grid_bag_sizer.Fit(self)
        self.start_button.Bind(wx.EVT_BUTTON, self.start_camera)
        self.close_button.Bind(wx.EVT_BUTTON, self.close_camera)
        self.photo_button.Bind(wx.EVT_BUTTON, self.photo)
        # self.startrecord_button.Bind(wx.EVT_BUTTON, self.record)


    def _start_camera(self, event):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 480)
        self.cnt = 0
        while(self.cap.isOpened()):
            flag, self.im_rd = self.cap.read()
            self.k = cv2.waitKey(1)
            height, width = self.im_rd.shape[:2]
            image1 = cv2.cvtColor(self.im_rd, cv2.COLOR_BGR2RGB)
            pic = wx.Bitmap.FromBuffer(width, height, image1)
            # 显示图片在panel上
            self.bmp.SetBitmap(pic)
            #self.grid_bag_sizer.Fit(self)
        self.cap.release()
    def start_camera(self, event):
        print('This is Start')
        import _thread
        _thread.start_new_thread(self._start_camera, (event,))

    def close_camera(self, event):
        print('This is Close')
        self.cap.release()
        self.bmp.SetBitmap(wx.Bitmap(self.image_cover))
        #self.grid_bag_sizer.Fit(self)

    def photo(self, event):
        now = time.time()
        # 格式化年月日时分秒
        local_time = time.localtime(now)
        date_format_localtime = time.strftime('%Y-%m-%d-%H-%M-%S', local_time)
        filename = root_dir + '/data/' + str(date_format_localtime) +'.jpg'
        print(filename)
        cv2.imwrite(filename, self.im_rd)
'''
    def _record(self, event):
        self.cap = cv2.VideoCapture(0)
        fps = self.cap.get(cv2.CAP_PROP_FPS)  # 获取帧率
        width_1 = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # 一定要转int 否则是浮点数
        height_1 = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        size = (width_1, height_1)  # 大小
        VWirte = cv2.VideoWriter('123asd.avi', cv2.VideoWriter_fourcc('I', '4', '2', '0'), fps,
                                size)  # 初始化文件写入 文件名 编码解码器 帧率 文件大小
        success, frame = self.cap.read()  # 只写10帧
        numFramesRemaining = 10 * fps  # z
        while success and numFramesRemaining:
            VWirte.write(frame)
            success, frame = self.cap.read()
            numFramesRemaining -= 1
        time.sleep(1)  # y延迟一秒关闭摄像头 否则会出现 terminating async callback 异步处理错误
        #self.cap.release()  # 释放摄像头
        print('ok')
    def record(self, event):
        import _thread
        _thread.start_new_thread(self._record, (event,))
'''




