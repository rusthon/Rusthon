# based on the go test by Dennis Francis
# https://github.com/dennisfrancis/gopherjs-channeltransfer-speed


import "github.com/gopherjs/gopherjs/js"


data_chan = go.channel(int)

document = js.Global.Get("document")

def main():
	js.Global.Get("window").Set("onload", setup)

def setup():

	go( receive() )
	bt = document.Call("getElementById", "startbt")
	bt.Set("onclick", runtests)


def runtests():
	var bt = document.Call("getElementById", "startbt")
	bt.Set("disabled", true)

	#go func() {
	#	test_calldepth()
	#	test_localmem()
	#}()

	go( test_calldepth() )
	go( test_localmem() )


def test_calldepth():

	latency = go.make([]float64, 1000)
	perf = js.Global.Get("performance")
	#for cd := 1; cd <= 1000; cd++ {
	for cd in range(1, 1000):
		t0 = perf.Call("now").Float()
		#for ii:=0; ii<50; ii++ {
		for ii in range(50):
			send_func(cd, 1, ii)
		t1 = perf.Call("now").Float()
		latency[cd-1] = (t1 - t0)/50.0
		print("test1 calldepth =", cd)
	plot("ctsgraph1", latency, "Call depth", "Variation of Kilo Channel Transfers per second (KCTps) with call depth")

def test_localmem():

	latency = go.make([]float64, 1000)
	perf = js.Global.Get("performance")
	#for varsz := 1; varsz <= 1000; varsz++ {
	for varsz in range(1, 1000):
		t0 = perf.Call("now").Float()
		#for ii:=0; ii<50; ii++ {
		for ii in range(50):
			send_func(1, varsz, ii)

		t1 = perf.Call("now").Float()
		latency[varsz-1] = (t1 - t0)/50.0
	plot("ctsgraph2", latency, "Local variable size", "Variation of Kilo Channel Transfers per second (KCTps) with local variable size")


def plot(id:string, latency:[]float64, xlabel:string, title:string ):

	div = document.Call("getElementById", id)
	#options = map[string]interface{}{
	options = map[string]interface{
		#"legend" : "always",
		"title"  : title,
		"showRoller" : true,
		"rollPeriod" : 1,
		"ylabel" : "KCTps",
		"labels" : []string("x", "CTS"),
	}

	data = go.make([][]float64, len(latency))

	#for rowid := 0; rowid < len(latency); rowid++ {
	for rowid in range(len(latency)):
		data[rowid] = []float64(
			float64(rowid + 1), 
			1.0/latency[rowid]
		)


	js.Global.Get("Dygraph").New(div, data, options)


def send_func(call_depth:int, varsize:int, data:int ):
	locvar = go.make([]int, varsize)
	
	if call_depth <= 1:
		data_chan <- data
		return

	send_func(call_depth-1, varsize, data)

	print(locvar)

def receive():
	int data = 0
	while True:
		data = <-data_chan
		print("Received data =", data)
