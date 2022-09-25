import pytest

from algopytest import application_global_state

def test_teacher_smart_contract_initialization(teacher, teacher_smart_contract_id):
    # Read the teacher's address from the application's global state
    state = application_global_state(
        smart_contract_id,
        address_fields=['teacher'],
    )
    
    # Assert that the `teacher` was set properly
    assert state['teacher'] == teacher.address    

def test_student_smart_contract_initialization(teacher, student_smart_contract_id):
    # Read the teacher's address from the application's global state
    state = application_global_state(
        smart_contract_id,
        address_fields=['teacher'],
    )
    
    # Assert that the `teacher` was set properly
    assert state['teacher'] == teacher.address    
    
