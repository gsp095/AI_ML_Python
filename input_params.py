chai ="Ginger chai"
def prepare_chai(order):
    print("Preparing", order)

prepare_chai(chai)
print("After preparing", chai)

chai =[1,2,3]
def edit_chai(cup):
    cup[0] = 10
    print("After editing", cup)

edit_chai(chai)
print("After editing", chai)

def make_chai(tea, milk, suge):
    print("Making chai with", tea, milk, suge)


make_chai("Ginger", "Yes", "Low")
make_chai(suge="High", milk="No", tea="Green")
