Caffe Deep Learning Framework
------------------

http://caffe.berkeleyvision.org/

I am using Fedora, here is how to get Caffe to build properly.
Follow the offical Fedora install instructions [here](http://caffe.berkeleyvision.org/install_yum.html)
except do not install Atlas, instead install OpenBlas (yum install openblas),
and change your Makefile.config as described [here](http://caffe.berkeleyvision.org/installation.html)
to use OpenBlas.  You may also want to disable GPU support, if not then edit
the define below and remove `CPU_ONLY`.

```
cd
git clone https://github.com/BVLC/caffe.git
cd caffe
nano Makefile.config
make all
```

After you have edited your Makefile.config, simply run `make all`,
and this will give you libcaffe.so ready to link into this Rusthon program.

Running
-------
This is the command to compile and run this example.
note: libcaffe.so is given as a data file so it will be copied into the output tar package,
the binary will load dynamic libraries from the same directory.

```
cd Rusthon
./rusthon.py ./examples/hello_caffe.md --data=~/caffe/.build_release/lib/libcaffe.so
```

Source Code
-----------

note: blob.hpp requires caffe.pb.h (google protocol buffer),
this is file is generated when building Caffe, and because the offical
make file for Caffe is super bare-bones, its missing a "make install"
target, and this file is not normally found when building an external binary
that includes and links to Caffe.  As a simple workaround, the `.build_release`
folder is set as one of the include folders.

note: based on: https://gist.github.com/onauparc/dd80907401b26b602885


* @define: CPU_ONLY
* @link:caffe
* @include:~/caffe/include
* @include:~/caffe/.build_release/src
```rusthon
#backend:c++
import caffe/caffe.hpp
import caffe/util/io.hpp
import caffe/blob.hpp

namespace("caffe")

NET = "foo.prototxt"
NET_LAYERS = ".."
IMAGE = "some.png"

with pointers:
	def main():
		print('caffe hello world')
		Caffe::set_mode( Caffe::CPU )

		with N as "Net<float>(%s, caffe::TEST)":
			net = new(N(NET))
		net.CopyTrainedLayersFrom(NET_LAYERS)

		dat = new( Datum() )
		ok = ReadImageToDatum(IMAGE, 1, 227, 227, addr(dat[...]) )
		if not ok:
			#raise std::exception  ## TODO fix
			raise std::exception()

		with FloatBlob as "Blob<float>":
			blob = new(
				FloatBlob(1,dat.channels(), dat.height(), dat.width())
			)
			bottom = []FloatBlob()


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

		blob.FromProto(bproto[...])
		bottom.append( blob )

		ftype  = 0.0
		result = net.Forward( bottom[...] )

		#cdata = result[0].cpu_data()  ## this syntax will not work with external libraries
		with C as "result[0]->cpu_data":
			ref = C()
			cdata = addr(ref)

		for i in range(1000):
			value = cdata[i]
			print value


```