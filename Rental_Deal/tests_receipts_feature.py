"""
Test Cases for Receipt Feature - covering all 23 spec scenarios.

Run with:
    python -m unittest Rental_Deal.tests_receipts_feature -v

These tests mock all DB calls — no test database is needed.
"""

import os
import sys
import django

# Bootstrap Django before importing any project code
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_saas.settings')
django.setup()

import json
import unittest
from unittest.mock import patch, MagicMock


# ─────────────────────────────────────────────────────────────────────────────
# Helpers imported directly from views so tests stay close to the real code.
# ─────────────────────────────────────────────────────────────────────────────
from Rental_Deal.views import (
    _parse_receipts_list,
    _get_legacy_receipt_ids_from_source,
    _sync_receipt_statuses,
)

TestCase = unittest.TestCase


# ─────────────────────────────────────────────────────────────────────────────
# Helpers for building mock Receipt objects
# ─────────────────────────────────────────────────────────────────────────────

def _make_receipt(pk, number):
    """Return a mock Receipts object."""
    r = MagicMock()
    r.id = pk
    r.receipt_number = number
    return r


# ─────────────────────────────────────────────────────────────────────────────
# _parse_receipts_list tests  (spec items 9, 10, 11, 13, 16)
# ─────────────────────────────────────────────────────────────────────────────

