Caffe Deep Learning Framework
------------------

http://caffe.berkeleyvision.org/
based on: https://gist.github.com/onauparc/dd80907401b26b602885


```rusthon
#backend:c++
import caffe/caffe.hpp
import caffe/util/io.hpp
import caffe/blob.hpp

namespace("caffe")

NET = "..."
NET_LAYERS = ".."
IMAGE = "some.png"

with pointers:
	def main():
		print('caffe hello world')
		Caffe::set_phase( Caffe::TEST )
		Caffe::set_mode( Caffe::CPU )

		with N as "Net<float>(%s)":
			net = new(N(NET))
		net.CopyTrainedLayerFrom(NET_LAYERS)

		dat = new( Datum() )
		ok = ReadImageToDatum(IMAGE, 1, 227, 227, addr(dat[...]) )
		if not ok:
			#raise std::exception  ## TODO fix
			raise std::exception()

		with B as "Blob<float>(%s)":
			blob = new(
				B(1,dat.channels(), dat.height(), dat.width())
			)

		bproto = new( BlobProto() )
		bproto.set_num(1)
		bproto.set_channels(dat.channels())
		bproto.set_height(  dat.height() )
		bproto.set_width(   dat.width()  )
		dsize = dat.channels()*dat.height()*dat.width()
		with stdmax as "std::max<int>(%s)":
			dsizedat = stdmax(
				dat.data().size(),
				dat.float_data_size()
			)

		for i in range(dsizedat):
			bproto.add_data(0.0)

		blob.FromProto(bproto)

		bottom = []Blob(blob,)

		ftype  = 0.0
		result = net.Forward( bottom )
		for i in range(1000):
			cdata = result[0].cpu_data()
			value = cdata[i]
			print value


```