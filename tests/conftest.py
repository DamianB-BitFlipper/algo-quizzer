from pytest import fixture
from algopytest import (
    deploy_smart_contract,
    opt_in_app,
    close_out_app,
)

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

def opt_in_student(student, smart_contract_id):
    """Opt-in the ``student`` to the ``smart_contract_id`` application."""
    opt_in_app(student, smart_contract_id)

    # The test runs here    
    yield student
    
    # Clean up by closing out of the application    
    close_out_app(student, smart_contract_id)

@fixture
def student1_in(user1, student_smart_contract_id):
    """Create a ``student1`` fixture that has already opted in to ``student_smart_contract_id``."""
    yield from opt_in_student(user1, student_smart_contract_id)

@fixture
def student2_in(user2, student_smart_contract_id):
    """Create a ``student2`` fixture that has already opted in to ``student_smart_contract_id``."""
    yield from opt_in_student(user2, student_smart_contract_id)

@fixture
def student3_in(user3, student_smart_contract_id):
    """Create a ``student3`` fixture that has already opted in to ``student_smart_contract_id``."""
    yield from opt_in_student(user3, student_smart_contract_id)    