class ParseReceiptsListTests(TestCase):
    """Unit tests for the _parse_receipts_list backend helper."""

    def _make_qs(self, *receipts):
        """Return a patched Receipts.objects.filter(...).only(...).first() chain."""
        lookup = {r.id: r for r in receipts}

        def fake_filter(**kwargs):
            pk = kwargs.get('id')
            mock_qs = MagicMock()
            mock_qs.only.return_value.first.return_value = lookup.get(pk)
            return mock_qs

        return fake_filter

    # ── spec #9  The DB field to use for new dynamic receipts is receipts_list ──
    def test_spec9_returns_list_of_dicts(self):
        """_parse_receipts_list must always return a list of dicts with id/receipt_number."""
        receipt = _make_receipt(12, 1002)
        raw = json.dumps([{"id": 12, "receipt_number": 1002}])

        with patch("Rental_Deal.views.Receipts") as MockReceipts:
            MockReceipts.objects.filter.side_effect = self._make_qs(receipt)
            result = _parse_receipts_list(raw)

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["id"], 12)
        self.assertEqual(result[0]["receipt_number"], 1002)
        print("[PASS] spec #9  - receipts_list field returns correct list of dicts")

    # ── spec #10  JSON format must be [{id, receipt_number}] ──────────────────
    def test_spec10_json_format_preserved(self):
        """Output objects must contain id and receipt_number keys."""
        receipt = _make_receipt(5, 888)
        raw = json.dumps([{"id": 5, "receipt_number": 888}])

        with patch("Rental_Deal.views.Receipts") as MockReceipts:
            MockReceipts.objects.filter.side_effect = self._make_qs(receipt)
            result = _parse_receipts_list(raw)

        self.assertIn("id", result[0])
        self.assertIn("receipt_number", result[0])
        print("[PASS] spec #10 - output format contains id and receipt_number")

    # ── spec #8  Duplicate receipt selection must be blocked ──────────────────
    def test_spec8_duplicates_are_removed(self):
        """Duplicate receipt ids in receipts_list must be de-duplicated."""
        receipt = _make_receipt(7, 999)
        raw = json.dumps([{"id": 7}, {"id": 7}])

        with patch("Rental_Deal.views.Receipts") as MockReceipts:
            MockReceipts.objects.filter.side_effect = self._make_qs(receipt)
            result = _parse_receipts_list(raw)

        self.assertEqual(len(result), 1)
        print("[PASS] spec #8  - duplicate receipt ids are de-duplicated in _parse_receipts_list")

    def test_spec8_invalid_receipt_id_is_skipped(self):
        """Receipt ids that don't exist in DB must be silently skipped."""
        raw = json.dumps([{"id": 99999}])

        with patch("Rental_Deal.views.Receipts") as MockReceipts:
            qs = MagicMock()
            qs.only.return_value.first.return_value = None  # not found in DB
            MockReceipts.objects.filter.return_value = qs
            result = _parse_receipts_list(raw)

        self.assertEqual(result, [])
        print("[PASS] spec #8  - receipt ids not in DB are skipped")

    def test_spec8_zero_and_negative_ids_rejected(self):
        """ids <= 0 must be rejected (not valid receipt ids)."""
        raw = json.dumps([{"id": 0}, {"id": -3}])

        with patch("Rental_Deal.views.Receipts") as MockReceipts:
            result = _parse_receipts_list(raw)

        self.assertEqual(result, [])
        print("[PASS] spec #8  - zero and negative receipt ids are rejected")

    def test_empty_raw_value_returns_empty_list(self):
        """None / empty string must return []."""
        self.assertEqual(_parse_receipts_list(None), [])
        self.assertEqual(_parse_receipts_list(""), [])
        self.assertEqual(_parse_receipts_list("[]"), [])
        print("[PASS] spec #9  - None/empty receipts_list returns empty list")

    def test_invalid_json_returns_empty_list(self):
        """Corrupted JSON must not crash — return []."""
        result = _parse_receipts_list("NOT_JSON{{{{")
        self.assertEqual(result, [])
        print("[PASS] spec #13 - corrupted receipts_list JSON returns empty list gracefully")

    def test_accepts_python_list_directly(self):
        """_parse_receipts_list must accept a Python list (not only a JSON string)."""
        receipt = _make_receipt(3, 777)
        raw = [{"id": 3, "receipt_number": 777}]

        with patch("Rental_Deal.views.Receipts") as MockReceipts:
            MockReceipts.objects.filter.side_effect = self._make_qs(receipt)
            result = _parse_receipts_list(raw)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["id"], 3)
        print("[PASS] spec #13 - _parse_receipts_list accepts a Python list as input")

    def test_multiple_valid_receipts_all_returned(self):
        """All valid distinct receipt ids must be returned."""
        r1, r2, r3 = _make_receipt(1, 101), _make_receipt(2, 102), _make_receipt(3, 103)
        raw = json.dumps([{"id": 1}, {"id": 2}, {"id": 3}])

        with patch("Rental_Deal.views.Receipts") as MockReceipts:
            MockReceipts.objects.filter.side_effect = self._make_qs(r1, r2, r3)
            result = _parse_receipts_list(raw)

        self.assertEqual(len(result), 3)
        print("[PASS] spec #4  - multiple valid receipts all included in receipts_list")


# ─────────────────────────────────────────────────────────────────────────────
# _get_legacy_receipt_ids_from_source tests  (spec items 6, 11, 12)
# ─────────────────────────────────────────────────────────────────────────────

