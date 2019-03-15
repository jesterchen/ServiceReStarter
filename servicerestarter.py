import wx
import subprocess


def get_service_status(svcname):
    cp = subprocess.run(["sc", 'query', svcname], capture_output=True)
    if cp.returncode == 0:
        if str(cp.stdout).find('STOPPED') != -1:
            return 'stopped'
        elif str(cp.stdout).find('RUNNING') != -1:
            return 'running'
    return 'unknown'


def stop_service(svcname):
    # print("stopping {}".format(svcname))
    subprocess.run(['net', 'stop', svcname], capture_output=True)


def start_service(svcname):
    # print("starting {}".format(svcname))
    subprocess.run(['net', 'start', svcname], capture_output=True)


class Example(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(Example, self).__init__(*args, **kwargs)
        self.cbs = []
        self.btn_stop = wx.Button()
        self.btn_start = wx.Button()
        self.init_ui()

    def init_ui(self):
        pnl = wx.Panel(self)
        data = load_data()

        offset = 10
        for d in data:
            self.cbs.append(wx.CheckBox(pnl, label=d[1], pos=(10, offset), name=d[0]))
            offset += 30

        self.set_checkbox_colors(self.cbs)
        self.btn_stop = wx.Button(pnl, label="Stop", pos=(10, offset))
        self.btn_start = wx.Button(pnl, label="Start", pos=(100, offset))
        self.btn_stop.Bind(wx.EVT_BUTTON, self.btn_clicked)
        self.btn_start.Bind(wx.EVT_BUTTON, self.btn_clicked)
        # todo: implement restart with proper checking for stop and start, perhaps red/green blinking label
        # self.btn_restart = wx.Button(pnl, label="Restart", pos=(190, offset))
        # self.btn_restart.Bind(wx.EVT_BUTTON, self.btn_clicked)

        self.SetSize(305, offset + 80)
        self.SetTitle('Service ReStarter')
        self.Centre()

    @staticmethod
    def set_checkbox_colors(cbs):
        # todo: do this every second, update gui accordingly
        color_switcher = {
            'running': (0, 100, 0),
            'stopped': (100, 0, 0),
            'unknown': (200, 200, 200)
        }
        for cb in cbs:
            state = get_service_status(cb.GetName())
            cb.SetForegroundColour(wx.Colour(color_switcher.get(state)))
            if state == 'unknown':
                cb.Disable()
            else:  # for the todo, not needed otherwise
                cb.Enable()

    def btn_clicked(self, event):
        service_switcher = {
            'Stop': stop_service,
            'Start': start_service
        }
        for cb in self.cbs:
            if cb.IsEnabled():
                if cb.GetValue():
                    func = service_switcher.get(event.GetEventObject().GetLabel())
                    func(cb.GetName())


def main():
    app = wx.App()
    ex = Example(None)
    ex.Show()
    app.MainLoop()


def load_data():
    try:
        with open('services.txt') as service_file:
            data = eval(service_file.read())
    except EnvironmentError:  # parent of IOError, OSError *and* WindowsError where available
        print('Could not open services.txt.')
        raise
    try:
        assert (isinstance(data, list))
    except AssertionError:
        print("Contents of services.txt are not in list format. See services.txt_sample.")
        raise
    return data


if __name__ == '__main__':
    main()
