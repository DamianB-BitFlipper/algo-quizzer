import pytest
from pytest import fixture

import algosdk

from algopytest import (
    application_global_state,
    application_local_state,
    call_app
)

SOLUTION = "c^2 = a^2 + b^2"
WRONG_SOLUTION = "c^2 = a^2 - b^2"

@fixture
def teacher_smart_contract_with_solution_id(teacher, teacher_smart_contract_id):
    # Set the solution
    call_app(
        sender=teacher,
        app_id=teacher_smart_contract_id,
        app_args=["set_solution", SOLUTION],
    )

    # Return the same `teacher_smart_contract_id`, but after it has a `solution` set
    return teacher_smart_contract_id
    
def test_teacher_set_solution(teacher_smart_contract_with_solution_id):    
    # Read the application's global state which includes the set solution
    state = application_global_state(
        teacher_smart_contract_with_solution_id,
        address_fields=['teacher'],        
    )
    
    # Assert that the `solution` was set properly
    assert state['solution'] == SOLUTION

def test_student_set_solution_raises(student1_in, teacher_smart_contract_id):
    # A student should not be able to set the solution
    with pytest.raises(algosdk.error.AlgodHTTPError, match=r'transaction .*: logic eval error: assert failed'):
        call_app(
            sender=student1_in,
            app_id=teacher_smart_contract_id,
            app_args=["set_solution", WRONG_SOLUTION],
        )

def test_teacher_clear_solution(teacher, teacher_smart_contract_with_solution_id):    
    # Clear the solution
    call_app(
        sender=teacher,
        app_id=teacher_smart_contract_with_solution_id,
        app_args=["clear_solution"]
    )

    # Read the application's global state which should have an empty solution
    state = application_global_state(
        teacher_smart_contract_with_solution_id,
        address_fields=['teacher'],        
    )

    assert 'solution' not in state

def test_student_clear_solution_raises(student1_in, teacher_smart_contract_with_solution_id):
    # A student should not be able to clear the solution
    with pytest.raises(algosdk.error.AlgodHTTPError, match=r'transaction .*: logic eval error: assert failed'):
        call_app(
            sender=student1_in,
            app_id=teacher_smart_contract_with_solution_id,
            app_args=["clear_solution"],
        )    

def test_teacher_clear_nonexistent_solution(teacher, teacher_smart_contract_id):
    # Clear a nonexistent solution which should be a No-Op
    call_app(
        sender=teacher,
        app_id=teacher_smart_contract_id,
        app_args=["clear_solution"]
    )

    # Read the application's global state which should have an empty solution
    state = application_global_state(
        teacher_smart_contract_id,
        address_fields=['teacher'],        
    )

    assert 'solution' not in state


def test_student_correct_solution(student1_in, teacher_smart_contract_with_solution_id, student_smart_contract_id):
    call_app(
        sender=student1_in,
        app_id=student_smart_contract_id,
        app_args=["check_solution", SOLUTION],
        foreign_apps=[teacher_smart_contract_with_solution_id],
    )

    # Read the student's local state which should have the integer `1` signaling a correct solution
    state = application_local_state(student_smart_contract_id, student1_in)

    assert state['is_correct'] == 1


def test_student_wrong_solution(student1_in, teacher_smart_contract_with_solution_id, student_smart_contract_id):
    call_app(
        sender=student1_in,
        app_id=student_smart_contract_id,
        app_args=["check_solution", WRONG_SOLUTION],
        foreign_apps=[teacher_smart_contract_with_solution_id],
    )

    # Read the student's local state which should have the integer `1` signaling a correct solution
    state = application_local_state(student_smart_contract_id, student1_in)

    assert state['is_correct'] == 0

def test_student_check_solution_nonexistent_solution_raises(student1_in, teacher_smart_contract_id, student_smart_contract_id):
    with pytest.raises(algosdk.error.AlgodHTTPError, match=r'transaction .*: logic eval error: assert failed'):
        call_app(
            sender=student1_in,
            app_id=student_smart_contract_id,
            app_args=["check_solution", SOLUTION],
            foreign_apps=[teacher_smart_contract_id],
        )

def test_multiple_students_submitting_solutions(student1_in, student2_in, student3_in, teacher_smart_contract_with_solution_id, student_smart_contract_id):
    student_solutions = [
        (student1_in, SOLUTION),
        (student2_in, SOLUTION),
        (student3_in, WRONG_SOLUTION),
    ]

    # Call the `student_smart_contract_id` with the respective solutions
    for student_in, solution in student_solutions:
        call_app(
            sender=student_in,
            app_id=student_smart_contract_id,
            app_args=["check_solution", solution],
            foreign_apps=[teacher_smart_contract_with_solution_id],
        )

    # After all of the solutions have been submitted, retrieve the local
    # state of each student and make sure it is correct
    for student_in, solution in student_solutions:
        state = application_local_state(student_smart_contract_id, student_in)

        is_correct = solution == SOLUTION        
        assert state['is_correct'] == is_correct
