# This example is provided for informational purposes only and has not been audited for security.
from pyteal import *

var_teacher = Bytes("teacher")
var_is_correct = Bytes("is_correct")

def student_program():
    """
    This smart contract simply validates if a solution submitted 
    is correct according to the `teacher_program` smart contract.
    """
    # Code block invoked during contract initialization. Sets the
    # `teacher` to be the sender (creator) of this smart contract
    init_contract = Seq([
        App.globalPut(var_teacher, Txn.sender()),
        Return(Int(1))
    ])

    # Checks if the sender of the current transaction invoking this
    # smart contract is the current `teacher`
    is_teacher = Txn.sender() == App.globalGet(var_teacher)
    
    # Code block invoked by a student to verify if their submitted solution
    # is correct according to the `teacher_program` smart contract. The student
    # invokes this block with two arguments and one application argument.
    # The first argument is "check_solution" used by the control flow below.
    # The second argument is the solution to be checked. The application argument
    # should be the `teacher_program` so that this smart contract can retrieve
    # the correct solution. If the solution is correct, the local storage of
    # the student at `var_is_correct` is set to `Int(1)`. Otherwise, it is
    # set to `Int(0)`.
    student_solution = Txn.application_args[1]
    check_solution = Seq([
        # Sanity checks
        Assert(Txn.application_args.length() == Int(2)),

        If(App.globalGetEx(Int(1), Bytes("solution")) == student_solution)
        .Then(App.localPut(Int(1), var_is_correct, Int(1)))
        .Else(App.localPut(Int(1), var_is_correct, Int(0)))
    ])
    
    # Control flow logic of the smart contract
    program = Cond(
        [Txn.application_id() == Int(0), init_contract],
        [Txn.on_completion() == OnComplete.DeleteApplication, Return(is_teacher)],
        [Txn.on_completion() == OnComplete.UpdateApplication, Return(is_teacher)],
        [Txn.on_completion() == OnComplete.OptIn, Return(Int(1))],
        [Txn.on_completion() == OnComplete.CloseOut, Return(Int(1))],
        [Txn.application_args[0] == Bytes("check_solution"), check_solution],
    )

if __name__ == "__main__":
    print(compileTeal(student_program(), Mode.Application, version=5))