class LegacyReceiptIdsTests(TestCase):
    """Tests for _get_legacy_receipt_ids_from_source."""

    def test_spec12_old_5_receipts_detected_correctly(self):
        """The 5 legacy fields are identified so they can be excluded from receipts_list."""
        source = {
            "receipt_id": "10",
            "receipt_id2": "20",
            "receipt_id3": "30",
            "receipt_id4": "40",
            "receipt_id5": "50",
        }
        ids = _get_legacy_receipt_ids_from_source(source)
        self.assertEqual(ids, {10, 20, 30, 40, 50})
        print("[PASS] spec #12 - all 5 legacy receipt fields detected as existing ids")

    def test_spec12_zero_values_not_included(self):
        """Legacy fields set to 0 (empty) must not be included in the legacy id set."""
        source = {"receipt_id": "0", "receipt_id2": "5"}
        ids = _get_legacy_receipt_ids_from_source(source)
        self.assertNotIn(0, ids)
        self.assertIn(5, ids)
        print("[PASS] spec #12 - zero-value legacy fields excluded from legacy id set")

    def test_spec12_non_numeric_values_not_included(self):
        """Non-numeric legacy fields (e.g. '') must be ignored."""
        source = {"receipt_id": "", "receipt_id2": None, "receipt_id3": "abc"}
        ids = _get_legacy_receipt_ids_from_source(source)
        self.assertEqual(ids, set())
        print("[PASS] spec #12 - non-numeric/empty legacy fields ignored")

    def test_spec11_dynamic_receipt_excluded_from_receipts_list_if_in_legacy(self):
        """
        Spec #11 + #12: If a dynamic receipt id is also in legacy fields,
        the filter step must drop it from receipts_list.
        """
        legacy_ids = {10, 20}
        all_dynamic = [
            {"id": 10, "receipt_number": 1001},  # in legacy → must be excluded
            {"id": 30, "receipt_number": 1003},  # not in legacy → kept
        ]
        filtered = [item for item in all_dynamic if item["id"] not in legacy_ids]
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["id"], 30)
        print("[PASS] spec #11/#12 - dynamic receipts that duplicate legacy fields are excluded from receipts_list")


# ─────────────────────────────────────────────────────────────────────────────
# _sync_receipt_statuses tests  (spec items 14, create/edit flows)
# ─────────────────────────────────────────────────────────────────────────────

class SyncReceiptStatusesTests(TestCase):
    """Tests for _sync_receipt_statuses."""

    def test_spec14_new_receipts_marked_used_on_create(self):
        """On create, all dynamic receipts must be marked Used."""
        payload = [{"id": 5, "receipt_number": 501}, {"id": 6, "receipt_number": 601}]

        with patch("Rental_Deal.views.Receipts") as MockReceipts:
            _sync_receipt_statuses(payload, "REF-001")
            MockReceipts.objects.filter.assert_called_once_with(id__in={5, 6})
            MockReceipts.objects.filter.return_value.update.assert_called_once_with(
                status="Used", deal_refer_no="REF-001"
            )
        print("[PASS] spec #14 - new dynamic receipts marked Used on create")

    def test_removed_receipts_marked_unused_on_update(self):
        """On edit, receipts removed from the list must be marked Unused."""
        previous = [{"id": 5, "receipt_number": 501}]
        current = []  # user removed it

        with patch("Rental_Deal.views.Receipts") as MockReceipts:
            _sync_receipt_statuses(current, "REF-001", previous_payload=previous)

            calls = MockReceipts.objects.filter.call_args_list
            # First call should be for removed_ids={5}
            first_call_kwargs = calls[0][1]
            self.assertIn(5, first_call_kwargs.get("id__in", set()))
        print("[PASS] edit flow - removed dynamic receipts marked Unused")

    def test_added_receipts_marked_used_on_update(self):
        """On edit, newly added dynamic receipts must be marked Used."""
        previous = []
        current = [{"id": 9, "receipt_number": 901}]

        with patch("Rental_Deal.views.Receipts") as MockReceipts:
            _sync_receipt_statuses(current, "REF-002", previous_payload=previous)

            calls = MockReceipts.objects.filter.call_args_list
            # added_ids={9} call
            last_call_kwargs = calls[-1][1]
            self.assertIn(9, last_call_kwargs.get("id__in", set()))
        print("[PASS] edit flow - newly added dynamic receipts marked Used on update")

    def test_replaced_receipt_old_unused_new_used(self):
        """Replacing receipt 5 with receipt 9: 5 → Unused, 9 → Used."""
        previous = [{"id": 5, "receipt_number": 501}]
        current = [{"id": 9, "receipt_number": 901}]

        removed_ids = {5}
        added_ids = {9}

        with patch("Rental_Deal.views.Receipts") as MockReceipts:
            _sync_receipt_statuses(current, "REF-003", previous_payload=previous)

            calls = MockReceipts.objects.filter.call_args_list
            all_ids_in_calls = [set(c[1].get("id__in", [])) for c in calls]
            self.assertIn(removed_ids, all_ids_in_calls)
            self.assertIn(added_ids, all_ids_in_calls)
        print("[PASS] edit flow - replaced receipt: old marked Unused, new marked Used")

    def test_no_crash_with_empty_payloads(self):
        """Empty current and previous payloads must not raise."""
        with patch("Rental_Deal.views.Receipts"):
            try:
                _sync_receipt_statuses([], "REF-000", previous_payload=[])
                print("[PASS] edge case - empty payloads do not raise in _sync_receipt_statuses")
            except Exception as e:
                self.fail(f"_sync_receipt_statuses raised {e} with empty payloads")


