import lazy_loader as lazy

import sys
import time


class PySpecClient():
    """
    This class will interact with the spec server on the hutch IDB3 computer and allow SARA pass the appropriate commands
    """
    def __init__(self, address='id3b.classe.cornell.edu', port='spec'):
        self.address = address
        self.port = port
        self.connected = False        
        self.output = []
        self.last_output = None
        self.channel = {}
        self.spec = None

        self.SpecConnection = lazy.load("pyspec.client.SpecConnection", require="AFL-automation[pyspec]")
        self.SpecCounter = lazy.load("pyspec.client.SpecCounter", require="AFL-automation[pyspec]")
        self.SpecConnectionsManager = lazy.load("pyspec.client.SpecConnectionsManager", require="AFL-automation[pyspec]")
        self.SpecWaitObject = lazy.load("pyspec.client.SpecWaitObject", require="AFL-automation[pyspec]")
        self.SpecVariable = lazy.load("pyspec.client.SpecVariable", require="AFL-automation[pyspec]")
        self.SpecMotor = lazy.load("pyspec.client.SpecMotor", require="AFL-automation[pyspec]")
        self.SpecCommand = lazy.load("pyspec.client.SpecCommand", require="AFL-automation[pyspec]")


    def _update_output(self, value, channel):
        self.output.append(value)
        self.last_output = self.output[-1]
        print(self.last_output)
        

    def _update_channel(self, value, channel):
        print(f"{channel}: {value}")


    def connect(self):
        '''
        Connect to the external spec server at connection name conn.
        This should be an object that can be passed to the other functions that talk to a spec server
        '''
        self.conn = f'{self.address}:{self.port}'
        print('')
        print(self.conn)
        # self.spec = SpecConnectionsManager_mod.SpecConnectionsManager().getConnection(self.conn)

        self.spec = self.SpecConnection(self.conn) #hard coded connection
        while not self.spec.is_connected():
            pass

        if self.spec.is_connected():
            print(f'established connection to {self.conn}')
        
        #need to register callbacks our desired channels:
        #this channel can be read as if spec is busy or not??
        self.spec.register('status/ready',self._update_channel) 
        #this channel returns the output from the cmd line and passes it into the output list
        self.spec.register('output/tty',self._update_output) 
        print('List of registered channels')
        for ch in list(self.spec.reg_channels):
            print(ch)
        print("")
        return

    def run_cmd(self,cmd,block=True,timeout=1800):
        cmd = self.SpecCommand(self.spec,cmd,timeout=timeout)
        if not block:
            cmd.synchronous = False
        cmd()

    def cd(self, path):
        """ A generic mv command. Moves the Spec directory to the specified path
        """

        self.spec.run_cmd(f'cd {path}')

    def mkdir(self, path):
        """A generic mkdir command. makes the specified directory or set of directories """
        self.spec.run_cmd(f'u mkdir {path}')

    def get_variable(self,name): 
        return self.spec.getVariable(name)

    def get_motor(self,name): 
        return self.spec.getMotor(name)

    def get_counter(self,name): 
        return self.spec.getChannel(name)

    def block_for_ready(self,timeout=300):
        ready = self.spec.getChannel('status/ready')
        if ready.read()==1:
            return
        else:
            w = self.SpecWaitObject(self.spec)
            w.waitChannelUpdate('status/ready', waitValue = 1,timeout=timeout*1000) 

    def block_for_count(self,timeout=300):
        w = self.SpecWaitObject(self.spec)
        w.waitChannelUpdate('scaler/.all./count', waitValue = 0,timeout=timeout*1000) 

    def count(self, name,time,wait_on_time=True):
        """Count up to a certain time or monitor count
        Arguments:
        time -- count time
        """
        counter = self.spec.getChannel('scaler/.all./count')
        channel = self.spec.getChannel(f'scaler/{name}/value')

        index = self.spec.getChannel(f'var/{name}').read()
        if index == 1: #MONITOR
          time = -time

        counter.write(time)

        self.block_for_count()

        return channel.read()


if __name__=="__main__":        
    #from AFL.automation.instrument.PySpecClient import PySpecClient
    client = PySpecClient("localhost","spec")





