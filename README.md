To run this project locally and see that the tests passed, you have to follow
the steps below.

1. Clone the repository
2. Create the database running the code:

```
psql -f tournament.sql
```

3. Run the tests module by running:

```
python tournament_test.py
```

The Python version must be Python 2.

The schema is defined in the tournament.sql file and the Python code is in
tournament.py.

The extra credits will be done in a future version.
