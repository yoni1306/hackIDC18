import win32service
import win32event
import servicemanager
import socket
import win32serviceutil
from DatakServerSide import DatakServerSide


class AppServerSvc(win32serviceutil.ServiceFramework):
    _svc_name_ = 'Datak_ServerSide'
    _svc_display_name_ = 'DatakServerSide'

    def __init__(self, args):
        """
        This function initiate the system.
        @param args: windows-service`s params.
        """
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        self.server = DatakServerSide()

    def SvcStop(self):
        """
        Stop the Datak_ServerSide service.
        """
        self.server.stop_server()
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STOPPED,
                              (self._svc_name_, ''))
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        """
        Run the Datak_ServerSide service.
        """
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.server.run_server()

if '__main__' == __name__:
    win32serviceutil.HandleCommandLine(AppServerSvc)