from merge_files.mergers.env import env


def test_no_change():
    value = "\n".join(["KEY=yay", "HOST=localhost"]).encode()

    result = env(value, value)

    assert result == value


def test_overwrite_value():
    target = "\n".join(["KEY=old_value"]).encode()
    source = "\n".join(["KEY=new_value"]).encode()

    expected = "\n".join(["KEY=new_value"]).encode()

    actual = env(source, target, True)

    assert actual == expected


def test_add_variable_no_overwrite():
    source = "\n".join(["KEY=default", "NEW=cool"]).encode()
    target = "\n".join(["KEY=mine", "HOST=localhost"]).encode()

    expected = "\n".join(["KEY=mine", "HOST=localhost", "NEW=cool"]).encode()

    actual = env(source, target)

    assert actual == expected


def test_variable_with_equals_sign():
    target = "\n".join(["KEY=existing=overwrite", "NEW=new=value"]).encode()
    source = "\n".join(["KEY=overwrite=me", "HOST=default=new"]).encode()

    expected = "\n".join(
        ["KEY=overwrite=me", "NEW=new=value", "HOST=default=new"]
    ).encode()

    actual = env(source, target, True)

    assert actual == expected


def test_add_comments():
    target = "\n".join(["KEY=mine", "HOST=localhost"]).encode()
    source = "\n".join(["KEY=default", "# Comment"]).encode()

    expected = "\n".join(["KEY=mine", "HOST=localhost", "# Comment"]).encode()

    actual = env(source, target)

    assert actual == expected


def test_keep_comments():
    source = "\n".join(["KEY=default", "OTHER=other_value # yup"]).encode()
    target = "\n".join(["KEY=custom", "# Comment"]).encode()

    expected = "\n".join(
        ["KEY=custom", "# Comment", "OTHER=other_value # yup"]
    ).encode()

    actual = env(source, target)

    assert actual == expected


def test_keep_comments_with_equals():
    source = "\n".join(["NEW_VAR=Truthy"]).encode()
    target = "\n".join(["#UNCOMMENT_ME=n # explode()", "OTHER_VAR"]).encode()

    expected = "\n".join(
        ["#UNCOMMENT_ME=n # explode()", "OTHER_VAR", "NEW_VAR=Truthy"]
    ).encode()

    actual = env(source, target)

    assert actual == expected


def test_dont_duplicate_comments():
    source = "\n".join(["#UNCOMMENT_ME=n # explode()", "NEW_VAR=y"]).encode()
    target = "\n".join(["#UNCOMMENT_ME=n # explode()", "OTHER_VAR"]).encode()

    expected = "\n".join(
        ["#UNCOMMENT_ME=n # explode()", "OTHER_VAR", "NEW_VAR=y"]
    ).encode()

    actual = env(source, target)

    assert actual == expected
