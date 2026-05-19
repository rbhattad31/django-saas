from django.test import TestCase, SimpleTestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch, MagicMock
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from core.models import Users, Account, Receipts, RentalDeals
from Rental_Deal.views import _parse_receipts_list, _sync_receipt_statuses

class CreateDealViewTest(TestCase):
    """
    Test suite for the create_deal view in the Rental_DealViewSet.
    """

    def setUp(self):
        """
        Set up the necessary objects for testing.
        This runs before each test method.
        """
        self.client = APIClient()

        # Create a test account
        self.account = Account.objects.create(account_name='Test Account', account_domain='test.com', is_active='Y')

        # Create a user with permission to add rental deals
        self.user_with_perm = Users.objects.create_user(
            email='testuser@test.com',
            password='testpassword',
            name='Test User',
            account=self.account
        )
        content_type = ContentType.objects.get_for_model(RentalDeals)
        permission = Permission.objects.get(
            codename='add_rentaldeals',
            content_type=content_type,
        )
        self.user_with_perm.user_permissions.add(permission)
        self.user_with_perm.refresh_from_db()

        # Create a user without permission
        self.user_without_perm = Users.objects.create_user(
            email='nopermuser@test.com',
            password='testpassword',
            name='No Perm User',
            account=self.account
        )

        # Create a test receipt
        self.receipt = Receipts.objects.create(
            receipt_number=9001,
            date='2024-01-01',
            dhs='1000',
            fils='00',
            sec_date='2024-01-01',
            being='Test',
            status='Unused',
            deal_type='Rental',
            sum_of_dhs='One Thousand',
            agent_name='Test Agent',
            project_name='Test Project',
            building_name='Test Building',
            unit_number='101',
            account_id=self.account.id,
            agent_id=self.user_with_perm.id,
            cheque_no = "123456",
            bank = "gopi",
            payment_type = "Cash",
            mail_status= "sent"
        )

        # URL for the create_deal view
        self.url = reverse('rental-deal-create')

        # Base valid data for creating a deal
        self.valid_data = {
            'reference_number': 'REF12345',
            'date': '01-01-2024',
            'unit_details': 'Test Unit',
            'building_name': 'Test Building',
            'project_name': 'Test Project',
            'is_new_deal': 'N',
            'owner_first_name': 'John',
            'owner_source': 'Test Source',
            'owner_mobile': '1234567890',
            'tenant_first_name': 'Jane',
            'tenant_source': 'Test Source',
            'tenant_mobile': '0987654321',
            'deal_start_date': '01-01-2024',
            'deal_end_date': '31-12-2024',
            'seller_nationality': 'American',
            'buyer_nationality': 'British',
            'screening': 'Done',
            'owner_agency': 'Owner Agency',
            'agent_first_name': 'Agent Bob',
            'agent_phone': '5551234',
            'tenant_agency': 'Tenant Agency',
            'tenant_agent_first_name': 'Agent Alice',
            'tenant_agent_phone': '5555678',
            'total_commission': '5000',
            'less_outsude_commission': '500',
            'net_commission': '4500',
            'classic': '2250',
            'agent1': '2250',
            'receipt_no': self.receipt.id,
            'rental_kyc_number': 'KYC987',
            'agent_name1': 'Test Agent',
            'submitted_by_agent': self.user_with_perm.id,
            'property_usage':"insustry"
        }

    @patch('Rental_Deal.views.upload_file_to_full_s3_url', return_value=True)
    def test_create_complete_deal_success(self, mock_upload):
        """
        Test successful creation of a 'Complete' rental deal.
        """
        self.client.force_authenticate(user=self.user_with_perm)
        data = self.valid_data.copy()
        data['save_as'] = 'create-deal'

        # Mock file uploads
        tenancy_contract = SimpleUploadedFile("contract.pdf", b"file_content", content_type="application/pdf")
        owner_passport = SimpleUploadedFile("passport.jpg", b"file_content", content_type="image/jpeg")
        tenant_visa = SimpleUploadedFile("visa.png", b"file_content", content_type="image/png")
        cheque_copy = SimpleUploadedFile("cheque.pdf", b"file_content", content_type="application/pdf")
        title_deed_file = SimpleUploadedFile("deed.pdf", b"file_content", content_type="application/pdf")
        data['tenancy_contract[]'] = tenancy_contract
        data['owner_passport_copy[]'] = owner_passport
        data['tenant_passport_visa_copy[]'] = tenant_visa
        data['rental_deposit_cheque_copy[]'] = cheque_copy
        data['title_deed[]'] = title_deed_file

        response = self.client.post(self.url, data, format='multipart')
        print(response)
        print(response.data)

        check_create = self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(check_create)
        
         

        deal = RentalDeals.objects.filter(reference_number='REF12345').first()
        self.assertEqual(deal.reference_number, 'REF12345')
        self.assertEqual(deal.form_status, 'Complete')
        self.assertIsNotNone(deal.submitted_date)
        self.assertEqual(deal.submitted_by_user, self.user_with_perm)
        self.assertEqual(deal.account, self.account)
        self.assertTrue(deal.tenancy_contract.startswith('tenancy_contract'))

        # Check if receipt was updated
        self.receipt.refresh_from_db()
        self.assertEqual(self.receipt.status, 'Used')
        self.assertEqual(self.receipt.deal_refer_no, 'REF12345')

#     @patch('Rental_Deal.views.upload_file_to_full_s3_url', return_value=True)
#     def test_create_draft_deal_success(self, mock_upload):
#         """
#         Test successful creation of an 'Incomplete' (draft) rental deal.
#         """
#         self.client.force_authenticate(user=self.user_with_perm)
#         data = self.valid_data.copy()
#         data['save_as'] = 'save-as-draft'
#         # Remove a field that is required for 'Complete' but not for 'Draft'
#         del data['total_commission']