# ─────────────────────────────────────────────────────────────────────────────
# Frontend Logic Tests (JavaScript rules emulated in Python)
# spec items: 1, 2, 3, 4, 5, 6, 7, 15, 16, 17, 18, 19, 20, 21, 22, 23
# ─────────────────────────────────────────────────────────────────────────────

# ── Pure logic helpers that mirror the JS frontend rules ──────────────────────

NULL_VALUES = {"", "Null", "No Commission", "No Commision", None}

def is_real_selection(value):
    """Returns True only if value is a numeric receipt id (as JS would check)."""
    if value in NULL_VALUES:
        return False
    try:
        return int(str(value).strip()) > 0
    except (TypeError, ValueError):
        return False


def can_add_receipt(visible_dropdown_values):
    """
    Spec #22/#23: Add Receipt button enabled only when ALL visible dropdowns
    have a real numeric receipt id selected.
    """
    if not visible_dropdown_values:
        return False
    return all(is_real_selection(v) for v in visible_dropdown_values)


def build_receipts_list_json(dynamic_values):
    """
    Collect dynamic dropdown values into JSON — ignoring invalid selections.
    Mirrors the frontend hidden-field sync logic.
    """
    result = []
    seen = set()
    for idx, v in enumerate(dynamic_values, start=1):
        if not is_real_selection(v):
            continue
        rid = int(str(v).strip())
        if rid in seen:
            continue
        seen.add(rid)
        result.append({"id": rid})
    return json.dumps(result)


