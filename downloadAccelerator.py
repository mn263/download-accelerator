import argparse
import os
import os.path
import requests
import threading
import time
import urllib2


class HeadRequest(urllib2.Request):
    def get_method(self):
        return "HEAD"



''' Downloader for a set of files '''
class Downloader:
    def __init__(self):
        ''' initialize the file where the list of URLs is listed, and the
        directory where the downloads will be stored'''
        self.args = None
        self.parse_arguments()

    def parse_arguments(self):
        ''' parse arguments, which include '-i' for input file and
        '-d' for download directory'''
        parser = argparse.ArgumentParser(prog='Mass downloader', description='A simple script that downloads multiple files from a list of URLs specified in a file', add_help=True)
        parser.add_argument('-n', '--number', type=int, action='store', help='Specify the number of threads to create',default=10)
        parser.add_argument("url")
        args = parser.parse_args()
        self.number = args.number
        self.url = args.url

    def download(self):
        ''' download the files listed in the input file '''
        url = self.url
        req = HeadRequest(url)
        response = urllib2.urlopen(req)
        meta = response.info()
        response.close()
        contentLength = int(meta.getheaders("Content-Length")[0])
        number = int(self.number)

        threadByteSize = contentLength/number
        beginBytes = 0
        endBytes = threadByteSize

        fileName = url.split('/')[-1].strip()
        if len(fileName) < 1:
            fileName = 'index.html'

        if os.path.isfile(fileName):
            os.remove(fileName)

        # Start timing
        t0 = time.clock()
        # print "clock started"
 
        threads = []
        for i in range(0,number-1):
            d = DownThread(url, beginBytes, endBytes)
            threads.append(d)
            d.start()
            beginBytes = endBytes + 1 
            endBytes = endBytes + threadByteSize

        # change to take the last thread and increment its bytes
        # if endBytes < contentLength:
        endBytes = contentLength + 1
        d = DownThread(url, beginBytes, endBytes)
        threads.append(d)
        d.start()

        for t in threads:
            t.join()

        with open(fileName, 'wb') as f:
            for t in threads:
                # print '%d' % t.beginBytes
                f.write(t.data)

        print '%s %d %d %f' % (url, number, contentLength, time.clock() - t0)


''' Use a thread to download one file given by url and stored in filename'''
class DownThread(threading.Thread):
    def __init__(self,url,beginBytes,endBytes):
        # print 'starting initialize for : beginBytes: %d endBytes: %d' % (beginBytes, endBytes)
        threading.Thread.__init__(self)
        self.url = url
        self.beginBytes = beginBytes
        self.endBytes = endBytes
        # print 'starting initialize for : beginBytes: %d endBytes: %d' % (beginBytes, endBytes)
        # self._content_consumed = False

    def run(self):
        # print 'starting run for : beginBytes: %d endBytes: %d' % (self.beginBytes, self.endBytes)
        # check if i need a space bbyte and = sign
        # bytesRange = 'bytes=%s-%s' % (self.beginBytes, self.endBytes)
        # print bytesRange
        req = urllib2.Request(self.url)
        # , headers={'Range':bytesRange})
        req.headers['Range'] = 'bytes=%s-%s' % (self.beginBytes, self.endBytes)
        data = urllib2.urlopen(req).read()
        self.data = data
        # print len(data)
        # print 'ending run for: beginBytes: %d endBytes: %d' % (self.beginBytes, self.endBytes)


if __name__ == '__main__':
    d = Downloader()
    d.download()

#the report should have enough detail that somebody could replicate my methodology and get the same results


























    '''
    import argparse
import sys
import threading

class Shared:
    """ Shared memory """
    def __init__(self):
        self.i = 0
        self.sem = threading.Semaphore()
        self.lock = threading.Lock()

    def inc(self):
        """ increment the shared varable """
        self.sem.acquire()
        self.i = self.i + 1
        s = self.i
        self.sem.release()
        return s

class Hello(threading.Thread):
    """ A thread that increments and prints both a local and shared
    variable """
    def __init__(self,shared):
        threading.Thread.__init__(self)
        self.i = 0
        self.shared = shared

    def run(self):
        self.i = self.i + 1
        s = self.shared.inc()
        with self.shared.lock:
            print "Hello from thread %s i = %d shared = %d" % (self.getName(),i,s)

def parse_options():
        parser = argparse.ArgumentParser(prog='threadHello', description='Simple demonstration of threading', add_help=True)
        parser.add_argument('-n', '--number', type=int, action='store', help='Specify the number of threads to create',default=10)
        return parser.parse_args()

if __name__ == "__main__":
    args = parse_options()
    s = Shared()
    for i in range(0,args.number):
        h = Hello(s)
        h.start()
'''