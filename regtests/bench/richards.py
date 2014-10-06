'''
Richards
'''

# based on a Java version:
#  Based on original version written in BCPL by Dr Martin Richards
#  in 1981 at Cambridge University Computer Laboratory, England
#  and a C++ version derived from a Smalltalk version written by
#  L Peter Deutsch.
#  Java version:  Copyright (C) 1995 Sun Microsystems, Inc.
#  Translation from C++, Mario Wolczko
#  Outer loop added by Alex Jacoby

from time import clock

# Task IDs
I_IDLE = 1
I_WORK = 2
I_HANDLERA = 3
I_HANDLERB = 4
I_DEVA = 5
I_DEVB = 6

# Packet types
K_DEV = 1000
K_WORK = 1001

# Packet

BUFSIZE = 4

BUFSIZE_RANGE = range(BUFSIZE)

class Packet(object):

	def __init__(self,l:*Packet, i:int, k:int):
		*Packet	self.link = l
		int		self.ident = i
		int		self.kind = k
		int		self.datum = 0
		#[]int	self.data = [0] * BUFSIZE
		[]int	self.data = []int()
		for x in range(BUFSIZE):
			self.data.append( 0 )

	def append_to(self, lst:*Packet) -> *Packet:
		self.link = None
		if lst is None:
			return self
		else:
			p = lst
			next = p.link
			while next is not None:
				p = next
				next = p.link
			p.link = self
			return lst

# Task Records

class TaskRec(object):
	pass

class DeviceTaskRec(TaskRec):
	def __init__(self):
		*Packet  self.pending = None

class IdleTaskRec(TaskRec):
	def __init__(self):
		int self.control = 1
		int self.count = 10000

class HandlerTaskRec(TaskRec):
	def __init__(self):
		*Packet  self.work_in = None
		*Packet  self.device_in = None

	def workInAdd(self, p:*Packet) ->*Packet:
		self.work_in = p.append_to(self.work_in)
		return self.work_in

	def deviceInAdd(self, p:*Packet) ->*Packet:
		self.device_in = p.append_to(self.device_in)
		return self.device_in

class WorkerTaskRec(TaskRec):
	def __init__(self):
		int self.destination = I_HANDLERA
		int self.count = 0

# Task

class TaskState(object):
	def __init__(self):
		bool self.packet_pending = True
		bool self.task_waiting = False
		bool self.task_holding = False

	def packetPending(self) -> self:
		self.packet_pending = True
		self.task_waiting = False
		self.task_holding = False
		return self

	def waiting(self) -> self:
		self.packet_pending = False
		self.task_waiting = True
		self.task_holding = False
		return self

	def running(self) -> self:
		self.packet_pending = False
		self.task_waiting = False
		self.task_holding = False
		return self
		
	def waitingWithPacket(self) -> self:
		self.packet_pending = True
		self.task_waiting = True
		self.task_holding = False
		return self
		
	def isPacketPending(self) -> bool:
		return self.packet_pending

	def isTaskWaiting(self) -> bool:
		return self.task_waiting

	def isTaskHolding(self) -> bool:
		return self.task_holding

	def isTaskHoldingOrWaiting(self) -> bool:
		return self.task_holding or (not self.packet_pending and self.task_waiting)

	def isWaitingWithPacket(self) -> bool:
		return self.packet_pending and self.task_waiting and not self.task_holding





tracing = False
layout = 0

def trace(a:string):
	global layout
	layout -= 1
	if layout <= 0:
		print()
		layout = 50
	print(a)




