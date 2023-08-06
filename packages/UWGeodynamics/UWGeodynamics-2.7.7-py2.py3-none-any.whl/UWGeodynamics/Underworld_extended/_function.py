import underworld.function as fn
from UWGeodynamics import non_dimensionalise
from UWGeodynamics import UnitRegistry as u

class Function(fn.Function):

    @staticmethod
    def convert(obj):
        """
        This method will attempt to convert the provided input into an equivalent
        underworld function. If the provided input is already of Function type,
        it is immediately returned. Likewise, if the input is of None type, it is
        also returned.

        Parameters
        ----------
        obj: fn_like
            The object to be converted. Note that if obj is of type None or
            Function, it is simply returned immediately.
            Where obj is of type int/float/double, a Constant type function
            is returned which evaluates to the provided object's value.
            Where obj is of type list/tuple, a function will be returned
            which evaluates to a vector of the provided list/tuple's values
            (where possible).

        Returns
        -------
        Fn.Function or None.

        Examples
        --------
        >>> import underworld as uw
        >>> import underworld.function as fn

        >>> fn_const = fn.Function.convert( 3 )
        >>> fn_const.evaluate(0.) # eval anywhere for constant
        array([[3]], dtype=int32)

        >>> fn_const == fn.Function.convert( fn_const )
        True

        >>> fn.Function.convert( None )

        >>> fn1 = fn.input()
        >>> fn2 = 10.*fn.input()
        >>> fn3 = 100.*fn.input()
        >>> vec = (fn1,fn2,fn3)
        >>> fn_vec = fn.Function.convert(vec)
        >>> fn_vec.evaluate([3.])
        array([[   3.,   30.,  300.]])

        """
        if isinstance(obj, u.Quantity):
            obj = non_dimensionalise(obj)

        return super(Function, Function).convert(obj)

