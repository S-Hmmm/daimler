import os
import sys

import wx
import win32api

from ncm_transfer import dump

APP_TITLE = u'cnm transfer'
APP_ICON = 'audacity.ico'


class MainFrame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, -1, APP_TITLE, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        self.SetBackgroundColour(wx.Colour(224, 224, 224))
        self.SetSize((800, 600))
        self.Center()

        if hasattr(sys, 'frozen') and getattr(sys, 'frozen') == 'windows_exe':
            exe_name = win32api.GetModuleFileName(win32api.GetModuleHandle(None))
            icon = wx.Icon(exe_name, wx.BITMAP_TYPE_ICO)
        else:
            icon = wx.Icon(APP_ICON, wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        # self.file_name = wx.TextCtrl(self, pos=(5, 5), size=(230, 230))
        self.file_ls = None
        panel = wx.Panel(self, -1)

        self.select_file_button = wx.Button(panel, label=u'选择文件', pos=(680, 10), size=(100, 35))
        self.select_file_button.Bind(wx.EVT_BUTTON, self.open_file)

        self.transfer_button = wx.Button(panel, label=u'转换格式', pos=(680, 50), size=(100, 35))
        self.transfer_button.Bind(wx.EVT_BUTTON, self.transfer_file)

        self.file_names = wx.StaticBox(panel, wx.ID_ANY, pos=(10, 10), size=(660, 600), style=wx.ALIGN_LEFT)

    def open_file(self, event):
        wildcard = 'cnm files(*.cnm)|*.*'
        dialog = wx.FileDialog(None, message=u'选择cnm文件', defaultDir=os.getcwd(), wildcard=wildcard,
                               style=wx.FD_OPEN | wx.FD_MULTIPLE)
        if dialog.ShowModal() == wx.ID_OK:
            names = ''
            for pth in dialog.GetPaths():
                names += (pth + '\n')
            self.file_names.SetLabel(names)
            self.file_ls = dialog.GetPaths()
            dialog.Destroy()

    def transfer_file(self, event):
        if self.file_ls:
            for file in self.file_ls:
                try:
                    dump(file)
                except Exception as e:
                    print(e)
            self.file_names.SetLabel('转换完成')
            op_dir = os.path.join(os.path.dirname(self.file_ls[0]), 'ncm_transfer')
            if op_dir:
                os.startfile(op_dir)
        else:
            self.file_names.SetLabel('请选择要转换的文件')
        # TODO


class MainApp(wx.App):
    def OnInit(self):
        self.SetAppName(APP_TITLE)
        self.Frame = MainFrame()
        self.Frame.Show()
        return True


if __name__ == '__main__':
    app = MainApp()
    app.MainLoop()
