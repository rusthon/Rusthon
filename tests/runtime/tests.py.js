var test_equal = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("a", "b", "message")};
arguments = get_arguments(signature, args, kwargs);
var a = arguments['a'];
var b = arguments['b'];
var message = arguments['message'];
if(a == b) {
console.log(message);
}
else {
console.log(message, "failed");
}

}

var test_true = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("a", "message")};
arguments = get_arguments(signature, args, kwargs);
var a = arguments['a'];
var message = arguments['message'];
if(a) {
console.log(message);
}
else {
console.log(message, "failed");
}

}

var test_false = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("a", "message")};
arguments = get_arguments(signature, args, kwargs);
var a = arguments['a'];
var message = arguments['message'];
if(!a) {
console.log(message);
}
else {
console.log(message, "failed");
}

}

var __args_0, __kwargs_0;
__args_0 = create_array();
__kwargs_0 = {};
tests = get_attribute(list, "__call__")(__args_0, __kwargs_0);
var test_issubclass = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array()};
arguments = get_arguments(signature, args, kwargs);
var A, __A_attrs, __A_parents;
__A_attrs = {};
__A_parents = create_array();
A = create_class("A", __A_parents, __A_attrs);
var B, __B_attrs, __B_parents;
__B_attrs = {};
__B_parents = create_array();
__B_parents.push(A);
B = create_class("B", __B_parents, __B_attrs);
var C, __C_attrs, __C_parents;
__C_attrs = {};
__C_parents = create_array();
__C_parents.push(B);
C = create_class("C", __C_parents, __C_attrs);
var D, __D_attrs, __D_parents;
__D_attrs = {};
__D_parents = create_array();
D = create_class("D", __D_parents, __D_attrs);
var E, __E_attrs, __E_parents;
__E_attrs = {};
__E_parents = create_array();
__E_parents.push(C);
__E_parents.push(D);
E = create_class("E", __E_parents, __E_attrs);
var __args_1, __kwargs_1;
__args_1 = create_array(C, C);
__kwargs_1 = {};
var __args_2, __kwargs_2;
__args_2 = create_array(get_attribute(issubclass, "__call__")(__args_1, __kwargs_1), "C is a subclass of C");
__kwargs_2 = {};
get_attribute(test_true, "__call__")(__args_2, __kwargs_2);
var __args_3, __kwargs_3;
__args_3 = create_array(C, B);
__kwargs_3 = {};
var __args_4, __kwargs_4;
__args_4 = create_array(get_attribute(issubclass, "__call__")(__args_3, __kwargs_3), "C is a subclass of B");
__kwargs_4 = {};
get_attribute(test_true, "__call__")(__args_4, __kwargs_4);
var __args_5, __kwargs_5;
__args_5 = create_array(C, A);
__kwargs_5 = {};
var __args_6, __kwargs_6;
__args_6 = create_array(get_attribute(issubclass, "__call__")(__args_5, __kwargs_5), "C is a subclass of A");
__kwargs_6 = {};
get_attribute(test_true, "__call__")(__args_6, __kwargs_6);
var __args_7, __kwargs_7;
__args_7 = create_array(B, B);
__kwargs_7 = {};
var __args_8, __kwargs_8;
__args_8 = create_array(get_attribute(issubclass, "__call__")(__args_7, __kwargs_7), "B is a subclass of B");
__kwargs_8 = {};
get_attribute(test_true, "__call__")(__args_8, __kwargs_8);
var __args_9, __kwargs_9;
__args_9 = create_array(B, A);
__kwargs_9 = {};
var __args_10, __kwargs_10;
__args_10 = create_array(get_attribute(issubclass, "__call__")(__args_9, __kwargs_9), "B is a subclass of A");
__kwargs_10 = {};
get_attribute(test_true, "__call__")(__args_10, __kwargs_10);
var __args_11, __kwargs_11;
__args_11 = create_array(A, A);
__kwargs_11 = {};
var __args_12, __kwargs_12;
__args_12 = create_array(get_attribute(issubclass, "__call__")(__args_11, __kwargs_11), "A is a subclass of A");
__kwargs_12 = {};
get_attribute(test_true, "__call__")(__args_12, __kwargs_12);
var __args_13, __kwargs_13;
__args_13 = create_array(A, B);
__kwargs_13 = {};
var __args_14, __kwargs_14;
__args_14 = create_array(get_attribute(issubclass, "__call__")(__args_13, __kwargs_13), "A is not a subclass of B");
__kwargs_14 = {};
get_attribute(test_false, "__call__")(__args_14, __kwargs_14);
var __args_15, __kwargs_15;
__args_15 = create_array(B, C);
__kwargs_15 = {};
var __args_16, __kwargs_16;
__args_16 = create_array(get_attribute(issubclass, "__call__")(__args_15, __kwargs_15), "B is not a subclass of C");
__kwargs_16 = {};
get_attribute(test_false, "__call__")(__args_16, __kwargs_16);
var __args_17, __kwargs_17;
__args_17 = create_array(D, A);
__kwargs_17 = {};
var __args_18, __kwargs_18;
__args_18 = create_array(get_attribute(issubclass, "__call__")(__args_17, __kwargs_17), "D is not a subclass of A");
__kwargs_18 = {};
get_attribute(test_false, "__call__")(__args_18, __kwargs_18);
var __args_19, __kwargs_19;
__args_19 = create_array(D, C);
__kwargs_19 = {};
var __args_20, __kwargs_20;
__args_20 = create_array(get_attribute(issubclass, "__call__")(__args_19, __kwargs_19), "D is not a subclass of C");
__kwargs_20 = {};
get_attribute(test_false, "__call__")(__args_20, __kwargs_20);
var __args_21, __kwargs_21;
__args_21 = create_array(E, E);
__kwargs_21 = {};
var __args_22, __kwargs_22;
__args_22 = create_array(get_attribute(issubclass, "__call__")(__args_21, __kwargs_21), "E is subclass of E");
__kwargs_22 = {};
get_attribute(test_true, "__call__")(__args_22, __kwargs_22);
var __args_23, __kwargs_23;
__args_23 = create_array(E, D);
__kwargs_23 = {};
var __args_24, __kwargs_24;
__args_24 = create_array(get_attribute(issubclass, "__call__")(__args_23, __kwargs_23), "E is subclass of D");
__kwargs_24 = {};
get_attribute(test_true, "__call__")(__args_24, __kwargs_24);
var __args_25, __kwargs_25;
__args_25 = create_array(E, C);
__kwargs_25 = {};
var __args_26, __kwargs_26;
__args_26 = create_array(get_attribute(issubclass, "__call__")(__args_25, __kwargs_25), "E is subclass of C");
__kwargs_26 = {};
get_attribute(test_true, "__call__")(__args_26, __kwargs_26);
var __args_27, __kwargs_27;
__args_27 = create_array(E, B);
__kwargs_27 = {};
var __args_28, __kwargs_28;
__args_28 = create_array(get_attribute(issubclass, "__call__")(__args_27, __kwargs_27), "E is subclass of B");
__kwargs_28 = {};
get_attribute(test_true, "__call__")(__args_28, __kwargs_28);
var __args_29, __kwargs_29;
__args_29 = create_array(E, A);
__kwargs_29 = {};
var __args_30, __kwargs_30;
__args_30 = create_array(get_attribute(issubclass, "__call__")(__args_29, __kwargs_29), "E is subclass of A");
__kwargs_30 = {};
get_attribute(test_true, "__call__")(__args_30, __kwargs_30);
}

