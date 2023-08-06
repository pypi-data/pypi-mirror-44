DCCP
====

DCCP package provides an organized heuristic for convex-concave programming.
It tries to solve nonconvex problems where all expressions have known curvature according to the rules of disciplined convex programming (DCP) but the objective and constraint right and left-hand sides may have any curvature (e.g., maximizing a convex expression). The full details of our approach are discussed in [the associated paper](https://stanford.edu/~boyd/papers/dccp.html). DCCP is built on top of [CVXPY](http://www.cvxpy.org/), a domain-specific language for convex optimization embedded in Python.

DCCP is now available for CVXPY 1.0

Installation
------------
You should first install [CVXPY](http://www.cvxpy.org/), following the instructions [here](http://www.cvxpy.org/en/latest/install/index.html).
Then install DCCP by running ``pip install dccp``.
To install from source, clone the repository and run ``python setup.py install`` inside.

DCCP rules
----------
A problem satisfies the rules of disciplined convex-concave programming (DCCP) if it has the form
```
minimize/maximize o(x)
subject to  l_i(x) ~ r_i(x),  i=1,...,m,
```
where ``o`` (the objective), ``l_i`` (lefthand sides), and ``r_i`` (righthand sides) are expressions (functions
of the variable ``x``) with curvature known from the DCP composition rules, and ``∼`` denotes one of the
relational operators ``=``, ``<=``, or ``>=``.

In a disciplined convex program, the curvatures of ``o``, ``l_i``, and ``r_i`` are restricted to ensure that the problem is convex. For example, if the objective is ``maximize o(x)`` then ``o`` must be convex according to the DCP composition rules. In a disciplined convex-concave program, by contrast, the objective and constraint right and left-hand sides can have any curvature, so long as all expressions satisfy the DCP composition rules.

Example
-------
The following code uses DCCP to approximately solve a simple nonconvex problem.
```python
import cvxpy as cvx
import dccp
x = cvx.Variable(2)
y = cvx.Variable(2)
myprob = cvx.Problem(cvx.Maximize(cvx.norm(x-y,2)), [0<=x, x<=1, 0<=y, y<=1])
print("problem is DCP:", myprob.is_dcp())   # false
print("problem is DCCP:", dccp.is_dccp(myprob))  # true
result = myprob.solve(method = 'dccp')
print("x =", x.value)
print("y =", y.value)
print("cost value =", result[0])
```
The output of the above code is as follows.
```
problem is DCP: False
problem is DCCP: True
iteration= 1 cost value =  1.38578967145 tau =  0.005
iteration= 2 cost value =  1.41421356224 tau =  0.006
iteration= 3 cost value =  1.41421356224 tau =  0.0072
========================
x = [[  4.84999696e-11]
 [  4.84999696e-11]]
y = [[ 1.]
 [ 1.]]
cost value = 1.41421356224
```

The solutions obtained by DCCP depend heavily on the initial point the CCP algorithm starts from.
By default the algorithm starts from a random initial point.
You can specify an initial point manually by setting the ``value`` field of the problem variables.
For example, the following code runs the CCP algorithm with the specified initial values for ``x`` and ``y``:
```python
x.value = numpy.array([1,2])
y.value = numpy.array([-1,1])
result = myprob.solve(method = 'dccp')
```


Functions and attributes
----------------
* ``is_dccp(problem)`` returns a boolean indicating if an optimization problem satisfies DCCP rules.
* ``expression.grad`` returns a dictionary of the gradients of a DCP expression
w.r.t. its variables at the points specified by ``variable.value``. (This attribute
is also in the core CVXPY package.)
* ``expression.domain`` returns a list of constraints describing the domain of a
DCP expression. (This attribute is also in the core CVXPY package.)
* ``linearize(expression)`` returns the linearization of a DCP expression at the point specified by ``variable.value``.
* ``convexify_obj(objective)`` returns the convexified objective of a DCCP objective.
* ``convexify_constr(constraint)`` returns the convexified constraint (without slack
variables) of a DCCP constraint, and if any expression is linearized, its domain is also returned.

Constructing and solving problems
---------------------------------
The components of the variable, the objective, and the constraints are constructed using standard CVXPY syntax. Once the user has constructed a problem object, they can apply the following solve method:
* ``problem.solve(method = 'dccp')`` applies the CCP heuristic, and returns the value of the cost function, the maximum value of the slack variables, and the value of each variable. Additional arguments can be used to specify the parameters.

Solve method parameters:
* The ``max_iter`` parameter sets the maximum number of iterations in the CCP algorithm. The default is 100.
* The ``tau`` parameter trades off satisfying the constraints and minimizing the objective. Larger ``tau`` favors satisfying the constraints. The default is 0.005.
* The ``mu`` parameter sets the rate at which ``tau`` increases inside the CCP algorithm. The default is 1.2.
* The ``tau_max`` parameter upper bounds how large ``tau`` can get. The default is 1e8.
* The ``solver`` parameter specifies what solver to use to solve convex subproblems.
* The ``ccp_times`` parameter specifies how many random initial points to run the algorithm from. The default is 1.

Any additional keyword arguments will be passed to the solver for convex subproblems. For example, ``warm_start=True`` will tell the convex solver to use a warm start.
