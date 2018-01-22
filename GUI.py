# -*-coding:utf-8
import os

import wx

import TrainNet, TestNet
import RuleOperate as ro


class MainFrame(wx.Frame):
    def __init__(self):
        self.IsSelected = False
        self.srcdir = os.path.abspath('.')
        wx.Frame.__init__(self, None, title=u"社交网络图像隐私决策系统", size=(800, 600), pos=(0, 0))
        panel = wx.Panel(self, -1)
        # -----------------文件夹选择--------------------------
        wx.StaticText(panel, -1, u"待训练图像文件夹：", size=(150, -1), pos=(50, 10))
        self.srcdirText = wx.TextCtrl(panel, -1, u"请选择", size=(300, -1), pos=(200, 5))
        self.dirButton = wx.Button(panel, -1, u"选择文件夹", pos=(600, 5))
        self.Bind(wx.EVT_BUTTON, self.On_dirButton_Click, self.dirButton)
        # -------------------训练模型--------------------------
        self.TrainButton = wx.Button(panel, -1, u"开始训练", pos=(325, 50))
        self.Bind(wx.EVT_BUTTON, self.On_trainButton_Click, self.TrainButton)
        # -------------------测试模型--------------------------
        wx.StaticText(panel, -1, u"语义规则文件：", size=(150, -1), pos=(50, 205))
        self.ruleText = wx.TextCtrl(panel, -1, u"请选择", size=(500, -1), pos=(150, 200))
        self.RuleButton = wx.Button(panel, -1, u"选择语义规则文件", pos=(300, 150))
        self.TestButton = wx.Button(panel, -1, u"图像隐私检测", pos=(600, 400))
        self.BenchButton = wx.Button(panel, -1, u"性能测试", pos=(610, 450))
        self.Imagepanel = wx.Panel(parent=panel, pos=(50, 250), size=(400, 300))
        image = wx.Image(os.path.join(self.srcdir, 'logo.jpg'), wx.BITMAP_TYPE_JPEG)
        image.Rescale(400, 300)
        temp = image.ConvertToBitmap()
        wx.StaticBitmap(self.Imagepanel, -1, temp)
        self.Bind(wx.EVT_BUTTON, self.On_ruleButton_Click, self.RuleButton)
        self.Bind(wx.EVT_BUTTON, self.On_testButton_Click, self.TestButton)
        self.Bind(wx.EVT_BUTTON, self.On_benchButton_Click, self.BenchButton)

    # ----------------------------响应函数------------------------------------------
    def On_dirButton_Click(self, event):
        dlg = wx.DirDialog(self, u"选择待训练的图像文件夹", defaultPath=self.srcdir, style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.srcdir = dlg.GetPath()
            self.IsSelected = True
        dlg.Destroy()
        self.srcdirText.SetValue(self.srcdir)

    def On_trainButton_Click(self, event):
        if self.IsSelected == True:
            prototxt = "bvlc_reference_caffenet/finetune-train_val.prototxt"
            wx.MessageBox(u"模型训练时间较长,您是否真的要训练模型?", u"提示", wx.ICON_INFORMATION)
            TrainNet.TrainCaffeNet(prototxt, 2)
            self.IsSelected = False
        else:
            wx.MessageBox(u"请先选择文件夹", u"提示", wx.ICON_INFORMATION)

    def On_ruleButton_Click(self, event):
        dlg = wx.FileDialog(self, u"选择规则文件", os.getcwd(), style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.ruletext = dlg.GetPath()
            self.IsSelected = True
        dlg.Destroy()
        self.ruleText.SetValue(self.ruletext)

    def On_testButton_Click(self, event):
        if self.IsSelected == True:
            dlg = wx.FileDialog(self, u"选择待检测的图像", os.path.join('..', 'data', 'demo'), style=wx.DD_DEFAULT_STYLE)
            if dlg.ShowModal() == wx.ID_OK:
                imgdir = dlg.GetPath()
            dlg.Destroy()
            im_names = []
            im_names.append(os.path.split(imgdir)[1])
            image = wx.Image(imgdir, wx.BITMAP_TYPE_JPEG)
            image.Rescale(400, 300)
            temp = image.ConvertToBitmap()
            wx.StaticBitmap(self.Imagepanel, -1, temp)
            wx.MessageBox(u"您确定要检测这幅图像?", u"提示", wx.YES_NO | wx.NO_DEFAULT | wx.ICON_INFORMATION)
            contents = TestNet.TestImage(im_names, 'gpu')
            title, rules = ro.ReadRules(self.ruletext)
            Action, Level, Line = ro.Compare(contents, rules)
            print Action, Level
            if 'Deny' == Action:
                if '7' == Level:
                    wx.MessageBox(u"触发规则,拦截", u"警告", wx.ICON_EXCLAMATION)
                if '3' == Level:
                    wx.MessageBox(u"触发规则,警告", u"警告", wx.ICON_QUESTION)
        else:
            wx.MessageBox(u"请先选择规则文件", u"提示", wx.ICON_INFORMATION)

    def On_benchButton_Click(self, event):
        TestNet.BenchMark()


if __name__ == '__main__':
    app = wx.App()
    frame = MainFrame()
    frame.Show()
    app.MainLoop()