class Task(TaskState):

	# note: r:TaskRec is the super class, TODO cast to its subclass.
	def __init__(self,i:int, p:int, w:*Packet, initialState:*TaskState,r:TaskRec):
		*Task    self.link = taskWorkArea.task
		int      self.ident = i
		int      self.priority = p
		*Packet  self.input = w

		bool self.packet_pending = initialState.isPacketPending()
		bool self.task_waiting = initialState.isTaskWaiting()
		bool self.task_holding = initialState.isTaskHolding()

		#*TaskRec  self.handle = r
		self.handle = r  ## generic

		#taskWorkArea.taskList = self
		#taskWorkArea.taskTab[i] = self
		taskWorkArea.set_task(self, i)

	def fn(self, pkt:*Packet, r:TaskRec) -> self:
		#raise NotImplementedError
		print('NotImplementedError')
		print(r)
		return self

	def addPacket(self,p:*Packet, old:Task) -> self:
		if self.input is None:
			self.input = p
			self.packet_pending = True
			if self.priority > old.priority:
				return self
		else:
			p.append_to(self.input)
		return old


	def runTask(self) -> self:
		*Packet msg
		if self.isWaitingWithPacket():
			msg = self.input
			self.input = msg.link
			if self.input is None:
				self.running()
			else:
				self.packetPending()
		#else:
		#	msg = None

		#return self.fn(msg,self.handle)  ## self.handle is generic (interface{})
		#return self.run_fn( msg, self.handle )
		return self.fn(msg, go.type_assert(self.handle, TaskRec))  ## self.handle is generic (interface{})

	#def run_fn(self, msg:*Packet, handle:TaskRec) -> self:
	#	return self.fn(msg, handle)


	def waitTask(self) -> self:
		self.task_waiting = True
		return self


	def hold(self) -> *Task:
		taskWorkArea.holdCount += 1
		self.task_holding = True
		return self.link


	def release(self,i:int) -> self:
		t = self.findtcb(i)
		t.task_holding = False
		if t.priority > self.priority:
			return go.type_assert(t, self)
		else:
			return self


	def qpkt(self, pkt:*Packet) -> self:
		t = self.findtcb(pkt.ident)
		taskWorkArea.qpktCount += 1
		pkt.link = None
		pkt.ident = self.ident
		#return t.addPacket(pkt,self)
		#return t.addPacket(pkt, go.type_assert(self, self))
		return go.type_assert( t.addPacket(pkt,self), self )


	def findtcb(self,id:int) -> *Task:
		t = taskWorkArea.taskTab[id]
		if t is None:
			print('Exception in findtcb')
		return t
			


# DeviceTask


class DeviceTask(Task):
	def __init__(self,i:int, p:int, w:*Packet, s:*TaskState, r:TaskRec):
		Task.__init__(self,i,p,w,s,r)

	#######def fn(self,pkt:*Packet, r:TaskRec) -> self:
	#def fn(self,pkt:*Packet, r:*DeviceTaskRec) -> self:
	def fn(self,pkt:*Packet, r:*TaskRec) -> self:
		d = go.type_assert(r, DeviceTaskRec)
		#assert isinstance(d, DeviceTaskRec)
		#class:DeviceTaskRec  d = r

		if pkt is None:
			pkt = d.pending
			if pkt is None:
				return self.waitTask()
			else:
				d.pending = None
				return self.qpkt(pkt)
		else:
			d.pending = pkt
			##########if tracing: trace(pkt.datum)
			return go.type_assert(self.hold(), self)



class HandlerTask(Task):
	def __init__(self,i:int, p:int, w:*Packet, s:*TaskState, r:TaskRec):
		Task.__init__(self,i,p,w,s,r)

	def fn(self, pkt:*Packet, r:*TaskRec) -> self:
		h = go.type_assert(r, HandlerTaskRec)
		#class:HandlerTaskRec h = r
		#assert isinstance(h, HandlerTaskRec)  ## old style typedef

		if pkt is not None:
			if pkt.kind == K_WORK:
				h.workInAdd(pkt)
			else:
				h.deviceInAdd(pkt)
		work = h.work_in
		if work is None:
			return self.waitTask()
		count = work.datum
		if count >= BUFSIZE:
			h.work_in = work.link
			return self.qpkt(work)

		dev = h.device_in
		if dev is None:
			return self.waitTask()

		h.device_in = dev.link
		dev.datum = work.data[count]
		work.datum = count + 1
		return self.qpkt(dev)

# IdleTask


