jjj = get_attribute(J, "__call__")("#foo");
hhh = get_attribute(get_attribute(jjj.addClass("green"), "addClass"), "__call__")("red");
get_attribute(get_attribute(hhh, "animate"), "__call__")({"opacity": 0}, 1000);

