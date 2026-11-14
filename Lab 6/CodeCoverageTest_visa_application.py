import pytest
from visa_application import visa_fee, documents_complete, application_status


# --- visa_fee: normal inputs ---
def test_visa_fee_within_included_entries_normal():
    assert visa_fee("tourist", 1, "normal", "B") == 0


def test_visa_fee_student_within_included():
    assert visa_fee("student", 2, "normal", "B") == 0


def test_visa_fee_business_within_included():
    assert visa_fee("business", 3, "normal", "B") == 0


# --- visa_fee: nationality_group A adds one included entry (non-student) ---
def test_visa_fee_nationality_group_a_non_student():
    # tourist included=1, +1 for group A => included=2, entries=3 => extra=1
    assert visa_fee("tourist", 3, "normal", "A") == 1 * 40


def test_visa_fee_nationality_group_a_student_no_extra():
    # student included=2, no +1 because visa_type == "student"
    assert visa_fee("student", 2, "normal", "A") == 0


# --- visa_fee: extra <= 0 returns 0 ---
def test_visa_fee_extra_zero_returns_zero():
    assert visa_fee("tourist", 1, "normal", "B") == 0


def test_visa_fee_extra_negative_returns_zero():
    assert visa_fee("business", 0, "normal", "B") == 0


# --- visa_fee: speed express vs normal rate ---
def test_visa_fee_express_rate():
    # tourist included=1, entries=6 => extra=5, express rate=100, extra<=5 no surcharge
    assert visa_fee("tourist", 6, "express", "B") == 5 * 100


def test_visa_fee_normal_rate():
    assert visa_fee("tourist", 6, "normal", "B") == 5 * 40


# --- visa_fee: extra > 5 surcharge ---
def test_visa_fee_extra_gt_five_normal():
    # tourist included=1, entries=8 => extra=7, normal rate=40+20=60
    assert visa_fee("tourist", 8, "normal", "B") == 7 * 60


def test_visa_fee_extra_gt_five_express():
    # tourist included=1, entries=8 => extra=7, express rate=100+20+10=130
    assert visa_fee("tourist", 8, "express", "B") == 7 * 130


# --- visa_fee: invalid visa type ---
def test_visa_fee_unknown_visa_type():
    with pytest.raises(ValueError, match="unknown visa type"):
        visa_fee("diplomatic", 2, "normal", "B")


# --- visa_fee: invalid entries ---
def test_visa_fee_negative_entries():
    with pytest.raises(ValueError, match="invalid entries"):
        visa_fee("tourist", -1, "normal", "B")


# --- visa_fee: empty / invalid types ---
def test_visa_fee_empty_visa_type():
    with pytest.raises(ValueError, match="unknown visa type"):
        visa_fee("", 1, "normal", "B")


# --- documents_complete: renewal path ---
def test_documents_complete_renewal_true():
    assert documents_complete(1, 0, True) is True


def test_documents_complete_renewal_false():
    assert documents_complete(0, 5, True) is False


# --- documents_complete: photos < 2 returns False ---
def test_documents_complete_photos_less_than_two_false():
    assert documents_complete(5, 1, False) is False


def test_documents_complete_photos_zero_false():
    assert documents_complete(5, 0, False) is False


# --- documents_complete: forms_filed >= 3 ---
def test_documents_complete_forms_three_true():
    assert documents_complete(3, 2, False) is True


def test_documents_complete_forms_two_false():
    assert documents_complete(2, 2, False) is False


def test_documents_complete_empty_forms_false():
    assert documents_complete(0, 2, False) is False


# --- application_status: express cutoff ---
def test_application_status_express_open():
    assert application_status(10, True, False) == "open"


def test_application_status_express_closing():
    assert application_status(5, True, False) == "closing"


def test_application_status_express_closed():
    # express cutoff=10, closing threshold = -5; days_left=-10 is closed
    assert application_status(-10, True, False) == "closed"


# --- application_status: normal cutoff ---
def test_application_status_normal_open():
    assert application_status(30, False, False) == "open"


def test_application_status_normal_closing():
    assert application_status(20, False, False) == "closing"


def test_application_status_normal_closed():
    assert application_status(0, False, False) == "closed"


# --- application_status: peak season adds 15 ---
def test_application_status_peak_season_open():
    assert application_status(45, False, True) == "open"


def test_application_status_peak_season_closing():
    assert application_status(30, False, True) == "closing"


def test_application_status_peak_season_closed():
    assert application_status(10, False, True) == "closed"


# --- application_status: express + peak season ---
def test_application_status_express_peak_open():
    # express cutoff=10 + 15 = 25
    assert application_status(25, True, True) == "open"


def test_application_status_express_peak_closed():
    assert application_status(0, True, True) == "closed"


# --- boundary values ---
def test_visa_fee_boundary_extra_one():
    assert visa_fee("tourist", 2, "normal", "B") == 1 * 40


def test_visa_fee_boundary_extra_five():
    assert visa_fee("tourist", 6, "normal", "B") == 5 * 40


def test_visa_fee_boundary_extra_six():
    assert visa_fee("tourist", 7, "normal", "B") == 6 * 60


def test_application_status_boundary_days_equals_cutoff():
    assert application_status(30, False, False) == "open"


def test_application_status_boundary_days_equals_cutoff_minus_15():
    assert application_status(15, False, False) == "closing"