var __args_31, __kwargs_31;
__args_31 = create_array(test_issubclass);
__kwargs_31 = {};
get_attribute(get_attribute(tests, "append"), "__call__")(__args_31, __kwargs_31);
var test_isinstance = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array()};
arguments = get_arguments(signature, args, kwargs);
var A, __A_attrs, __A_parents;
__A_attrs = {};
__A_parents = create_array();
A = create_class("A", __A_parents, __A_attrs);
var B, __B_attrs, __B_parents;
__B_attrs = {};
__B_parents = create_array();
__B_parents.push(A);
B = create_class("B", __B_parents, __B_attrs);
var X, __X_attrs, __X_parents;
__X_attrs = {};
__X_parents = create_array();
X = create_class("X", __X_parents, __X_attrs);
var Y, __Y_attrs, __Y_parents;
__Y_attrs = {};
__Y_parents = create_array();
__Y_parents.push(X);
Y = create_class("Y", __Y_parents, __Y_attrs);
var __args_32, __kwargs_32;
__args_32 = create_array();
__kwargs_32 = {};
var __args_33, __kwargs_33;
__args_33 = create_array(get_attribute(A, "__call__")(__args_32, __kwargs_32), A);
__kwargs_33 = {};
var __args_34, __kwargs_34;
__args_34 = create_array(get_attribute(isinstance, "__call__")(__args_33, __kwargs_33), "A() is an instance of A");
__kwargs_34 = {};
get_attribute(test_true, "__call__")(__args_34, __kwargs_34);
var __args_35, __kwargs_35;
__args_35 = create_array();
__kwargs_35 = {};
var __args_36, __kwargs_36;
__args_36 = create_array(get_attribute(B, "__call__")(__args_35, __kwargs_35), A);
__kwargs_36 = {};
var __args_37, __kwargs_37;
__args_37 = create_array(get_attribute(isinstance, "__call__")(__args_36, __kwargs_36), "B() is an instance of A");
__kwargs_37 = {};
get_attribute(test_true, "__call__")(__args_37, __kwargs_37);
var __args_38, __kwargs_38;
__args_38 = create_array();
__kwargs_38 = {};
var __args_39, __kwargs_39;
__args_39 = create_array(get_attribute(B, "__call__")(__args_38, __kwargs_38), A);
__kwargs_39 = {};
var __args_40, __kwargs_40;
__args_40 = create_array(get_attribute(isinstance, "__call__")(__args_39, __kwargs_39), "B() is an instance of B");
__kwargs_40 = {};
get_attribute(test_true, "__call__")(__args_40, __kwargs_40);
var __args_41, __kwargs_41;
__args_41 = create_array(B, B);
__kwargs_41 = {};
var __args_42, __kwargs_42;
__args_42 = create_array(get_attribute(isinstance, "__call__")(__args_41, __kwargs_41), "B is not an instance of B");
__kwargs_42 = {};
get_attribute(test_false, "__call__")(__args_42, __kwargs_42);
var __args_43, __kwargs_43;
__args_43 = create_array(B, A);
__kwargs_43 = {};
var __args_44, __kwargs_44;
__args_44 = create_array(get_attribute(isinstance, "__call__")(__args_43, __kwargs_43), "B is not an instance of A");
__kwargs_44 = {};
get_attribute(test_false, "__call__")(__args_44, __kwargs_44);
var __args_45, __kwargs_45;
__args_45 = create_array();
__kwargs_45 = {};
var __args_46, __kwargs_46;
__args_46 = create_array(get_attribute(B, "__call__")(__args_45, __kwargs_45), X);
__kwargs_46 = {};
var __args_47, __kwargs_47;
__args_47 = create_array(get_attribute(isinstance, "__call__")(__args_46, __kwargs_46), "B() is not an instance of X");
__kwargs_47 = {};
get_attribute(test_false, "__call__")(__args_47, __kwargs_47);
var __args_48, __kwargs_48;
__args_48 = create_array();
__kwargs_48 = {};
var __args_49, __kwargs_49;
__args_49 = create_array(get_attribute(B, "__call__")(__args_48, __kwargs_48), Y);
__kwargs_49 = {};
var __args_50, __kwargs_50;
__args_50 = create_array(get_attribute(isinstance, "__call__")(__args_49, __kwargs_49), "B() is not an instance of Y");
__kwargs_50 = {};
get_attribute(test_false, "__call__")(__args_50, __kwargs_50);
}

var __args_51, __kwargs_51;
__args_51 = create_array(test_isinstance);
__kwargs_51 = {};
get_attribute(get_attribute(tests, "append"), "__call__")(__args_51, __kwargs_51);
var __iterator__, test;
__iterator__ = get_attribute(get_attribute(tests, "__iter__"), "__call__")(create_array(), {});
try {
test = get_attribute(__iterator__, "next")(create_array(), {});
while(true) {
var __args_52, __kwargs_52;
__args_52 = create_array();
__kwargs_52 = {};
get_attribute(test, "__call__")(__args_52, __kwargs_52);
test = get_attribute(__iterator__, "next")(create_array(), {});
}
}
catch(__exception__) {
if (__exception__ == StopIteration || isinstance([__exception__, StopIteration])) {

}

}

