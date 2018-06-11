import cppyy
cppyy.cppdef("""

struct AAA {
  virtual ~AAA() {}
};

struct BBB : public AAA {
  int i;
};
""")


cppyy.cppdef("BBB T({});")
cppyy.cppdef("BBB v[1] { T };")
cppyy.gbl.v    # boom
