from models import Test

# we need to make it entered by the user
def get_tests():
    tests = Test.query.order_by(Test.id.desc()).all()
    return tests
    # return [t.name for t in tests] # just the name
    # return CATEGORIES

