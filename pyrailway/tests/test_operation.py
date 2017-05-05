from funcy import rcompose
from pyrailway.operation import success, failure, step, Operation


ENJOY_MSG = "great to hear, enjoy your day"
JOKE = "Broken pencils are pointless"


def hello(options, **k):
    print("hello")
    return True


def fail(options, **k):
    return False
    

def world(options, **k):
    print("world")
    return True


hello_world = rcompose(hello, world)


def how_are_you(options, params, **k):
    return params["happy"] == "yes"


def enjoy_your_day(options, **k):
    print(ENJOY_MSG)
    

def tell_joke(options, **k):
    options["joke"] = JOKE
    print(JOKE)
    
    
def test_step_function_args():
    def func(options, params, dep):
        assert options["params"] == params
        assert options["dep"] == dep
        
    op = Operation(step(func))
    op({"happy": "yes"}, dep=5)


def test_one_step(capsys):
    
    create = Operation(step(hello))
    result = create()

    out, _ = capsys.readouterr()
    assert out == "hello\n"
    
    assert result.success
    
    
def test_fail_step():
    op = Operation(step(fail))
    res = op()
    assert res.failure
    
    
def test_success_step():
    op = Operation(success(fail))
    res = op()
    assert res.success
    

def test_two_steps(capsys):
    op = Operation(step(hello), step(world))
    result = op()

    out, _ = capsys.readouterr()
    assert out == "hello\nworld\n"
    
    assert result.success


def test_input_success(capsys):
    op = Operation(step(how_are_you), success(enjoy_your_day))
    res = op({"happy": "yes"})
    out, _ = capsys.readouterr()
    assert out == ENJOY_MSG + "\n"
    assert res.success


def test_input_failure():
    op = Operation(step(how_are_you), success(enjoy_your_day))
    res = op({"happy": "I am sad"})
    assert res.failure
    
    
def test_with_failure_handler():
    op = Operation(step(how_are_you), success(enjoy_your_day), failure(tell_joke))
    res = op({"happy": "I am sad"})
    assert res.failure
    assert "joke" in res
    assert res["joke"] == JOKE
    
    
def test_fail_fast():
    def must_not_be_called(options, **k):
        raise AssertionError("this step must not be called after fail fast!")
    
    op = Operation(step(fail, fail_fast=True), failure(must_not_be_called))
    op()