class IdleTask(Task):
	def __init__(self,i:int, p:int, w:*Packet, s:*TaskState, r:TaskRec):
		Task.__init__(self,i,0,None,s,r)

	def fn(self,pkt:*Packet,r:*TaskRec) -> self:
		i = go.type_assert(r, IdleTaskRec)
		#assert isinstance(i, IdleTaskRec)
		i.count -= 1
		if i.count == 0:
			#return self.hold()
			return go.type_assert(self.hold(), self)
		elif i.control & 1 == 0:
			i.control //= 2
			return self.release(I_DEVA)
		else:
			i.control = i.control//2 ^ 0xd008
			return self.release(I_DEVB)
			

# WorkTask


A = ord('A')

class WorkTask(Task):
	def __init__(self,i:int, p:int, w:*Packet, s:*TaskState, r:TaskRec):
		Task.__init__(self,i,p,w,s,r)

	def fn(self,pkt:*Packet, r:*TaskRec) -> self:
		w = go.type_assert(r, WorkerTaskRec)
		#assert isinstance(w, WorkerTaskRec)
		if pkt is None:
			return self.waitTask()

		#int dest
		dest = 0
		if w.destination == I_HANDLERA:
			dest = I_HANDLERB
		else:
			dest = I_HANDLERA

		w.destination = dest
		pkt.ident = dest
		pkt.datum = 0

		for i in BUFSIZE_RANGE: # xrange(BUFSIZE)
			w.count += 1
			if w.count > 26:
				w.count = 1
			pkt.data[i] = A + w.count - 1

		return self.qpkt(pkt)


class TaskWorkArea(object):
	def __init__(self):
		[]Task      self.taskTab  = [10]Task()
		*Task       self.task     = None
		int self.holdCount = 0
		int self.qpktCount = 0

	def set_task(self, t:Task, i:int):
		c = go.type_assert(t, Task)
		self.task = c
		self.taskTab[i] = c

taskWorkArea = TaskWorkArea()

def schedule():
	t = taskWorkArea.task
	while t is not None:
		#pkt = None
		#if tracing:
		#	print("tcb =",t.ident)

		if t.isTaskHoldingOrWaiting():
			t = t.link
		else:
			###########if tracing: trace(chr(ord("0")+t.ident))
			t = t.runTask()

class Richards(object):

	def run(self, iterations:int) ->bool:
		for i in range(iterations):
			taskWorkArea.holdCount = 0
			taskWorkArea.qpktCount = 0

			#IdleTask(I_IDLE, 1, 10000, TaskState().running(), IdleTaskRec())
			IdleTask(I_IDLE, 1, None, TaskState().running(), IdleTaskRec())

			wkq = Packet(None, 0, K_WORK)
			wkq = Packet(wkq , 0, K_WORK)
			WorkTask(I_WORK, 1000, wkq, TaskState().waitingWithPacket(), WorkerTaskRec())

			wkq = Packet(None, I_DEVA, K_DEV)
			wkq = Packet(wkq , I_DEVA, K_DEV)
			wkq = Packet(wkq , I_DEVA, K_DEV)
			HandlerTask(I_HANDLERA, 2000, wkq, TaskState().waitingWithPacket(), HandlerTaskRec())

			wkq = Packet(None, I_DEVB, K_DEV)
			wkq = Packet(wkq , I_DEVB, K_DEV)
			wkq = Packet(wkq , I_DEVB, K_DEV)
			HandlerTask(I_HANDLERB, 3000, wkq, TaskState().waitingWithPacket(), HandlerTaskRec())

			wkq = None;
			DeviceTask(I_DEVA, 4000, wkq, TaskState().waiting(), DeviceTaskRec());
			DeviceTask(I_DEVB, 5000, wkq, TaskState().waiting(), DeviceTaskRec());
			
			schedule()

			if taskWorkArea.holdCount == 9297 and taskWorkArea.qpktCount == 23246:
				pass
			else:
				return False

		return True

def entry_point(iterations:int) ->float64:
	r = Richards()
	startTime = clock()
	result = r.run(iterations)
	if not result:
		print('#ERROR incorrect results!')
	return clock() - startTime

def main():
	iterations=10
	#print("#Richards benchmark (Python) starting. iterations="+str(iterations))
	total_s = entry_point(iterations)
	#print("#Total time for %s iterations: %s secs" %(iterations,total_s))
	s = total_s / float64(iterations)
	#print("#Average seconds per iteration:", s)
	print(s)
