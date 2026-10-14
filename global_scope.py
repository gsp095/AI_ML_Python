chai_type ="Plain"

def front_desk():
    def kitchen():
        global chai_type
        chai_type ="Kesar"
    kitchen()
    print("After kitchen update", chai_type)

front_desk()
print("After kitchen update", chai_type)
