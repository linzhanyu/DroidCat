# -*- coding:utf-8 -*-

# import subs
import RuntimeOS
import time, subprocess, os, re, threading, traceback, platform
from ADBTask import CmdTask, LoopTask
from config import Config
# from AndroidControl import AndroidControl

adb = os.path.join(Config.ADK, 'platform-tools', 'adb')

# subs.func0()
console = RuntimeOS.Console()
console.Title( u'天地无极 乾坤正法' )
# console.SetOutputCodepage( 65001 ) # UTF-8
if platform.system() == 'Windows':
    console.SetOutputCodepage( 936 ) # GBK
# console.SetOutputCodepage( 54936 ) # GB18030

console.Assert( '%s\n' % (adb, ) )
console.Assert( 'assert.\n' )
console.Error( 'error.\n' )
console.Warning( 'warning.\n' )
console.Info( 'info.\n' )
console.Debug( 'debug.\n' )
console.Verbose( 'verbose.\n' )

# ==================================================
pslist = []
# watch_pname = 'com.tencent.tmgp.sanguox'
# watch_pname = 'com.westhouse.sanguox.sogou'
# watch_pname = 'com.westhouse.bigsanguo'
# watch_pname = 'com.mpsoft.opencvdemo'
# watch_pname = 'com.freejoy.wasteland'
# watch_pname = 'com.kurokostudio.slg'
# watch_pname = 'com.yanfa.bleach'
watch_pname = Config.AppName
# watch_pname = 'com.kimi.beta.bleachtw'
# watch_pname = 'com.kunlun.bleach.mi'
# watch_pname = 'com.kunlun.bleach.kl'
# watch_pname = 'org.mushroom.camerademo'
watch_pid = None
watch_tid = None

logcat = None

# ==================================================
console.Info( '\n当前调试程序 : %s\n' % (watch_pname, ) )
console.Info( '请连接设备并启动要调试的程序  Ctrl+C 退出\n' )
time.sleep(3.0)
# console.clear()

# ==================================================
subProc = None
def SubProc( cmd, run_dir ):
    newEnv = os.environ.copy()
    newEnv['LC_MESSAGES'] = 'en'

    info = subprocess.STARTUPINFO()
    info.wShowWindow = False
    info.dwFlags=subprocess.SW_HIDE
    if os.name == 'nt':
        info.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    try:
        global subProc
        # Gui application
        subProc = subprocess.Popen(cmd, env=newEnv, cwd=run_dir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, startupinfo=info, shell=False)
        # Nongui application
        # subProc = subprocess.Popen(cmd, env=newEnv, cwd=run_dir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, startupinfo=info, shell=True)
    except OSError as e:
        print( 'Execute %s failed.' % (cmd[0],) )
        raise e

def KillSubProc() :
    global subProc
    if subProc != None :
        subProc.kill()
        subProc = None

def str2uni( strBuf ):
    l = strBuf
    try:
        l = strBuf.decode('utf-8')
    except UnicodeDecodeError as e:
        # print(type(strBuf), strBuf)
        try:
            l = strBuf.decode('gb18030')
        except UnicodeDecodeError as e:
            try:
                l = strBuf.decode('big5')
            except UnicodeDecodeError as e:
                return ''
            pass
    return l


# class AndroidLogCat( AndroidControl ):
class AndroidLogCat( ):
    def __init__(self):
        # AndroidControl.__init__(self)
        self.proc = None
        pass

    def GetAllProcess(self):
        return [self.proc, ]

    keywords = ['MonoHeapSize', 'Async :', 'Sync :', ' -> ', ]
    def CaptureLog( self, device, pid ):
        global adb
        # adb = r'D:\android\sdk\platform-tools\adb.exe'
        # adb = r'D:\android\platform-tools\adb.exe'
        cmd = [adb, ]
        cmd.extend( 'shell logcat -v thread'.split(' ') )
        print( cmd )
        self.proc = RuntimeOS.SubProcess( cmd, '.', shell=False )
        # console = RuntimeOS.Console()
        self.proc.run()

        print( self.proc.stdout )

        with open( watch_pname+'.log', 'wb' ) as f:
            with open( watch_pname+'.all.log', 'wb' ) as f1:
                for line in iter(self.proc.stdout.readline, b''):
                    l = str2uni(line)
                    try:
                        if 'obtainBuffer' not in l:
                            self.showLog(l)
                    except TypeError as e :
                        print( type(l) )
                        print( l )
                        raise e
                    for keyword in AndroidLogCat.keywords:
                        if keyword in l:
                            f.write( bytes(l, encoding='utf-8') )
                    t = time.localtime()
                    f1.write( bytes( time.strftime("%H:%M:%S", t), encoding='utf-8' ) )
                    f1.write( bytes(l, encoding='utf-8') )
                f1.flush()
            f.flush()

    def showLog( self, line ):
        try:
            m = re.match(r'(\w)\(\s*(\d+):\s*(\d+)\)\s*(.*)', line)
        except TypeError as e:
            return 

        if m != None :
            # print( m.group(1), m.group(2), m.group(3), m.group(4) )
            pid = int(m.group(2))
            if pid != watch_pid :
                return

            key = m.group(1)
            l = '%5d:%5d %s' % ( int(m.group(2)), int(m.group(3)), m.group(4) )
            if key == 'A':
                console.Assert(l)
            elif key == 'E':
                console.Error(l)
            elif key == 'W':
                console.Warning(l)
            elif key == 'D':
                console.Debug(l)
            elif key == 'I':
                console.Info(l)
            elif key == 'V':
                console.Verbose(l)
        # console.Debug(l)

