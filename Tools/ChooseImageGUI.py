# -*-coding:utf-8
import os, shutil

import wx

import FileOperate as fo


class MainFrame(wx.Frame):
    def __init__(self):
        self.IsSelected = False
        self.srcdir = os.path.abspath('.')
        self.imagecount = 0
        self.classes = ('hands', 'kiss', 'hug')

        wx.Frame.__init__(self, None, title=u"人工图像分类器", size=(800, 600), pos=(0, 0))
        panel = wx.Panel(self, -1)
        # -----------------文件夹选择--------------------------
        wx.StaticText(panel, -1, u"待分类文件夹：", size=(100, -1), pos=(0, 5))
        self.Information = wx.StaticText(panel, -1, size=(100, -1), pos=(400, 35))
        self.srcdirText = wx.TextCtrl(panel, -1, u"请选择", size=(500, -1), pos=(100, 0))
        self.dirButton = wx.Button(panel, -1, u"选择文件夹", pos=(600, 0))
        self.Bind(wx.EVT_BUTTON, self.On_dirButton_Click, self.dirButton)
        # -------------------展示图像--------------------------
        self.Imagepanel = wx.Panel(parent=panel, pos=(10, 70), size=(640, 480))
        image = wx.Image(os.path.join(self.srcdir, 'logo.jpg'), wx.BITMAP_TYPE_JPEG)
        image.Rescale(640, 480)
        temp = image.ConvertToBitmap()
        wx.StaticBitmap(self.Imagepanel, -1, temp)
        self.disButton = wx.Button(panel, -1, u"开始浏览", pos=(300, 30))
        self.Bind(wx.EVT_BUTTON, self.On_disButton_Click, self.disButton)
        # -------------------选择类别--------------------------
        self.prevButton = wx.Button(panel, -1, u"Prev", pos=(680, 200))
        self.clsButton1 = wx.Button(panel, -1, u"类别1", pos=(680, 250))
        self.clsButton2 = wx.Button(panel, -1, u"类别2", pos=(680, 300))
        self.clsButton3 = wx.Button(panel, -1, u"类别3", pos=(680, 350))
        self.nextButton = wx.Button(panel, -1, u"Next", pos=(680, 400))
        self.Bind(wx.EVT_BUTTON, self.On_prevBotton_Click, self.prevButton)
        self.Bind(wx.EVT_BUTTON, self.On_clsButton1_Click, self.clsButton1)
        self.Bind(wx.EVT_BUTTON, self.On_clsButton2_Click, self.clsButton2)
        self.Bind(wx.EVT_BUTTON, self.On_clsButton3_Click, self.clsButton3)
        self.Bind(wx.EVT_BUTTON, self.On_nextBotton_Click, self.nextButton)

    # ----------------------------显示函数------------------------------------------
    def disImage(self, label=1):
        if label == 1:
            imagename = self.imageset[self.imagecount]
            self.Information.SetLabel(imagename)
            self.ImageName = os.path.join(self.srcdir, imagename)
            image = wx.Image(self.ImageName, wx.BITMAP_TYPE_JPEG)
            image.Rescale(640, 480)
            temp = image.ConvertToBitmap()
            wx.StaticBitmap(self.Imagepanel, -1, temp)
            self.imagecount = self.imagecount + 1
        else:
            if self.imagecount > 1:
                self.imagecount = self.imagecount - 2
                imagename = self.imageset[self.imagecount]
                self.Information.SetLabel(imagename)
                self.ImageName = os.path.join(self.srcdir, imagename)
                image = wx.Image(self.ImageName, wx.BITMAP_TYPE_JPEG)
                image.Rescale(640, 480)
                temp = image.ConvertToBitmap()
                wx.StaticBitmap(self.Imagepanel, -1, temp)

    # ----------------------------响应函数------------------------------------------
    def On_dirButton_Click(self, event):
        dlg = wx.DirDialog(self, u"选择", defaultPath=self.srcdir, style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.srcdir = dlg.GetPath()
            self.IsSelected = True
            self.Information.SetLabel('')
        dlg.Destroy()
        self.srcdirText.SetValue(self.srcdir)

    def On_disButton_Click(self, event):
        if self.IsSelected == True:
            for dirname in self.classes:
                fo.createclass(self.srcdir, dirname)
            self.clsButton1.SetLabel(self.classes[0])
            self.clsButton2.SetLabel(self.classes[1])
            self.clsButton3.SetLabel(self.classes[2])
            self.imageset = fo.readfile(self.srcdir)
            self.disImage()
        else:
            self.Information.SetLabel(u"请先选择文件夹")

    def On_clsButton1_Click(self, event):
        dstPath = os.path.join(self.srcdir, self.classes[0])
        shutil.copy(self.ImageName, dstPath)
        self.disImage()

    def On_clsButton2_Click(self, event):
        dstPath = os.path.join(self.srcdir, self.classes[1])
        shutil.copy(self.ImageName, dstPath)
        self.disImage()

    def On_clsButton3_Click(self, event):
        dstPath = os.path.join(self.srcdir, self.classes[2])
        shutil.copy(self.ImageName, dstPath)
        self.disImage()

    def On_nextBotton_Click(self, event):
        self.disImage()

    def On_prevBotton_Click(self, event):
        self.disImage(0)


if __name__ == '__main__':
    app = wx.App()
    frame = MainFrame()
    frame.Show()
    app.MainLoop()
