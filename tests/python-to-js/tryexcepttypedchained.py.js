var Exception1, Exception2;
Exception1 = {};
Exception2 = {};
try {
throw Exception2;
}
catch(__exception__) {
if (__exception__ == Exception1 || isinstance([__exception__, Exception1])) {
console.log(false);
}

if (__exception__ == Exception2 || isinstance([__exception__, Exception2])) {
console.log(true);
}

}

