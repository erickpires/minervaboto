#!/usr/bin/env python3

from minervaboto import renew_books, renewed_to_string, utils
from multiprocessing import Process, Queue

import os
import wx
import wx.lib.dialogs

class RenewTask(Process):
    def __init__(self, queue, user_id, user_password):
        Process.__init__(self)

        self.queue = queue
        self.user_id = user_id
        self.user_password = user_password

    def run(self):
        renewed = renew_books(self.user_id, self.user_password,
                              status_callback=self.OnNewStatus)
        self.queue.put(renewed)

    def OnNewStatus(self, status, progress):
        self.queue.put({'status': status, 'progress': progress})

class StatusBar(wx.StatusBar):
    def __init__(self, parent):
        wx.StatusBar.__init__(self, parent, -1)
        self.SetFieldsCount(2)
        self.SetStatusWidths([-1, -1])

        self.SetStatusText('Pronto', 0)

        self.gauge = wx.Gauge(self, -1, 100, size=(158, -1))
        self.OnResize(None)
        self.gauge.Show(False)

        self.Bind(wx.EVT_SIZE, self.OnResize)

    def OnResize(self, event):
        field_rect = self.GetFieldRect(1)
        gauge_rect = self.gauge.GetRect()

        width_diff = field_rect.width - gauge_rect.width
        field_rect.width = gauge_rect.width
        field_rect.x += width_diff - 3

        field_rect.height = 14
        field_rect.y = 5

        self.gauge.SetRect(field_rect)

class LoginWindow(wx.Frame):
    def __init__(self, title, user_id='', user_pass='',
                 config=None, config_file=None, has_config=False):
        wx.Frame.__init__(
            self, None, -1, title,
            style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX
        )

        self.config = config
        self.config_file = config_file
        self.has_config = has_config
        self.process = None
        self.queue = Queue()

        self.panel = wx.Panel(self)

        sizer = wx.GridBagSizer(5, 5)

        logo = wx.StaticBitmap(self.panel, -1,
                               wx.Bitmap('logo.png', wx.BITMAP_TYPE_ANY))
        sizer.Add(logo, pos=(0, 0), span=(1, 5), border=20,
                  flag=wx.ALIGN_CENTER_HORIZONTAL | wx.ALL)

        label_id = wx.StaticText(self.panel, label='ID/CPF')
        sizer.Add(label_id, pos=(1, 0),
                  flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border=10)

        self.input_id = wx.TextCtrl(self.panel, value=user_id)
        self.Bind(wx.EVT_TEXT, self.OnInputChange, self.input_id)
        sizer.Add(self.input_id, pos=(1, 1), span=(1, 4),
                  flag=wx.RIGHT | wx.EXPAND, border=10)

        label_pass = wx.StaticText(self.panel, label='Senha')
        sizer.Add(label_pass, pos=(2, 0),
                  flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border=10)

        self.input_pass = wx.TextCtrl(self.panel, value=user_pass,
                                      style=wx.TE_PASSWORD)
        self.Bind(wx.EVT_TEXT, self.OnInputChange, self.input_pass)
        sizer.Add(self.input_pass, pos=(2, 1), span=(1, 4),
                  flag=wx.RIGHT | wx.EXPAND, border=10)

        self.check_save = wx.CheckBox(self.panel, label='Salvar dados')
        self.check_save.SetValue(has_config)
        sizer.Add(self.check_save, pos=(3, 1), span=(1,1))

        self.button_renew = wx.Button(self.panel, label='Renovar')
        self.Bind(wx.EVT_BUTTON, self.OnRenewClick, self.button_renew)
        self.button_renew.SetDefault()
        sizer.Add(self.button_renew, pos=(4, 4), span=(1, 1),
                  flag=wx.BOTTOM | wx.RIGHT | wx.ALIGN_RIGHT, border=10)
        self.OnInputChange(None)

        sizer.AddGrowableCol(2)

        vbox = wx.BoxSizer(wx.VERTICAL)
        self.panel.Sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.panel.Sizer.Add(sizer, flag=wx.CENTER | wx.BOTTOM | wx.EXPAND,
                             border=30 if wx.Platform == '__WXMSW__' else 0)
        vbox.Add(self.panel, flag=wx.CENTER)
        self.SetSizer(vbox)
        self.panel.Sizer.Fit(self)

        self.status = StatusBar(self)
        self.SetStatusBar(self.status)

        self.Show(True)
        self.Bind(wx.EVT_CLOSE, self.OnWindowClose)

    def OnInputChange(self, event):
        if (self.input_id.GetValue().isdigit() and
            len(self.input_pass.GetValue()) > 0):
            self.button_renew.Enable()
        else:
            self.button_renew.Disable()

    def OnRenewClick(self, event):
        for child in self.panel.GetChildren():
            if not isinstance(child, wx.StaticBitmap):
                child.Disable()
        self.status.gauge.Show(True)

        self.process = RenewTask(self.queue, self.input_id.GetValue(),
                                 self.input_pass.GetValue())
        self.process.start()
        self.OnTimer()

    def OnTimer(self):
        if self.queue.empty():
            wx.CallLater(15, self.OnTimer)
            return

        result = self.queue.get(0)
        if 'status' in result:
            self.SetStatusText(result['status'], 0)
            self.status.gauge.SetValue(result['progress'])
            wx.CallLater(15, self.OnTimer)
            return

        self.FinishedRenewal(result)

    def OnWindowClose(self, event):
        if self.process: self.process.terminate()
        event.Skip()

    def FinishedRenewal(self, renewed):
        for child in self.panel.GetChildren():
            if not isinstance(child, wx.StaticBitmap):
                child.Enable()
        self.status.gauge.Show(False)
        self.status.gauge.SetValue(0)
        self.SetStatusText('Pronto', 0)

        if renewed['result']:
            result_list = renewed_to_string(renewed, True)
            dialog = wx.lib.dialogs.ScrolledMessageDialog(
                self, result_list[0], result_list[1], size=(480, 300)
            )
        else:
            if renewed['response']['code'] == 200:
                icon = wx.ICON_INFORMATION
            else:
                icon = wx.ICON_ERROR
            dialog = wx.MessageDialog(self, renewed['response']['message'],
                                      'Renovação', wx.OK | wx.CENTRE | icon)

        dialog.CenterOnParent(wx.BOTH)
        dialog.ShowModal()
        dialog.Destroy()

        if renewed['response']['code'] != 401:
            self.SaveCredentials()

        self.input_id.SetFocus()

    def SaveCredentials(self):
        if self.check_save.GetValue():
            self.config['LOGIN']['MINERVA_ID'] = self.input_id.GetValue()
            self.config['LOGIN']['MINERVA_PASS'] = self.input_pass.GetValue()
        else:
            self.config['LOGIN']['MINERVA_ID'] = ''
            self.config['LOGIN']['MINERVA_PASS'] = ''

        if self.has_config or self.check_save.GetValue():
            utils.write_config_file(self.config, self.config_file)

if __name__ == '__main__':
    title = 'Renovação Minerva'

    config_file = utils.get_default_config_file('minervaboto', 'boto.conf')
    config = utils.read_config_file(config_file)
    user_id, user_pass = utils.get_info_from_config(config)
    if (os.path.exists(config_file) and user_id and user_pass):
        has_config = True
    else:
        has_config = False

    app = wx.App(False)
    LoginWindow(title, user_id, user_pass, config, config_file, has_config)
    app.MainLoop()