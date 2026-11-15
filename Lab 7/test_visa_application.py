from hypothesis import given, strategies as st, settings, HealthCheck
import pytest
from visa_application import parse_application, processing_average, payable_fee


# ---------------------------------------------------------------------------
# parse_application(text) -> (visa_type_title, entries_int)
# Expected contract:
#   - well-formed "visa:entries" (exactly one colon, integer entries)
#     returns (visa.strip().title(), int(entries))
#   - None or malformed input raises ValueError
# ---------------------------------------------------------------------------


@given(s=st.none())
def test_parse_application_none_raises_value_error(s):
    with pytest.raises(ValueError):
        parse_application(s)


@given(
    s=st.text(min_size=1, max_size=40).filter(lambda s: ":" not in s)
)
def test_parse_application_no_colon_raises_value_error(s):
    with pytest.raises(ValueError):
        parse_application(s)


multi_colon = st.builds(
    lambda a, b, c: f"{a}:{b}:{c}", st.text(), st.text(), st.text()
)


@given(s=multi_colon)
def test_parse_application_multiple_colons_raise_value_error(s):
    with pytest.raises(ValueError):
        parse_application(s)


visa_part = st.text(min_size=1, max_size=20).filter(lambda s: ":" not in s)
non_int_entries = st.text(min_size=0, max_size=20).filter(
    lambda t: t.strip() == "" or not t.strip().lstrip("-").isdigit()
)
non_int_parse = st.builds(lambda v, e: f"{v}:{e}", visa_part, non_int_entries)


@given(s=non_int_parse)
@settings(suppress_health_check=[HealthCheck.filter_too_much])
def test_parse_application_non_integer_entries_raise_value_error(s):
    with pytest.raises(ValueError):
        parse_application(s)


valid_parse = st.builds(
    lambda v, e: f"{v}:{e}",
    visa_part,
    st.integers(min_value=0, max_value=1000000),
)


@given(s=valid_parse)
def test_parse_application_valid_returns_title_and_int(s):
    visa_str, entries_str = s.split(":")
    visa, entries = parse_application(s)
    assert visa == visa_str.strip().title()
    assert entries == int(entries_str)


@given(s=valid_parse)
def test_parse_application_valid_returns_two_tuple(s):
    result = parse_application(s)
    assert isinstance(result, tuple)
    assert len(result) == 2


# ---------------------------------------------------------------------------
# processing_average(days_csv) -> floor(mean)
# Expected contract:
#   - comma-separated integer string returns sum(values) // len(values)
#   - None or malformed input raises ValueError
# ---------------------------------------------------------------------------


@given(s=st.none())
def test_processing_average_none_raises_value_error(s):
    with pytest.raises(ValueError):
        processing_average(s)


@given(
    s=st.text(min_size=1, max_size=40).filter(lambda s: "," not in s)
)
@settings(suppress_health_check=[HealthCheck.filter_too_much])
def test_processing_average_single_token(s):
    try:
        result = processing_average(s)
    except ValueError:
        return
    assert result == int(s)


csv_ints = st.lists(
    st.integers(min_value=-1000000, max_value=1000000), min_size=1, max_size=30
)
valid_csv = st.builds(lambda xs: ",".join(str(x) for x in xs), csv_ints)


@given(s=valid_csv)
def test_processing_average_returns_floor_mean(s):
    values = [int(x) for x in s.split(",")]
    assert processing_average(s) == sum(values) // len(values)


@given(s=valid_csv)
def test_processing_average_returns_int(s):
    assert isinstance(processing_average(s), int)


# ---------------------------------------------------------------------------
# payable_fee(text) -> max(fee * 1.18 - discount, 0)
# Expected contract:
#   - "fee|discount" numeric string returns the computed non-negative fee
#   - None or malformed input raises ValueError
# ---------------------------------------------------------------------------


@given(s=st.none())
def test_payable_fee_none_raises_value_error(s):
    with pytest.raises(ValueError):
        payable_fee(s)


@given(
    s=st.text(min_size=1, max_size=40).filter(lambda s: "|" not in s)
)
@settings(suppress_health_check=[HealthCheck.filter_too_much])
def test_payable_fee_no_pipe_raises_value_error(s):
    with pytest.raises(ValueError):
        payable_fee(s)


multi_pipe = st.builds(
    lambda a, b, c: f"{a}|{b}|{c}", st.text(), st.text(), st.text()
)


@given(s=multi_pipe)
def test_payable_fee_multiple_pipes_raise_value_error(s):
    with pytest.raises(ValueError):
        payable_fee(s)


fee_val = st.floats(
    min_value=-1000000, max_value=1000000, allow_nan=False, allow_infinity=False
)
discount_val = st.floats(
    min_value=-1000000, max_value=1000000, allow_nan=False, allow_infinity=False
)
valid_fee = st.builds(lambda f, d: f"{f}|{d}", fee_val, discount_val)


@given(s=valid_fee)
def test_payable_fee_computation(s):
    fee_s, discount_s = s.split("|")
    expected = max(float(fee_s) * 1.18 - float(discount_s), 0)
    assert payable_fee(s) == expected


@given(s=valid_fee)
def test_payable_fee_result_is_non_negative(s):
    assert payable_fee(s) >= 0
