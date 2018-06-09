namespace libsemigroups {

  class PythonElement {
  private:
    PyObject* _value;

  public:
    explicit PythonElement() : _value(Py_None) {
    }

    explicit PythonElement(PyObject* value) : _value(value) {
      Py_INCREF(value);
    }

    // Should there be a destructor?

    PyObject* get_value() const {
      return _value;
    }

    bool operator == (PythonElement const& that) const  {
      return PyObject_RichCompareBool(this->_value,
                                      that._value,
                                      Py_EQ);
    }

    bool operator<(PythonElement const& that) const  {
      return PyObject_RichCompareBool(this->_value,
                                      that._value,
                                      Py_LT);
    }

    PythonElement operator*(PythonElement const& that) const  {
      PyObject* product;
      if        (this->_value == Py_None) {
        product = that._value;
      } else if (that. _value == Py_None) {
        product = this->_value;
      } else {
        product
          = PyNumber_Multiply(this->_value,
                              that._value);
      }
      return PythonElement(product);

    }
  };


  template <>
    PythonElement one(PythonElement) {
    return PythonElement(Py_None);
  }

}

template <> struct std::hash<libsemigroups::PythonElement> {
  size_t operator()(libsemigroups::PythonElement const&that) const {
    return PyObject_Hash(that.get_value());
  }
};
