var Exception;
Exception = {};
try {
foo;
}
catch(__exception__) {
if (__exception__ == Exception || isinstance([__exception__, Exception])) {
var babar = __exception__;
console.log(true);
}

}

