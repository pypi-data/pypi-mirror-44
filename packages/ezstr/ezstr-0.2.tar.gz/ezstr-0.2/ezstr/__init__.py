def tostr(cls):
    """
    Decorator function to create a str representation for an object
    :param cls: The class to be passed to the function
    :return: The updated class
    """
    def __str__(self):
        obj_name = type(self).__name__
        attr = ', '.join('{}={}'.format(*item) for item in vars(self).items())
        return '{}({})'.format(obj_name, attr)

    cls.__str__ = __str__
    return cls