import pytest
from visa_application import visa_fee, documents_complete, application_status


# --- visa_fee: visa_type branch (True: unknown, False: known) ---
def test_branch_visa_type_unknown():
    with pytest.raises(ValueError):
        visa_fee("diplomatic", 2, "normal", "B")


def test_branch_visa_type_known():
    assert visa_fee("tourist", 1, "normal", "B") == 0


# --- visa_fee: entries < 0 branch ---
def test_branch_entries_negative():
    with pytest.raises(ValueError):
        visa_fee("tourist", -1, "normal", "B")


def test_branch_entries_non_negative():
    assert visa_fee("tourist", 0, "normal", "B") == 0


# --- visa_fee: nationality_group == "A" and visa_type != "student' branch ---
def test_branch_nationality_a_not_student_true():
    # group A and not student => included incremented
    assert visa_fee("tourist", 3, "normal", "A") == 1 * 40


def test_branch_nationality_a_not_student_false_not_a():
    assert visa_fee("tourist", 3, "normal", "B") == 2 * 40


def test_branch_nationality_a_not_student_false_is_student():
    assert visa_fee("student", 3, "normal", "A") == 1 * 40


# --- visa_fee: extra <= 0 branch ---
def test_branch_extra_le_zero_true():
    assert visa_fee("tourist", 1, "normal", "B") == 0


def test_branch_extra_le_zero_false():
    assert visa_fee("tourist", 2, "normal", "B") == 1 * 40


# --- visa_fee: speed == "express" branch ---
def test_branch_speed_express_true():
    assert visa_fee("tourist", 6, "express", "B") == 5 * 100


def test_branch_speed_express_false():
    assert visa_fee("tourist", 6, "normal", "B") == 5 * 40


# --- visa_fee: extra > 5 branch ---
def test_branch_extra_gt_five_true():
    assert visa_fee("tourist", 8, "normal", "B") == 7 * 60


def test_branch_extra_gt_five_false():
    assert visa_fee("tourist", 6, "normal", "B") == 5 * 40


# --- visa_fee: nested speed == "express" inside extra > 5 ---
def test_branch_nested_express_true():
    assert visa_fee("tourist", 8, "express", "B") == 7 * 130


def test_branch_nested_express_false():
    assert visa_fee("tourist", 8, "normal", "B") == 7 * 60


# --- documents_complete: is_renewal branch ---
def test_branch_is_renewal_true():
    assert documents_complete(1, 0, True) is True


def test_branch_is_renewal_false():
    assert documents_complete(3, 2, False) is True


# --- documents_complete: photos < 2 branch ---
def test_branch_photos_lt_two_true():
    assert documents_complete(5, 1, False) is False


def test_branch_photos_lt_two_false():
    assert documents_complete(5, 2, False) is True


# --- application_status: is_express branch ---
def test_branch_is_express_true():
    assert application_status(5, True, False) == "closing"


def test_branch_is_express_false():
    assert application_status(20, False, False) == "closing"


# --- application_status: is_peak_season branch ---
def test_branch_is_peak_season_true():
    assert application_status(40, False, True) == "closing"


def test_branch_is_peak_season_false():
    assert application_status(20, False, False) == "closing"


# --- application_status: days_left >= cutoff branch ---
def test_branch_days_ge_cutoff_true():
    assert application_status(30, False, False) == "open"


def test_branch_days_ge_cutoff_false():
    assert application_status(20, False, False) == "closing"


# --- application_status: days_left >= cutoff - 15 branch ---
def test_branch_days_ge_cutoff_minus_15_true():
    assert application_status(15, False, False) == "closing"


def test_branch_days_ge_cutoff_minus_15_false():
    assert application_status(0, False, False) == "closed"
