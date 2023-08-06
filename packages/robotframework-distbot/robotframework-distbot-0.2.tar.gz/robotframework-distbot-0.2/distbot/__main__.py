import argparse
import subprocess
import os
import time
import psutil
import robot
from multiprocessing import Process, Value, Lock
from robot.parsing.model import TestData, TestDataDirectory
from tasksdb import TasksDB
import logging

class DistRoboRunner(object):
    def __init__(self, args, robotArgs):
        self.args = args
        self.robotArgs = robotArgs
        if self.args.outputdir==None:
            self.args.outputdir='report'
        self.robotArgs += ['-d',self.args.outputdir]

    def sequential(self):
        if self.args.suite:
            self.robotArgs += ['-s', self.args.suite]
        self.robotArgs += [self.args.main_suite]
        print(self.robotArgs)
        robot.run_cli(self.robotArgs)

    def distributed(self):
        tasks = TasksDB(self.args.outputdir)
        if not tasks.isTasksLoaded():
            newTasks = {
                'sequential': [
                    {
                        'parallel': self.getAllSuites()
                    },
                    'rebot'
                ]
            }
            tasks.loadTasks(newTasks)
            tasks.printTableData()
        procCount = Value('i', 0)
        lock = Lock()
        while True:
            if self.canStartProcess(procCount.value):
                task = tasks.getTaskToWorkOn()
                if task:
                    p = Process(target=self.runTask, args=(task,procCount,lock))
                    p.start()
                    time.sleep(2)
                else:
                    break
            else:
                time.sleep(5)

    def canStartProcess(self, procsCount):
        canStart = True
        allNone = True
        if self.args.max_processes:
            print('Running processes count:' + str(procsCount))
            canStart = canStart and (self.args.max_processes > procsCount)
            allNone = False
        if self.args.max_cpu_percent:
            cpuPerc = psutil.cpu_percent()
            print('Used CPU (%):' + str(cpuPerc))
            canStart = canStart and (self.args.max_cpu_percent > cpuPerc)
            allNone = False
        if self.args.max_memory:
            memMB = psutil.virtual_memory().used/1024/1024
            print('Used memory (MB):' + str(memMB))
            canStart = canStart and (self.args.max_memory > memMB)
            allNone = False
        if allNone:
            canStart = canStart and (5 > procsCount)
        return canStart

    def runTask(self, rowid, procsCount, lock):
        tasks = TasksDB(self.args.outputdir)
        suite = tasks.getTask(rowid)
        print(str(os.getpid()) + '|Running suite ' + suite + ' .....')
        with lock:
            procsCount.value += 1
        if suite == 'rebot':
            runArgs = ['-R','-d',self.args.outputdir,self.args.outputdir+'/*.xml']
            robot.rebot_cli(runArgs, exit=False)
        else:
            runArgs = self.robotArgs + ['-l','NONE','-r','NONE','-s',suite,'-o',suite+'.xml',self.args.main_suite]
            robot.run_cli(runArgs, exit=False)
        tasks.finishTask(rowid)
        tasks.printTableData()
        with lock:
            procsCount.value -= 1

    def getAllSuites(self):
        root = TestData(parent=None, source=self.args.main_suite, 
                include_suites=([] if self.args.suite==None else self.args.suite.split(',')))
        return self.traverseTestDataDir(root, '', [])

    def traverseTestDataDir(self, suite, path, suites):
        if isinstance(suite, TestDataDirectory):
            for childSuite in suite.children:
                self.traverseTestDataDir(childSuite, path + suite.name + '.', suites)
        else:
            suites += [path + suite.name]
        return suites

class PhantomJS(object):
    def __init__(self):
        import socket
        from contextlib import closing
        portNum = '2018'
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
            s.bind(('localhost', 0))
            portNum = str(s.getsockname()[1])
        self.phantom = subprocess.Popen(['phantomjs', '--webdriver='+portNum])
        self.remoteUrl = 'http://localhost:'+portNum+'/'

    def get(self):
        return self.remoteUrl

    def __del__(self):
        self.phantom.kill()

def main():
    parser = argparse.ArgumentParser(usage='-e ENV [options] main_suite [robot arguments]', add_help=True)
    parser.add_argument('-e', required=True, help='dev, stage, prod etc. This value will be available as variable ENV.')
    parser.add_argument('-b', required=False, help='This value will be available as variable BROWSER.')
    parser.add_argument('-u', required=False, help='This value will be available as variable USERNAME.')
    parser.add_argument('-p',required=False, help='This value will be available as variable PASSWORD.')
    parser.add_argument('--mode', required=False, choices=['sequential', 'distributed'], default='sequential')
    parser.add_argument('--max-cpu-percent', required=False, type=float, help='Program will stop spawning new process when cpu usage reaches this value.')
    parser.add_argument('--max-memory', required=False, type=int, help='Program will stop spawning new process when memory usage reaches this value.')
    parser.add_argument('--max-processes', required=False, type=int, help='Program will stop spawning new process when running processes count is this value.')
    parser.add_argument('main_suite', help='Folder name containing all the robot framework scripts.')
    parser.add_argument('-d', '--outputdir', required=False, help='Directory to save report files. Default is <working dir>/report')
    parser.add_argument('-s', '--suite', required=False, help='Only run suites matching this value.')
    args, robotArgs = parser.parse_known_args()
    remoteUrl = 'False'
    phantom = None
    if args.b == 'phantomjs':
        phantom = PhantomJS()
        remoteUrl = phantom.get()
    robotArgs += ['-v', 'ENV:'+args.e]
    if args.b:
        robotArgs += ['-v', 'BROWSER:'+args.b]
    if args.u:
        robotArgs += ['-v', 'USERNAME:'+args.u]
    if args.p:
        robotArgs += ['-v', 'PASSWORD:'+args.p]
    if remoteUrl:
        robotArgs += ['-v', 'REMOTEURL:'+remoteUrl]
    
    getattr(DistRoboRunner(args, robotArgs), args.mode, lambda: "Unkown run mode!")()

if __name__ == '__main__':
    main()
