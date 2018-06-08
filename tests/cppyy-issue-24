import cppyy
cppyy.cppdef("""
template <typename T> struct A {
  static T const a;
};

template <typename T>
T const A<T>::a = 0;

template <typename T>
struct B : public A<T> {
  using A<T>::a;

  explicit B(int x) : A<T>() {
    if (x > a) {
      return;
    }
  }
};
""");
cppyy.gbl.B("size_t")(0)
