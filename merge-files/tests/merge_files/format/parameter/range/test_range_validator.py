import pytest
from merge_files.format.parameter.range import Range, Ranges
from pydantic import BaseModel, ValidationError


class ModelWithRange(BaseModel):
    range: Range


class ModelWithRanges(BaseModel):
    ranges: Ranges


def test_working_range_str():
    model = ModelWithRange(range="1:10")

    assert model.range.start == 1
    assert model.range.stop == 10


def test_working_range():
    model = ModelWithRange(range=Range("1:10"))

    assert model.range.start == 1
    assert model.range.stop == 10


def test_invalid_range():
    with pytest.raises(ValidationError):
        ModelWithRange(range="this isn't a range")


def test_working_ranges_str():
    model = ModelWithRanges(ranges="1:10, 20:30")

    assert len(model.ranges.ranges) == 2
    assert model.ranges.ranges[0].start == 1
    assert model.ranges.ranges[0].stop == 10
    assert model.ranges.ranges[1].start == 20
    assert model.ranges.ranges[1].stop == 30


def test_working_ranges():
    model = ModelWithRanges(ranges=Ranges("1:10, 20:30"))

    assert len(model.ranges.ranges) == 2
    assert model.ranges.ranges[0].start == 1
    assert model.ranges.ranges[0].stop == 10
    assert model.ranges.ranges[1].start == 20
    assert model.ranges.ranges[1].stop == 30


def test_invalid_ranges():
    with pytest.raises(ValidationError):
        ModelWithRanges(range="this isn't ranges")


def test_some_invalid_ranges():
    with pytest.raises(ValidationError):
        ModelWithRanges(range="0:10, boom!, 20:30")


def test_json_serialize_range():
    model = ModelWithRange(range="1:10")

    assert model.json() == '{"range": "1:10"}'


def test_json_serialize_ranges():
    model = ModelWithRanges(ranges="0:10, 20:30")

    model.ranges

    assert model.json() == '{"range": "10,20:30"}'
