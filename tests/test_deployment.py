import pytest

from algopytest import (
    application_global_state,
)

def test_teacher_smart_contract_initialization(teacher, teacher_smart_contract_id):
    # Read the teacher's address from the application's global state
    state = application_global_state(
        teacher_smart_contract_id,
        address_fields=['teacher'],
    )
    
    # Assert that the `teacher` was set properly and that there is no `solution`
    assert state['teacher'] == teacher.address
    assert 'solution' not in state
    

def test_student_smart_contract_initialization(teacher, student_smart_contract_id):
    # Read the teacher's address from the application's global state
    state = application_global_state(
        student_smart_contract_id,
        address_fields=['teacher'],
    )
    
    # Assert that the `teacher` was set properly
    assert state['teacher'] == teacher.address    
    
