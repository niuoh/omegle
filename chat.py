#coding=utf-8
from Tkinter import *
import tkFont,thread,time,urllib,urllib2
import sys
reload(sys)
sys.setdefaultencoding('utf8')
class CHAT:
	status,z_close=0,0
	height,width=570,600
	qz=u"系统消息:"
	init_url="http://front11.omegle.com/start?rcs=1&firstevents=1&spid=&randid=PB7EUBQU&lang=zh"
	event_url="http://front11.omegle.com/events"
	send_url="http://front11.omegle.com/send"
	disconnect_url="http://front11.omegle.com/disconnect"
	all_msg=[]

	def __init__(self):
		self.window = Tk()
		self.window.title(u'匿名聊天')
		self.init_window()
		self.window.mainloop()

	def init_window(self):
		ws = self.window.winfo_screenwidth()
		hs = self.window.winfo_screenheight()
		x = (ws/2) - (self.width/2)
		y = (hs/2) - (self.height/2)
		self.window.minsize(self.width,self.height)
		self.window.maxsize(self.width,self.height)
		self.window.geometry('%dx%d+%d+%d' % (self.width, self.height, x, y))
		self.window.bind('<Key>', self.key)
		self.M=Text(self.window,relief=RAISED,bg="white",cursor="arrow")
		self.M.place(width = self.width,height=500,anchor="nw")
		self.M.bind("<KeyPress>",lambda e:"break")
		self.M.tag_config("system",foreground="red")
		self.M.tag_config("me",foreground="#0066CC")
		self.M.tag_config("other",foreground="#006666")
		self.C=Button(self.window, text ="开始\n匹配", command = self.pipei,bg="#006633",activebackground="#006633",fg="white",activeforeground="white",font=tkFont.Font(size=11))
		self.C.place(width=80,height=70,anchor="nw",y=500)
			
		self.T=Text(self.window,relief=RAISED,bg="white")
		self.T.place(width=440,height=70,anchor="nw",y=500,x=80)

		self.S=Button(self.window, text ="发送\n消息", command = self.send,bg="#006633",activebackground="#006633",fg="white",activeforeground="white",font=tkFont.Font(size=11))
		self.S.place(width=80,height=70,anchor="nw",y=500,x=520)
		self.S['state']="disabled"

		self.M.insert(INSERT,self.qz+u"欢迎使用匿名聊天程序　点击开始匹配寻找陌生人聊天...\n","system")

	def pipei(self):
		if self.status==0:
			self.z_close=0
			self.C['state']="disabled"
			self.M.insert(INSERT,self.qz+u"开始匹配...","system")
			thread.start_new_thread(self.get_msg,())
		else:
			self.close(True)

	def get_msg(self):
		try:
			html = urllib2.Request(self.init_url)
			html = urllib2.urlopen(html).read()
		except:return

		self.data={"id":eval(html)['clientID']}
		while True:
			if self.z_close==1:return
			try:
				html = urllib2.Request(self.event_url,urllib.urlencode(self.data))
				html = urllib2.urlopen(html).read()
			except:continue
			#html=requests.post(self.event_url,data=self.data)
			if html=="null":continue
			elif self.status==0:
                                self.status=1
				self.M.delete("1.0",END)
				self.all_msg=[]
				self.all_msg.append("system&&&&"+self.qz+u"成功匹配到陌生人...开始聊天吧！")
				self.S['state']="normal"
                                self.show()
				self.C['state']="normal"
				self.C['text']=u"断开\n连接"
			try:r=eval(html)[0]
			except:
				self.close()
				return
			if "gotMessage" in r:
				self.all_msg.append(u"other&&&&陌生人:"+unicode(r[1],"utf-8").decode("unicode_escape"))
				self.show()
			elif "strangerDisconnected" in r[0]:
                               self.close()
                               return
			time.sleep(1)

	def close_action(self):
		self.z_close=1
		self.all_msg.append("system&&&&"+self.qz+u"我关闭了连接")
		self.show()
		try:
			html = urllib2.Request(self.disconnect_url)
			html = urllib2.urlopen(html).read()
		except:pass

	def close(self,z=False):
		if z==False:
			self.all_msg.append("system&&&&"+self.qz+u"对方关闭了连接")
			self.show()
		else:thread.start_new_thread(self.close_action,())
		self.status=0
		self.S['state']="disabled"
		self.C['text']=u"开始\n匹配"

	def send(self):
		msg=self.T.get("1.0",END).strip('\n')
		if len(msg)==0:
			self.all_msg.append("system&&&&"+self.pz+u"消息不能为空...")
			self.show()
		else:thread.start_new_thread(self.send_action,(msg,))

	def send_action(self,msg):
		self.T.delete("1.0",END)
		data=self.data
		data['msg']=msg
		self.all_msg.append("me&&&&"+u"我:"+msg)
		self.show()
		try:
			html = urllib2.Request(self.send_url,urllib.urlencode(data))
			html = urllib2.urlopen(html).read()
		except:html=""
		if html!="win":
			self.all_msg.append("system&&&&"+self.qz+u"消息:'"+msg+u"'发送失败!")
			self.show()

	def show(self):
		self.M.delete("1.0",END)
		for i in self.all_msg:
			msg=i.split('&&&&')
			self.M.insert(INSERT,msg[1]+"\n",msg[0])

	def key(self,e):
		if e.keycode==36:
			if self.S['state']=="normal":self.send()

if __name__ == '__main__':
	chat=CHAT()
