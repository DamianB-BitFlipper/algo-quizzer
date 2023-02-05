# Simulating a Classroom Quiz on Algorand

This is a demo project showcasing how to use [AlgoPytest](https://github.com/DamianB-BitFlipper/algopytest "AlgoPytest") to test an Algorand application incorporating multiple smart contracts interacting with one another. The premise is teacher quizzing their students. A teacher smart contract posts a solution to a problem on the Algorand blockchain. Then multiple student smart contracts may submit solutions to the Algorand blockchain and verify whether they are correct or not by comparing with the teacher's solution.

## Smart Contracts

Two smart contract programs are contained within the `assets` directory of this project under `teacher_program.py` and `student_program.py`.

The teacher smart contract specification is:
- Initialization: Set the creator of the teacher application to be the teacher.
- Delete: Only the teacher may delete the teacher application.
- Update: Only the teacher may update the teacher application.
- OptIn: Anyone may opt-in to the teacher application.
- CloseOut: Anyone may close-out of the teacher application.
- Command `"set_solution"`: Set the solution supplied with this application call. Only the teacher is permitted to set the solution.
- Command `"clear_solution"`: Any set solution is erased. If no solution is set, it does nothing. Only the teacher is permitted to clear the solution.

The student smart contract specification is:
- Initialization: Set the creator of the student application to be the teacher.
- Delete: Only the teacher may delete the student application.
- Update: Only the teacher may update the student application.
- OptIn: Anyone may opt-in to the student application.
- CloesOut: Anyone may close-out of the student application.
- Command `"check_solution"`: A student submits a solution which is checked against any posted solution by the teacher. If no solution is posted by the teacher, this command fails. Otherwise, if the solution matches the teacher's solution, set the `"is_correct"` local variable of the student to `"1"`. If the submitted solution differs, set that local variable to `"0"`.

## Testing

All of the unit tests are located in the `tests` directory. The code in `conftest.py` demonstrates how to initialize *AlgoPytest* and then the test files with names beginning with `test_` demonstrate how to properly test all parts of the Algorand Diploma Smart Contract.

### Running the Tests

1. Testing this DApp requires the [*AlgoPytest*](https://github.com/DamianB-BitFlipper/algopytest) plugin. Follow the installation instructions as well as the usage regarding starting the sandbox and setting up the relevant environment variables.
   - In most cases, the relevant *AlgoPytest* environemnt variables to set are `SANDBOX_DIR` and `INITIAL_FUNDS_ACCOUNT`.
   - Since this DApp is not an installable Python package, you will need to add the `assets` directory to your `PYTHONPATH` environment variable. That may be done with `export PYTHONPATH=$PYTHONPATH:/path/to/algo-quizzer/assets/` for example.

2. Simply run the tests by executing `pytest`in the base directory of `algo-quizzer`.