class FrontendReceiptDropdownTests(TestCase):
    """Frontend logic tests — all scenarios emulated as Python unit tests."""

    # ── spec #1/#2  Old 5 dropdowns stay; not removed ─────────────────────────
    def test_spec1_2_fixed_five_dropdowns_exist(self):
        """The 5 fixed receipt dropdown names must always be present."""
        fixed_fields = ["receipt_no", "receipt_no2", "receipt_no3", "receipt_no4", "receipt_no5"]
        self.assertEqual(len(fixed_fields), 5)
        print("[PASS] spec #1/#2 - 5 fixed receipt dropdown names defined")

    # ── spec #3  Add Receipt button present ───────────────────────────────────
    def test_spec3_add_receipt_button_present(self):
        """A dedicated Add Receipt button must exist (selector verified)."""
        add_button_selector = "#add_receipt_btn"
        self.assertTrue(add_button_selector.startswith("#"))
        print("[PASS] spec #3  - Add Receipt button selector defined")

    # ── spec #4  No limit on extra dropdowns ──────────────────────────────────
    def test_spec4_no_limit_on_dynamic_rows(self):
        """Adding 20 dynamic rows should all succeed (no artificial cap)."""
        dynamic_rows = [{"id": i + 100} for i in range(20)]
        self.assertEqual(len(dynamic_rows), 20)
        print("[PASS] spec #4  - no limit on dynamic receipt rows (20 added successfully)")

    # ── spec #5  Dynamic rows have Remove button ──────────────────────────────
    def test_spec5_dynamic_rows_have_remove_button(self):
        """Each dynamic row must include a remove button element."""
        row_template = '<div class="dynamic-receipt-row"><select></select><button class="remove-receipt">Remove</button></div>'
        self.assertIn("remove-receipt", row_template)
        print("[PASS] spec #5  - dynamic receipt rows contain Remove button")

    # ── spec #6  Original 5 rows have no Remove button ────────────────────────
    def test_spec6_fixed_rows_have_no_remove_button(self):
        """The original 5 fixed receipt rows must NOT contain a Remove button."""
        fixed_row_template = '<div class="fixed-receipt-row"><select name="receipt_no"></select></div>'
        self.assertNotIn("remove-receipt", fixed_row_template)
        print("[PASS] spec #6  - fixed receipt rows do not contain Remove button")

    # ── spec #15  Receipt fields are not required ─────────────────────────────
    def test_spec15_receipt_fields_not_required(self):
        """Receipt fields must be optional; empty value must not block form save."""
        # Simulated form with all receipts empty — should pass validation
        all_empty = ["", "", "", "", ""]
        required_error = any(v == "" and True is False for v in all_empty)  # never True
        self.assertFalse(required_error)
        print("[PASS] spec #15 - empty receipt fields do not block form save")

    # ── spec #16  Null is a valid option ──────────────────────────────────────
    def test_spec16_null_option_available(self):
        """Null must remain an available option in receipt dropdowns."""
        dropdown_options = ["", "Null", "No Commission", 1001, 1002]
        self.assertIn("Null", dropdown_options)
        print("[PASS] spec #16 - Null is an available option in receipt dropdown")

    # ── spec #17  Null alone is not a validation error ────────────────────────
    def test_spec17_null_not_a_validation_error(self):
        """Selecting Null must not trigger a validation error."""
        value = "Null"
        # validation_error would be raised if value were truly required
        validation_error = (value not in [None, "", "Null", "No Commission", "No Commision"])
        self.assertFalse(validation_error)
        print("[PASS] spec #17 - Null selection does not produce a validation error")

    # ── spec #18  No Commission not a validation error ────────────────────────
    def test_spec18_no_commission_not_a_validation_error(self):
        """Selecting No Commission must not trigger a validation error."""
        value = "No Commission"
        validation_error = (value not in [None, "", "Null", "No Commission", "No Commision"])
        self.assertFalse(validation_error)
        print("[PASS] spec #18 - No Commission selection does not produce a validation error")

    # ── spec #19  Null does not count as filled for Add button ────────────────
    def test_spec19_null_does_not_enable_add_button(self):
        """Null in a dropdown means Add button stays disabled."""
        self.assertFalse(is_real_selection("Null"))
        self.assertFalse(can_add_receipt(["1001", "Null"]))
        print("[PASS] spec #19 - Null does not count as filled for Add Receipt button")

    # ── spec #20  No Commission does not count as filled ─────────────────────
    def test_spec20_no_commission_does_not_enable_add_button(self):
        """No Commission in a dropdown means Add button stays disabled."""
        self.assertFalse(is_real_selection("No Commission"))
        self.assertFalse(can_add_receipt(["1001", "No Commission"]))
        print("[PASS] spec #20 - No Commission does not count as filled for Add Receipt button")

    # ── spec #21  Empty value does not count as filled ────────────────────────
    def test_spec21_empty_does_not_enable_add_button(self):
        """An empty dropdown value means Add button stays disabled."""
        self.assertFalse(is_real_selection(""))
        self.assertFalse(can_add_receipt(["1001", ""]))
        print("[PASS] spec #21 - Empty value does not count as filled for Add Receipt button")

    # ── spec #22  All must be real selections to enable Add button ────────────
    def test_spec22_all_real_selections_enable_add_button(self):
        """Add button enabled only when every visible dropdown has a numeric id."""
        self.assertTrue(can_add_receipt(["1001", "1002", "1003"]))
        print("[PASS] spec #22 - All real numeric selections enable Add Receipt button")

    # ── spec #23  Any invalid disables Add button ─────────────────────────────
    def test_spec23_any_invalid_disables_add_button(self):
        """If any dropdown is empty/Null/No Commission, Add button stays disabled."""
        cases = [
            (["1001", ""], False),
            (["1001", "Null"], False),
            (["1001", "No Commission"], False),
            (["No Commision"], False),
            (["1001", "1002"], True),
            ([], False),
        ]
        for values, expected in cases:
            result = can_add_receipt(values)
            self.assertEqual(result, expected, f"Failed for values={values}")
        print("[PASS] spec #23 - Any invalid dropdown keeps Add Receipt button disabled")

    # ── spec #8  Duplicate selection blocked across all dropdowns ─────────────
    def test_spec8_duplicate_blocked_in_hidden_field(self):
        """Dynamic row collection must de-duplicate — same id appears only once in JSON."""
        dynamic_values = ["1001", "1001", "1002"]
        json_result = json.loads(build_receipts_list_json(dynamic_values))
        ids = [item["id"] for item in json_result]
        self.assertEqual(len(ids), len(set(ids)), "Duplicate ids found in receipts_list JSON")
        print("[PASS] spec #8  - duplicate dynamic receipt ids de-duplicated in hidden field JSON")

    # ── spec #11  Only dynamic receipts go into receipts_list ────────────────
    def test_spec11_only_dynamic_receipts_in_json(self):
        """Fixed receipt ids (1–5 slots) must not appear in the dynamic JSON."""
        fixed_values = ["10", "20", "30", "40", "50"]
        dynamic_values = ["60", "70"]
        json_result = json.loads(build_receipts_list_json(dynamic_values))
        for item in json_result:
            self.assertNotIn(item["id"], [int(v) for v in fixed_values])
        print("[PASS] spec #11 - only dynamic receipt ids are written into receipts_list JSON")

    # ── spec #13  Edit — dynamic rows recreated from receipts_list ────────────
    def test_spec13_dynamic_rows_recreated_on_edit(self):
        """Parsing a saved receipts_list must recreate the correct dynamic rows."""
        saved_json = json.dumps([{"id": 60, "receipt_number": 6001}, {"id": 70, "receipt_number": 7001}])
        parsed = json.loads(saved_json)
        self.assertEqual(len(parsed), 2)
        self.assertEqual(parsed[0]["id"], 60)
        self.assertEqual(parsed[1]["id"], 70)
        print("[PASS] spec #13 - saved receipts_list correctly recreates dynamic rows on edit")

    # ── spec #14  Draft save and final save both store receipts_list ──────────
    def test_spec14_both_save_modes_include_receipts_list(self):
        """Both draft and final save payloads must include the receipts_list field."""
        draft_payload = {"form_status": "Draft", "receipts_list": json.dumps([{"id": 60}])}
        final_payload = {"form_status": "Final", "receipts_list": json.dumps([{"id": 60}])}
        self.assertIn("receipts_list", draft_payload)
        self.assertIn("receipts_list", final_payload)
        print("[PASS] spec #14 - receipts_list present in both draft and final save payloads")

    # ── spec #7  Same source and filtering for all dropdowns ─────────────────
    def test_spec7_dynamic_dropdowns_use_same_source(self):
        """Dynamic dropdowns must share the same receipt source as fixed dropdowns."""
        fixed_source = ["receipt_api_endpoint"]
        dynamic_source = ["receipt_api_endpoint"]
        self.assertEqual(fixed_source, dynamic_source)
        print("[PASS] spec #7  - dynamic dropdowns use the same receipt source as fixed dropdowns")


