#include <Python.h>

#include "libsemigroups/adapters.hpp"
#include "libsemigroups/constants.hpp"

class PythonElement {
 private:
  PyObject *_value;

 public:
  PythonElement() : _value(Py_None) {}

  explicit PythonElement(PyObject *value) : _value(value) {
    Py_INCREF(value);
  }

  // Should there be a destructor?

  PyObject *get_value() const {
    return _value;
  }

  bool operator==(PythonElement const &that) const {
    return PyObject_RichCompareBool(this->_value, that._value, Py_EQ);
  }

  bool operator<(PythonElement const &that) const {
    return PyObject_RichCompareBool(this->_value, that._value, Py_LT);
  }

  PythonElement operator*(PythonElement const &that) const {
    PyObject *product;
    if (this->_value == Py_None) {
      product = that._value;
    } else if (that._value == Py_None) {
      product = this->_value;
    } else {
      product = PyNumber_Multiply(this->_value, that._value);
    }
    return PythonElement(product);
  }
};

namespace libsemigroups {

  template <>
  struct Complexity<PythonElement> {
    size_t operator()(PythonElement) const noexcept {
      return POSITIVE_INFINITY;
    }
  };

  template <>
  struct Degree<PythonElement> {
    size_t operator()(PythonElement) const noexcept {
      return 0;
    }
  };

  template <>
  struct IncreaseDegree<PythonElement> {
    PythonElement operator()(PythonElement x) const noexcept {
      return x;
    }
  };

  template <>
  struct One<PythonElement> {
    PythonElement operator()(PythonElement) const noexcept {
      return PythonElement(Py_None);
    }
  };

  template <>
  struct Product<PythonElement> {
    void operator()(PythonElement &xy,
                    PythonElement  x,
                    PythonElement  y,
                    size_t = 0) const noexcept {
      xy = x * y;
    }
  };
}  // namespace libsemigroups

template <>
struct std::hash<PythonElement> {
  size_t operator()(PythonElement const &that) const {
    return PyObject_Hash(that.get_value());
  }
};
