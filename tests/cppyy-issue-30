import cppyy

cppyy.cppdef("""
class AAA {
  private:
    class foo {
    };

  public:
    typedef foo bar;

    bar f() {
        return bar();
    }
};

AAA::bar x = AAA().f();
""")

cppyy.gbl.AAA().f()

