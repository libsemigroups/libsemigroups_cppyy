import cppyy
cppyy.cppdef("""
    struct AAA {
      virtual ~AAA() {}
    };

    AAA t;
    """)
t = cppyy.gbl.t
cppyy.gbl.std.vector(type(t))([t])
