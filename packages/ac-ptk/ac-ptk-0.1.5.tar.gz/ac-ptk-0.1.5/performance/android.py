import os
import re
import sqlite3
import subprocess
import time
import traceback
from time import sleep

from performance.config import WORK_DIR

from performance import DUMP_INTERVAL, mail, DB_NAME, db_helper, matlab_plt
from performance.db_helper import create_table_if_need
from performance.excelx import excelx
from performance.log import logd, tip
from performance.mail import Report
from performance.mem_history import History


def parse_mem(mem_str=""):
    mem = {'Total': 0}
    start = False
    for line in mem_str.splitlines():
        if line.strip() == "App Summary":
            start = True
            continue
        if not start:
            continue

        lines = re.split("\\s+", line.strip())
        if lines.__len__() < 2:
            continue
        if lines[0] == "TOTAL:":
            break
        value = lines[-1]
        lines.remove(value)
        key = " ".join(lines)
        mem[key] = int(value)
        mem['Total'] += mem[key]
    return mem


class AndroidApp:

    def __init__(self, pkg, series=None):
        self.run = True
        self.series = series
        self.pkg = pkg
        self.output = ''
        self.file_prefix = 'ptk_' + pkg + '_' + time.strftime('%Y%m%d%H%M%S')
        self.max = 0
        self.avg = 0
        self.duration = 0
        self.success = True
        self.ptk_crash_dir = None
        self.ptk_anr_dir = None
        self.crashes = 0
        self.conn = sqlite3.connect(DB_NAME)
        create_table_if_need(History(), self.conn)

    def __str__(self):
        return self.pkg

    def check_pkg(self):
        is_ok = False
        pkgs = self.get_all_pkgs()
        assert isinstance(pkgs, str)
        for pkg in pkgs.splitlines():
            pkg = pkg.split(":")[1]
            if pkg == self.pkg:
                is_ok = True
                break
        if not is_ok:
            raise Exception('%s is not a valid package name.' % self.pkg)

    def get_all_pkgs(self):
        return self.adb_shell("pm list packages")

    def get_memory(self):
        return parse_mem(self.adb_shell("dumpsys meminfo " + self.pkg))

    def adb_shell(self, command="", _shell=True, check=True):
        args = ['adb']
        if self.series is not None and self.series != '':
            args.append('-s')
            args.append(self.series)
        args.append('shell')
        args.append(command)
        # return shell(args, command, _shell, check)
        r = ''
        try:
            r = subprocess.check_output(' '.join(args), shell=_shell, encoding='utf-8')
        except UnicodeDecodeError as e:
            tip(e)
        except Exception as e:
            if check:
                raise e
            else:
                tip(e)
        return r

    def adb(self, command="", _shell=True, check=True):
        args = ['adb']
        if self.series is not None and self.series != '':
            args.append('-s')
            args.append(self.series)
        args.append(command)
        r = ''
        try:
            r = subprocess.check_output(' '.join(args), shell=_shell, encoding='utf-8')
        except Exception as e:
            if check:
                raise e
            else:
                tip(e)
        return r

    def monkey(self):
        tip("(%s) start monkey events..." % self.series)
        stop_file = get_stop_file(self)
        if os.path.exists(stop_file):
            os.remove(stop_file)
        try:
            while self.run and not os.path.exists(stop_file):
                self.adb_shell("monkey -v -v -v -s 8888 --throttle 500 --ignore-crashes --ignore-timeouts "
                               "--ignore-security-exceptions --monitor-native-crashes  --hprof --pct-touch 8 "
                               "--pct-motion 10 --bugreport "
                               "--pct-appswitch 5 --pct-majornav 5 --pct-nav 0 --pct-syskeys 0 --pct-trackball 60 "
                               "-p %s %d > %s" % (self.pkg, 999999999, self.get_output_file(".monkey")))
        except Exception as e:
            self.run = False
            tip("(%s) monkey stopped with errors!!!" % self.series, e)
        tip("(%s) monkey stopped!!!" % self.series)

    def stop_monkey(self):
        self.run = False
        self.kill_process_name("com.android.com")

    def dump_memory(self):
        tip("(%s) start dump..." % self.series)
        excel = excelx()
        try:
            last_datas = None
            datas = self.get_memory()
            excel.create_memory_sheet(self.get_output_file(".xlsx"), datas)

            crashed = False
            while self.run:
                datas = self.get_memory()

                # crash count
                excel.add_data(datas)
                cur = datas['Total']
                if cur == 0:
                    crashed = True
                else:
                    if crashed:
                        if last_datas is None:
                            continue
                        last = last_datas['Total']
                        if last - cur > 1000:
                            self.crashes += 1
                            print("crash count +1  -> %d" % self.crashes)
                            self.logcat_e_count(self.crashes)
                    crashed = False
                    last_datas = datas
                if cur > self.max:
                    self.max = cur
                if self.avg == 0:
                    self.avg = cur
                self.avg = int((self.avg + cur) / 2)
                logd('(%s) add data: %s' % (self.series, datas.values().__str__()))
                sleep(DUMP_INTERVAL)
        except Exception as e:
            self.success = False
            msg = traceback.format_exc()
            print("dump_memory: %s " % msg)
            raise e
        finally:
            tip("(%s) dump stopped!!!" % self.series)
            self.run = False
            plt_simple = excel.save(self.output)
            self.record(plt_simple)
            self.stop_monkey()

    def record(self, plt_simple):

        self.collect_logs()

        history = History()
        history.max = self.max
        history.avg = self.avg
        history.success = self.success
        history.device = self.series
        history.pkg = self.pkg
        db_helper.insert(history, self.conn)

        histories = db_helper.query_all(history, self.conn)

        history_temp = self.output + os.path.sep + "plt_history_temp.png"
        matlab_plt.plt_export_history(self.pkg, histories, history_temp)

        report = Report()
        report.pkg = self.pkg
        report.device = self.series
        report.plt_simple = plt_simple
        report.avg = self.avg
        report.max = self.max
        report.anrs = self.get_anr_files()
        report.crashes = self.get_crash_files()
        report.duration = self.duration
        report.xlsx = self.get_output_file(".xlsx")
        report.success = self.success
        report.plt_history = history_temp
        report.lint_file = self.__get_lint_file()
        report.checkstyle_file = self.__get_checkstyle_file()
        report.crash_count = self.crashes

        mail.send_mail(report)

    def __get_lint_file(self):
        dr = os.path.split(self.output)[0]
        file = "lint-results-dailyRelease.html"
        return dr + "/" + file

    def __get_checkstyle_file(self):
        dr = os.path.split(self.output)[0]
        file = "checkstyle.html"
        return dr + "/" + file

    def stop_logcat(self):
        self.kill_process_name("logcat")

    def logcat_clear(self):
        try:
            self.adb_shell("logcat -c")
        except Exception as e:
            tip("logcat -c failed, ", e)

    def logcat_e_count(self, count: int):
        self.adb_shell("logcat -v threadtime -t 2000 > %s " % self.get_output_file(".e.%d.logcat" % count, parent='ptk_app_crash'))

    def logcat(self):
        # args = ['adb']
        # if self.series is not None:
        #     args.append('-s')
        #     args.append(self.series)
        # args.append('logcat > %s' % self.get_output_file(".logcat"))
        #
        # process = subprocess.check_output(' '.join(args), shell=True)
        self.adb_shell("logcat -v threadtime > %s " % self.get_output_file(".logcat"))

    def logcat_e(self):
        # args = ['adb']
        # if self.series is not None:
        #     args.append('-s')
        #     args.append(self.series)
        # args.append('logcat *:E > %s' % self.get_output_file(".e.logcat"))
        #
        # subprocess.check_output(' '.join(args), shell=True)
        self.adb_shell("logcat -v threadtime *:E > %s " % self.get_output_file(".e.logcat"))

    def kill_process(self, pid):
        self.adb_shell("kill -9 %s" % pid)

    def kill_process_name(self, process_name):
        logd(self.series + " try stop process " + process_name)
        line_str = self.top_1()
        assert isinstance(line_str, str)
        lines = line_str.splitlines()
        for line in lines:
            els = re.split("\\s+", line.strip())
            if els.__len__() < 3:
                continue
            if not els[-1].startswith(process_name):
                continue
            pid = els[0]
            process = els[-1]
            try:
                tip("killing process %s(%s)..." % (process, pid))
                self.kill_process(pid)
            except Exception as e:
                tip("kill process %s(%s) failed!" % (process, pid), e)
                pass

    def get_output_file(self, suffix: str, parent=None):
        file_dir = self.output
        if parent is not None and parent.__len__() > 0:
            file_dir = file_dir + os.path.sep + parent
            os.makedirs(file_dir, exist_ok=True)
        return file_dir + os.path.sep + self.file_prefix + suffix

    def get_anr_files(self):
        if self.ptk_anr_dir is None:
            logd("ptk anr dir 没有初始化")
            return []
        if not os.path.exists(self.ptk_anr_dir):
            return []
        names = os.listdir(self.ptk_anr_dir)
        return [self.ptk_anr_dir + os.path.sep + name for name in names]

    def get_crash_files(self):
        if self.ptk_crash_dir is None:
            logd("ptk crash dir 没有初始化")
            return []
        if not os.path.exists(self.ptk_crash_dir):
            return []
        names = os.listdir(self.ptk_crash_dir)
        return [self.ptk_crash_dir + os.path.sep + name for name in names]

    def start(self):
        component = self.get_launcher_component2()
        if component is None:
            raise Exception("start app failed, cannot found app component, pkg: %s" % self.pkg)
        self.adb_shell("am start -n %s" % component)

    """ 
        获取AndroidManifest.xml中标记为Launcher的组件名称,
        cat= android.intent.category.LAUNCHER
        前提是app已经启动
    """

    def get_launcher_component(self):
        component = ''
        lines = self.adb_shell("dumpsys activity activities")
        assert isinstance(lines, str)
        for line in lines.splitlines():
            if line.__contains__("android.intent.category.LAUNCHER"):
                cmp_str = re.split("\\s+", line)[-1]
                component = cmp_str.split("=")[-1].replace("}", "")
                break
        return component

    """ 
        获取AndroidManifest.xml中标记为Launcher的组件名称,
        cat= android.intent.category.LAUNCHER
    """

    def get_launcher_component2(self):
        found_main = False
        lines = self.adb_shell("pm dump %s" % self.pkg).splitlines()
        component = None
        component_line = None
        for line in lines:
            assert isinstance(line, str)
            if line.strip() == 'android.intent.action.MAIN:':
                found_main = True
                continue
            if found_main:
                component_line = line
                break
        if component_line is None:
            return None
        component_line_splits = re.split("\\s+", component_line.strip())
        for split_word in component_line_splits:
            if split_word.startswith(self.pkg):
                component = split_word
                break
        return component

    """ 等待app启动 """

    def waiting_for_start(self):
        for i in range(10):
            process_start = False
            line_str = self.top_1()
            assert isinstance(line_str, str)
            lines = line_str.splitlines()
            for line in lines:
                words = re.split("\\s+", line.strip())
                if len(words) < 3:
                    continue
                if words[0].strip() == 'PID' or words[1] == 'PID':
                    process_start = True
                    continue
                if process_start:
                    pid = words[0]
                    name = words[-1].strip()
                    if name.startswith(self.pkg):
                        return pid
            sleep(1)
        return 0

    def top_1(self):
        return self.adb_shell("top -n 1")

    """ 清除历史日志 """

    def log_clear(self):
        dir = "/storage/self/primary"
        try:
            self.adb_shell("rm %s/app_crash*" % dir)
            self.adb_shell("rm %s/anr_*" % dir)
        except Exception as e:
            logd(e=e)

    def collect_logs(self, src_dir="/storage/self/primary"):
        # app_crash_dir = self.output + os.path.sep + "app_crash"
        # app_anr_dir = self.output + os.path.sep + "anr"
        # os.makedirs(app_crash_dir, exist_ok=True)
        # os.makedirs(app_anr_dir, exist_ok=True)

        ptk_phone_crash_dir = src_dir + os.path.sep + "ptk_app_crash"
        self.adb_shell("mkdir -p %s" % ptk_phone_crash_dir)
        self.adb_shell("mv %s/app_crash* %s" % (src_dir, ptk_phone_crash_dir), check=False)
        self.adb("pull %s %s" % (ptk_phone_crash_dir, self.output), check=False)
        self.adb_shell("rm -rf %s" % ptk_phone_crash_dir)

        ptk_phone_anr_dir = src_dir + os.path.sep + "ptk_anr"
        self.adb_shell("mkdir -p %s" % ptk_phone_anr_dir)
        self.adb_shell("mv %s/anr_* %s" % (src_dir, ptk_phone_anr_dir), check=False)
        self.adb("pull %s %s" % (ptk_phone_anr_dir, self.output), check=False)
        self.adb_shell("rm -rf %s" % ptk_phone_anr_dir)

    def ls(self, dir):
        return self.adb_shell("ls %s" % dir)


