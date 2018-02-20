C-Style For-Loops as Python Classes
===================================

*Because that's totally a thing you wanted.*

Basic Usage
-----------

:class:`loop.Loop` lets you write C-style loops in the bodies of Python classes.

.. code-block:: python

   >>> from loop import Loop
   >>> class For(Loop):
   ...     x = 0; x < 5; ++x
   ...     print("Body:", x)
   ...
   Body: 0
   Body: 1
   Body: 2
   Body: 3
   Body: 4

Control Flow
------------

Inside the body of the loop, you can call ``break_()`` and ``continue_()`` to
break and continue the loop execution.

.. code-block:: python

   >>> class For(Loop):
   ...     x = 0; x < 5; ++x
   ...     if x == 2:
   ...         print("Skipping 2")
   ...         continue_()
   ...     print("Body:", x)
   ...
   Body: 0
   Body: 1
   Skipping 2
   Body: 3
   Body: 4

.. code-block:: python

   >>> class For(Loop):
   ...     x = 0; x < 5; ++x
   ...     if x == 2:
   ...         print("Breaking on 2")
   ...         break_()
   ...     print("Body:", x)
   ...
   Body: 0
   Body: 1
   Breaking on 2

Edge Case Handling
------------------

:class:`Loop` correctly handle tricky edge cases.

Loop Condition Never True
~~~~~~~~~~~~~~~~~~~~~~~~~

If the loop condition is initially False, the loop body is never executed.

.. code-block:: python

   >>> iters = []
   >>> class For(Loop):
   ...     x = 0; x > 100; ++x
   ...     iters.append(x)
   ...
   >>> iters
   []

Loops Inside Functions
~~~~~~~~~~~~~~~~~~~~~~

:class:`Loop` bodies can refer to local variables of enclosing functions.

.. code-block:: python

>>> def func():
...     iters = []
...     class For(Loop):
...         x = 0; x < 5; ++x
...         iters.append(x)
...     return iters
...
>>> func()
[0, 1, 2, 4, 4]
