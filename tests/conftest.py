from pytest import fixture
from algopytest import deploy_smart_contract

# Load the smart contracts from this project. The path to find these
# imports is set by the environment variable `$PYTHONPATH`.
from teacher_program import teacher_program
from student_program import student_program
from clear_program import clear_program

@fixture
def teacher(owner):
    """Rename the ``owner`` fixture to be the ``teacher``."""
    yield owner

@fixture
def teacher_smart_contract_id(teacher):
    with deploy_smart_contract(
            teacher,
            approval_program=teacher_program(), 
            clear_program=clear_program(),
            global_bytes=2,
    ) as app_id:
        yield app_id

@fixture
def student_smart_contract_id(teacher):
    with deploy_smart_contract(
            teacher,
            approval_program=student_program(), 
            clear_program=clear_program(),
            local_ints=1,
            global_bytes=1,
    ) as app_id:
        yield app_id        