def shell(args, command='', _shell=True, check=False):
    with subprocess.Popen(" ".join(args), stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          encoding="utf-8", shell=_shell) as process:
        try:
            stdout, stderr = process.communicate(command, timeout=3000)
        except subprocess.TimeoutExpired:
            stdout, stderr = process.communicate()
            raise subprocess.TimeoutExpired(process.args, 3000, output=stdout,
                                            stderr=stderr)
        except Exception as e:
            tip(e=e)
            raise
        retcode = process.poll()
        if check and retcode:
            raise Exception(stderr, retcode)
    return stdout


def monkey(app):
    assert isinstance(app, AndroidApp)
    app.monkey()


def stop(app):
    assert isinstance(app, AndroidApp)
    tip("(%s) try to stop monkey & logcat..." % app.series)
    app.run = False
    os.system("touch %s" % get_stop_file(app))
    stop_monkey(app)
    stop_logcat(app)


def get_stop_file(app: AndroidApp):
    return "%s.stop.%s" % (WORK_DIR, app.pkg)


def stop_monkey(app):
    assert isinstance(app, AndroidApp)
    for i in range(3):
        app.stop_monkey()
        sleep(0.5)


def stop_logcat(app):
    assert isinstance(app, AndroidApp)
    for i in range(3):
        app.stop_logcat()
        sleep(0.5)
