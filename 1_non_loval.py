def update_order():
    chai_type="Elaichi"
    def kitchen():
        nonlocal chai_type
        chai_type ="Kesar"
    kitchen()
    print("After kichen update", chai_type)

update_order()