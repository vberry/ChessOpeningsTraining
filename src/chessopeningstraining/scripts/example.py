# This is an example file contaning 1 doctest to show how they should be implemented in the doc string 
# at the top of a function
# The result should describe which output (standard output AND returned value) is expected
#
# Run the test from the project's root folder with: uv run python -m doctest src/chessopeningstraining/example.py -v
#

def one_f():
    """ 
    This is a doc comment
    >>> one_f()
    hello
    again
    23
    """
    print('hello')
    print('again')
    return 2


if __name__ == "__main__":
    print("First runs the doctests")
    import doctest
    import sys
    test_res=doctest.testmod()
    if test_res.failed:
        print('some tests failed: refusing to run the script') 
        sys.exit()
    print('All tests are OK, proceeding with running the script')
    # Main script:
    one_f()

