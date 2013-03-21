J = Object();
parents = new Array();
var J____init__ = function(self, arg) {
set_attribute(self, "j", jQuery(arg));

}
J.__init__ = J____init__;
var J__add = function(self, arg) {
j = get_attribute(self, "j");
o = j.add(arg);
return get_attribute(J, "__call__")(o);
}
J.add = J__add;
var J__add = function(self, arg) {
j = get_attribute(self, "j");
o = j.addBack(arg);
return get_attribute(J, "__call__")(o);
}
J.add = J__add;
var J__addClass = function(self, klass) {
j = get_attribute(self, "j");
o = j.addClass(klass);
return get_attribute(J, "__call__")(o);
}
J.addClass = J__addClass;
var J__after = function(self, arg) {
j = get_attribute(self, "j");
o = j.after(arg);
return get_attribute(J, "__call__")(o);
}
J.after = J__after;
var J__animate = function(self, properties, duration, easing, complete) {
j = get_attribute(self, "j");
o = j.animate(properties, duration, easing, complete);
return get_attribute(J, "__call__")(o);
}
J.animate = J__animate;
J = create_class("J", parents, J);

