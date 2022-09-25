# This example is provided for informational purposes only and has not been audited for security.
from pyteal import *

var_teacher = Bytes("teacher")
var_solution = Bytest("solution")

def teacher_program():
    """
    This smart contract contains the quiz ``solution`` set by the ``teacher``.
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

    # Code block invoked during quiz solution setting. Only the `teacher`
    # may invoke this block with two arguments. The first argument is
    # "set_solution" used by the control flow below. The second argument
    # is the quiz solution which is set to the global variable `var_solution`.
    set_solution = Seq([
        # Sanity checks
        Assert(is_teacher),
        Assert(Txn.application_args.length() == Int(2)),

        App.globalPut(var_solution, Txn.application_args[1]),
    ])

    # Code block invoked to clear the quiz solution. Only the `teacher`
    # may invoke this block with one argument. The first argument is
    # "clear_solution" used by the control flow below.
    clear_solution = Seq([
        # Sanity checks
        Assert(is_teacher),
        Assert(Txn.application_args.length() == Int(1)),

        App.globalDel(var_solution),
    ])
    
    # Control flow logic of the smart contract
    program = Cond(
        [Txn.application_id() == Int(0), init_contract],
        [Txn.on_completion() == OnComplete.DeleteApplication, Return(is_teacher)],
        [Txn.on_completion() == OnComplete.UpdateApplication, Return(is_teacher)],
        [Txn.on_completion() == OnComplete.OptIn, Return(Int(1))],
        [Txn.on_completion() == OnComplete.CloseOut, Return(Int(1))],
        [Txn.application_args[0] == Bytes("set_solution"), set_solution],
        [Txn.application_args[0] == Bytes("clear_solution"), clear_solution],
    )

if __name__ == "__main__":
    print(compileTeal(teacher_program(), Mode.Application, version=5))