class TaskThread( threading.Thread ):
    def __init__( self ):
        threading.Thread.__init__( self )
        self.locker = threading.Lock()
        self.event  = threading.Event()
        self.running = True
        self.taskList = []

    def AddTask( self, task ) :
        self.locker.acquire()
        self.taskList.append( task )
        self.locker.release()

    def __DelTask( self, index ):
        self.locker.acquire()
        del self.taskList[index]
        self.locker.release()

    def stop( self ):
        self.running = False

    def run( self ):
        try :
            while self.running:
                if self.event.wait( 0.5 ):
                    pass
                else:
                    idx = 0

                    self.locker.acquire()
                    while idx < len( self.taskList ):
                        if not self.running:
                            break

                        task = self.taskList[idx]
                        task.Execute()
                        if task.isFinish():
                            self.__DelTask( idx )
                        else:
                            idx += 1

                    self.locker.release()
                time.sleep(0.1)
        except Exception as e:
            traceback.print_exc()
            raise e


# 还需要添加的功能
# 枚举包
# 多进程


# SubProc( 'notepad.exe', '.' )

def PIDFilter( output ):
    if output == None :
        return

    pslist.clear()
    for line in iter(output.readline, b''):
        l = str2uni(line)
        procInfo = l.split()
        pslist.append( procInfo )

        if procInfo[-1] == watch_pname :
            pid = int(procInfo[1])
            __ChangeLogcatPID( pid )

def __ChangeLogcatPID( pid ):
    global watch_pid
    global logcat
    if watch_pid != pid:
        watch_pid = pid
        print( 'PID : %d' % (pid, ) )
        # 重启 Logcat 进程
        if logcat != None: 
            logcat.proc.kill()
        logcat = AndroidLogCat()
        logcat.CaptureLog(None, None)


def Logcat():
    thread = TaskThread()
    try: 
        thread.start()

        # adb = r'D:\android\sdk\platform-tools\adb.exe'
        global adb
        cmd = [adb, ]
        cmd.extend( 'shell ps'.split(' ') )
        task = CmdTask( RuntimeOS.SubProcess( cmd, '.', shell=False ), PIDFilter )

        loopTask = LoopTask( task, 0.5 )
        thread.AddTask( loopTask )

        # logcat = AndroidLogCat()
        # logcat.CaptureLog(None, None)
        while True:
            thread.join(1.0)
            if thread.is_alive():
                time.sleep(0.5)
            else:
                break
    except KeyboardInterrupt as e :
        # traceback.print_exc()
        console.Verbose('\n')
        console.Verbose('清理环境... 这就退出.\n')
        console.Verbose('     Happy fun.\n')
        console.Verbose('     Author : linzhanyu@gmail.com\n')
        console.resetColor()
        thread.stop()
        thread.join()
    except Exception as e:
        traceback.print_exc()

    finally:
        exit(0)


# def Logcat():
#     try:
#         thread = TaskThread()
#         thread.start()
#         logcat = AndroidLogCat()
#         logcat.CaptureLog(None, None)
#         thread.join()
#     except KeyboardInterrupt as e:
#         console.resetColor()
#         thread.stop()


# proc = RuntimeOS.SubProcess( 'notepad.exe', '.', shell=False )
# proc.run()
# 
# 
# time.sleep(10)

# KillSubProc()