#         response = self.client.post(self.url, data, format='multipart')

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(RentalDeals.objects.count(), 1)

#         deal = RentalDeals.objects.first()
#         self.assertEqual(deal.form_status, 'Incomplete')
#         self.assertIsNone(deal.submitted_date) # Should not be set for drafts

#     def test_create_deal_no_permission(self):
#         """
#         Test that a user without 'add_rentaldeals' permission gets a 403 Forbidden.
#         """
#         self.client.force_authenticate(user=self.user_without_perm)
#         response = self.client.post(self.url, self.valid_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

#     def test_create_deal_unauthenticated(self):
#         """
#         Test that an unauthenticated user gets a 401 Unauthorized.
#         """
#         response = self.client.post(self.url, self.valid_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_create_deal_missing_required_field_for_complete(self):
#         """
#         Test that creating a 'Complete' deal with missing required data fails with a 400.
#         """
#         self.client.force_authenticate(user=self.user_with_perm)
#         data = self.valid_data.copy()
#         data['save_as'] = 'create-deal'
#         del data['total_commission']  # A required field for complete deals

#         response = self.client.post(self.url, data, format='json')

#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertIn('total_commission', response.data)

#     def test_create_deal_duplicate_reference_number(self):
#         """
#         Test that creating a deal with a duplicate reference number fails.
#         """
#         # Create an initial deal
#         RentalDeals.objects.create(**self.valid_data, submitted_by_user=self.user_with_perm, account=self.account)

#         self.client.force_authenticate(user=self.user_with_perm)
#         data = self.valid_data.copy()
#         data['save_as'] = 'create-deal'

#         response = self.client.post(self
# .url, data, format='json')

#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertIn('reference_number', response.data)
#         self.assertIn('already used', response.data['reference_number'][0])


class ReceiptsListHelperTests(SimpleTestCase):
    """Unit tests for receipts_list helper functions."""

    @patch("Rental_Deal.views.Receipts.objects.filter")
    def test_parse_receipts_list_accepts_json_and_removes_duplicates(self, mock_filter):
        receipt_map = {
            101: MagicMock(id=101, receipt_number=7001),
            102: MagicMock(id=102, receipt_number=7002),
        }

        def filter_side_effect(*args, **kwargs):
            receipt_id = kwargs.get("id")
            query = MagicMock()
            query.only.return_value = query
            query.first.return_value = receipt_map.get(receipt_id)
            return query

        mock_filter.side_effect = filter_side_effect

        raw_value = '[{"id": 101}, {"id": 102}, {"id": 101}, {"id": "bad"}]'
        parsed = _parse_receipts_list(raw_value)

        self.assertEqual(
            parsed,
            [
                {"id": 101, "receipt_number": 7001},
                {"id": 102, "receipt_number": 7002},
            ],
        )

    @patch("Rental_Deal.views.Receipts.objects.filter")
    def test_parse_receipts_list_supports_plain_id_array(self, mock_filter):
        receipt_map = {
            201: MagicMock(id=201, receipt_number=8001),
            202: MagicMock(id=202, receipt_number=8002),
        }

        def filter_side_effect(*args, **kwargs):
            receipt_id = kwargs.get("id")
            query = MagicMock()
            query.only.return_value = query
            query.first.return_value = receipt_map.get(receipt_id)
            return query

        mock_filter.side_effect = filter_side_effect

        parsed = _parse_receipts_list("[201, 202, 201]")

        self.assertEqual(
            parsed,
            [
                {"id": 201, "receipt_number": 8001},
                {"id": 202, "receipt_number": 8002},
            ],
        )

    def test_parse_receipts_list_returns_empty_on_invalid_json(self):
        parsed = _parse_receipts_list("not-a-json")
        self.assertEqual(parsed, [])

    @patch("Rental_Deal.views.Receipts.objects.filter")
    def test_sync_receipt_statuses_marks_removed_unused_and_current_used(self, mock_filter):
        removed_qs = MagicMock()
        added_qs = MagicMock()

        def filter_side_effect(*args, **kwargs):
            ids = set(kwargs.get("id__in", []))
            if ids == {11}:
                return removed_qs
            if ids == {12, 13}:
                return added_qs
            return MagicMock()

        mock_filter.side_effect = filter_side_effect

        previous_payload = [
            {"id": 11, "receipt_number": 5001},
            {"id": 12, "receipt_number": 5002},
        ]
        current_payload = [
            {"id": 12, "receipt_number": 5002},
            {"id": 13, "receipt_number": 5003},
        ]

        _sync_receipt_statuses(current_payload, "REF-100", previous_payload)

        removed_qs.update.assert_called_once_with(status="Unused", deal_refer_no="")
        added_qs.update.assert_called_once_with(status="Used", deal_refer_no="REF-100")

    @patch("Rental_Deal.views.Receipts.objects.filter")
    def test_sync_receipt_statuses_marks_all_current_used_when_no_previous(self, mock_filter):
        added_qs = MagicMock()

        def filter_side_effect(*args, **kwargs):
            ids = set(kwargs.get("id__in", []))
            if ids == {21, 22}:
                return added_qs
            return MagicMock()

        mock_filter.side_effect = filter_side_effect

        current_payload = [
            {"id": 21, "receipt_number": 6001},
            {"id": 22, "receipt_number": 6002},
        ]

        _sync_receipt_statuses(current_payload, "REF-200")

        added_qs.update.assert_called_once_with(status="Used", deal_refer_no="REF-200")
