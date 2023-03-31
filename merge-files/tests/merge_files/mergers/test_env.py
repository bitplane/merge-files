# from merge_files.mergable.env import env


# def test_no_change():
#     value = "\n".join(["KEY=yay", "HOST=localhost"]).encode()

#     result = env(value, value)

#     assert result == value


# def test_overwrite_value():
#     dest = "\n".join(["KEY=custom"]).encode()
#     source = "\n".join(["KEY=default"]).encode()

#     expected = "\n".join(["KEY=default"]).encode()

#     actual = env(source, dest, True)

#     assert actual == expected


# def test_change_variable():
#     dest = "\n".join(["KEY=mine", "HOST=localhost"]).encode()
#     source = "\n".join(["KEY=default", "NEW=cool"]).encode()

#     expected = "\n".join(["KEY=mine", "HOST=localhost", "NEW=cool"]).encode()

#     actual = env(source, dest)

#     assert actual == expected


# def test_add_comments():
#     dest = "\n".join(["KEY=mine", "HOST=localhost"]).encode()
#     source = "\n".join(["KEY=default", "# Comment"]).encode()

#     expected = "\n".join(["KEY=mine", "HOST=localhost", "# Comment"]).encode()

#     actual = env(source, dest)

#     assert actual == expected


# def test_keep_comments():
#     dest = "\n".join(["KEY=custom", "# Comment"]).encode()
#     source = "\n".join(["KEY=default", "OTHER=other_value # yup"]).encode()

#     expected = "\n".join(
#         ["KEY=custom", "# Comment", "OTHER=other_value # yup"]
#     ).encode()

#     actual = env(source, dest)

#     assert actual == expected


# def test_keep_comments_with_equals():
#     dest = "\n".join(["#UNCOMMENT_ME=n # explode()", "OTHER_VAR"]).encode()
#     source = "\n".join(["NEW_VAR=Truthy"]).encode()

#     expected = "\n".join(
#         ["#UNCOMMENT_ME=n # explode()", "OTHER_VAR", "NEW_VAR=Truthy"]
#     ).encode()

#     actual = env(source, dest)

#     assert actual == expected


# def test_dont_duplicate_comments():
#     dest = "\n".join(["#UNCOMMENT_ME=n # explode()", "OTHER_VAR"]).encode()
#     source = "\n".join(["#UNCOMMENT_ME=n # explode()", "NEW_VAR=y"]).encode()

#     expected = "\n".join(
#         ["#UNCOMMENT_ME=n # explode()", "OTHER_VAR", "NEW_VAR=y"]
#     ).encode()

#     actual = env(source, dest)

#     assert actual == expected