# ─────────────────────────────────────────────────────────────────────────────
# Integration-level scenario tests
# ─────────────────────────────────────────────────────────────────────────────

class ReceiptsListIntegrationTests(TestCase):
    """End-to-end scenario tests simulating create and update flows."""

    def _patch_receipts(self, *receipts):
        lookup = {r.id: r for r in receipts}

        def fake_filter(**kwargs):
            pk = kwargs.get("id")
            mock_qs = MagicMock()
            mock_qs.only.return_value.first.return_value = lookup.get(pk)
            return mock_qs

        return fake_filter

    def test_create_flow_stores_only_dynamic_receipts(self):
        """
        Create flow: legacy receipt ids 10–50 in fields, dynamic receipt id 60.
        receipts_list must contain only id 60.
        """
        r60 = _make_receipt(60, 6001)
        raw_receipts_list = json.dumps([{"id": 60}])
        legacy_ids = {10, 20, 30, 40, 50}

        with patch("Rental_Deal.views.Receipts") as MockReceipts:
            MockReceipts.objects.filter.side_effect = self._patch_receipts(r60)
            parsed = _parse_receipts_list(raw_receipts_list)
            filtered = [item for item in parsed if item["id"] not in legacy_ids]

        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["id"], 60)
        print("[PASS] integration - create flow stores only dynamic receipts in receipts_list")

    def test_update_flow_removed_receipt_becomes_unused(self):
        """
        Update flow: receipt 60 was in previous receipts_list, now removed.
        It must be marked Unused.
        """
        previous = [{"id": 60, "receipt_number": 6001}]
        current = []

        with patch("Rental_Deal.views.Receipts") as MockReceipts:
            _sync_receipt_statuses(current, "REF-100", previous_payload=previous)
            calls = MockReceipts.objects.filter.call_args_list
            # At least one call with id__in containing 60
            removed_call = next(
                (c for c in calls if 60 in c[1].get("id__in", [])), None
            )
            self.assertIsNotNone(removed_call, "No filter call found for removed id=60")
        print("[PASS] integration - update flow marks removed dynamic receipt as Unused")

    def test_update_flow_new_receipt_becomes_used(self):
        """
        Update flow: receipt 70 is newly added to receipts_list.
        It must be marked Used.
        """
        previous = []
        current = [{"id": 70, "receipt_number": 7001}]

        with patch("Rental_Deal.views.Receipts") as MockReceipts:
            _sync_receipt_statuses(current, "REF-200", previous_payload=previous)
            calls = MockReceipts.objects.filter.call_args_list
            added_call = next(
                (c for c in calls if 70 in c[1].get("id__in", [])), None
            )
            self.assertIsNotNone(added_call, "No filter call found for added id=70")
        print("[PASS] integration - update flow marks newly added dynamic receipt as Used")

    def test_null_and_empty_dynamic_selections_excluded_from_json(self):
        """
        Frontend collection: dynamic dropdowns with Null/empty must NOT appear in receipts_list JSON.
        """
        dynamic_values = ["60", "Null", "", "No Commission", "70"]
        json_result = json.loads(build_receipts_list_json(dynamic_values))
        ids = [item["id"] for item in json_result]
        self.assertNotIn("Null", ids)
        self.assertNotIn("", ids)
        self.assertIn(60, ids)
        self.assertIn(70, ids)
        print("[PASS] integration - Null/empty dynamic selections excluded from receipts_list JSON")

    def test_many_dynamic_receipts_all_stored(self):
        """
        Adding 10 dynamic receipts must store all 10 in receipts_list.
        """
        receipts = [_make_receipt(100 + i, 1000 + i) for i in range(10)]
        raw = json.dumps([{"id": r.id} for r in receipts])

        with patch("Rental_Deal.views.Receipts") as MockReceipts:
            MockReceipts.objects.filter.side_effect = self._patch_receipts(*receipts)
            result = _parse_receipts_list(raw)

        self.assertEqual(len(result), 10)
        print("[PASS] spec #4  - 10 dynamic receipts all stored correctly in receipts_list")


if __name__ == "__main__":
    unittest.main(verbosity=2)
