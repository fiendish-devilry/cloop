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

   >>> from loop import Loop
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

   >>> from loop import Loop
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

Edge Cases
----------

:class:`loop.Loop` correctly handles many tricky edge cases.

Loop Condition Never True
~~~~~~~~~~~~~~~~~~~~~~~~~

pass
