JavaVM JNI
---------

Supports user code `import.jvm`, `jvm.namespace`, and `jvm(myclass)`.  See example here:
https://github.com/rusthon/Rusthon/blob/master/examples/java_giws.md

Below `gen_jvm_header` generates the JNI header code required to implement rusthon's `jvm` api.
TODO: fix JVM crash, originally it was working, but then something changed here (making it a global?) that makes it crash on exit.

```python


JVM_HEADER = '''
#include <jni.h>

JavaVM* __create_javavm__() {
	JavaVM* jvm = new JavaVM();
	JNIEnv* env;
	JavaVMInitArgs args;
	JavaVMOption options[2];
	args.version = JNI_VERSION_1_4;
	args.nOptions = 2;
	options[0].optionString = const_cast<char*>("-Djava.class.path=.%s");
	options[1].optionString = const_cast<char*>("-Xcheck:jni");
	args.options = options;
	args.ignoreUnrecognized = JNI_FALSE;
	JNI_CreateJavaVM(&jvm, (void **)&env, &args);
	return jvm;
}

static JavaVM* __javavm__ = __create_javavm__();
'''
def gen_jvm_header( jars ):
	if jars:
		a = ':' + ':'.join(jars)
		return JVM_HEADER %a
	else:
		return JVM_HEADER %''

```