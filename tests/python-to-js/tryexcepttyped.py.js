var Exception;
Exception = {};
try {
throw Exception;
}
catch(__exception__) {
if (__exception__ == Exception || isinstance([__exception__, Exception])) {
console.log(true);
}

}

