import cppyy

cppyy.cppdef("""
    struct A {
      virtual void f () { };
    };

    struct B : public A {
      B() {}
      void f () override { };
    };
    """)

cppyy.py.pin_type(cppyy.gbl.B)
cppyy.cppdef("B T;")
cppyy.cppdef("B v[1] { T };")
cppyy.gbl.v
