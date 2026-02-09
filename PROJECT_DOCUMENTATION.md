# Django SaaS - Real Estate Deal Management System

## 1. Project Overview

**Project Name:** Django SaaS - Real Estate Deal Management Platform

**What This Project Is About:**  
A comprehensive multi-tenant SaaS platform designed for real estate agencies to manage rental deals, sales transactions, property management, receipts, and third-party deposits. The system provides role-based workflows (Admin, Manager, Agent, Finance) with approval processes, commission tracking, document management via AWS S3, and automated compliance checks including AML screening and KYC verification.

---

## 2. Tech Stack

### Programming Languages
- **Python 3.x** - Primary backend language

### Frameworks & Libraries
| Framework/Library | Version | Purpose |
|-------------------|---------|---------|
| Django | 5.2+ | Web framework |
| Django REST Framework | 3.14+ | REST API development |
| django-filter | 24.1 | Query filtering |
| django-multitenant | Latest | Multi-tenancy support |
| django-storages | Latest | Cloud storage backend |
| django-crontab | Latest | Scheduled tasks |

### Database
- **MySQL** - Primary relational database

### Cloud & Storage
- **AWS S3** - Document and media file storage
- **boto3** - AWS Python SDK

### Additional Tools
- **WeasyPrint** - PDF generation for receipts and contracts
- **python-dotenv** - Environment configuration management
- **bcrypt** - Password hashing
- **mysqlclient** - MySQL database adapter

---

## 3. Project Structure

```
bradsol/
├── core/                              # Core application - users, accounts, authentication
│   ├── models.py                      # User, Account, Properties, Receipts models
│   ├── views.py                       # Core views and dashboard
│   ├── urls.py                        # Core URL routing
│   ├── authentication_backend.py      # Custom authentication logic
│   ├── permissions.py                 # Permission definitions
│   └── middleware.py                  # Custom middleware
│
├── Rental_Deal/                       # Rental deal management
│   ├── models.py                      # Rental deal models
│   ├── views.py                       # Rental deal CRUD operations
│   ├── urls.py                        # Rental deal routing
│   ├── serializers.py                 # API serializers
│   ├── permissions.py                 # Deal-specific permissions
│   └── templates/                     # Rental deal templates
│
├── Sales_Deals_Management/            # Sales deal management
│   ├── models.py                      # Sales deal models
│   ├── views.py                       # Sales deal operations
│   ├── urls.py                        # Sales deal routing
│   ├── serializers.py                 # API serializers
│   └── templates/                     # Sales deal templates
│
├── property_management_deals/         # Property management
│   ├── models.py                      # Property models
│   ├── views.py                       # Property CRUD operations
│   ├── urls.py                        # Property routing
│   ├── forms.py                       # Property forms
│   └── templates/                     # Property templates
│
├── Third_Party_Receipts/              # Third-party receipt management
│   ├── models.py                      # Deposit models
│   ├── views.py                       # Receipt operations
│   └── urls.py                        # Receipt routing
│
├── accounts_management/               # User and account management
│   ├── models.py                      # Account-related models
│   ├── views.py                       # Account management views
│   ├── serializers.py                 # Account serializers
│   └── permissions.py                 # Account permissions
│
├── rolemanagement/                    # Role and permission management
│   ├── models.py                      # Role models
│   ├── views.py                       # Role management views
│   └── permissionsofrole.py          # Role permission mappings
│
├── reports_management/                # Reporting module
│   ├── views.py                       # Report generation views
│   ├── urls.py                        # Report routing
│   ├── serializers.py                 # Report serializers
│   ├── permissions.py                 # Report permissions
│   └── templates/                     # Report templates
│
├── django_saas/                       # Project configuration
│   ├── settings.py                    # Django settings
│   ├── urls.py                        # Main URL configuration
│   ├── wsgi.py                        # WSGI configuration
│   └── asgi.py                        # ASGI configuration
│
├── templates/                         # Global templates
│   ├── layouts/                       # Base layout templates
│   ├── includes/                      # Reusable template components
│   └── accounts/                      # Account-related templates
│
├── static/                            # Static files (CSS, JS, images)
│   └── assets/                        # Project assets
│
├── staticfiles/                       # Collected static files
├── logs/                              # Application logs
├── reports/                           # Generated reports
├── requirements.txt                   # Python dependencies
├── manage.py                          # Django management script
└── db.sqlite3                         # SQLite database (dev/backup)
```

### Folder Descriptions

- **core/** - Central application containing user authentication, account management, base models (Users, Account, Properties, Receipts), and shared functionality
- **Rental_Deal/** - Complete rental deal lifecycle management including creation, approval workflows, finance processing
- **Sales_Deals_Management/** - Sales transaction management with approval workflows and financial tracking
- **property_management_deals/** - Property listing and management receipt generation
- **Third_Party_Receipts/** - Third-party deposit and receipt management
- **accounts_management/** - Multi-tenant account administration
- **rolemanagement/** - Role-based access control (RBAC) system
- **reports_management/** - Commission reports and analytics (agent commission report, agent performance report)
- **django_saas/** - Project-level configuration and settings
- **templates/** - HTML templates for the frontend
- **static/** - Static assets (CSS, JavaScript, images)
- **logs/** - Application and module-specific log files
- **reports/** - Generated report files and missing file logs

---

## Setup & Run Instructions

### Prerequisites

- Python 3.8 or higher
- MySQL Server 5.7+
- pip (Python package manager)
- AWS Account (for S3 storage)
- Git

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd bradsol
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   
   Create a `.env` file in the project root with the following variables:
   
   ```env
   # Database Configuration
   DATABASE_NAME=your_database_name
   DATABASE_USER=your_database_user
   DATABASE_PASSWORD=your_database_password
   DATABASE_HOST=your_database_host
   DATABASE_PORT=3306
   
   # AWS S3 Configuration
   AWS_ACCESS_KEY_ID=your_aws_access_key
   AWS_SECRET_ACCESS_KEY=your_aws_secret_key
   AWS_BUCKET=your_bucket_name
   AWS_DEFAULT_REGION=ap-southeast-1
   MEDIA_LOCATION=media
   ```

5. **Set up the database**
   ```bash
   # Create MySQL database
   mysql -u root -p
   CREATE DATABASE your_database_name;
   EXIT;
   
   # Run migrations
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

8. **Configure cron jobs** (Optional)
   ```bash
   python manage.py crontab add
   ```

### How to Run the Project Locally

**Development Server:**
```bash
python manage.py runserver
```

Access the application at: `http://127.0.0.1:8000/`

**Run on specific port:**
```bash
python manage.py runserver 0.0.0.0:8080
```

**Run scheduled tasks manually:**
```bash
python manage.py check_rental_in_S3 --days 2
python manage.py check_sale_in_S3 --days 2
```

---

## 4. Database / Schema Details

### Database Type
**MySQL** - Relational Database Management System

### Tables Overview

| Table Name | Description | Primary Key |
|------------|-------------|-------------|
| accounts | Multi-tenant organization/account data | id (BigAutoField) |
| users | User authentication and profile data | id (AutoField) |
| auth_group | Django groups for RBAC | id |
| core_groupprofile | Links groups to specific accounts | id |
| rental_deals | Rental transaction management | id |
| sales_deals | Sales transaction management | id (AutoField) |
| rental_properties | Property management deals | id (BigAutoField) |
| properties | Property master data | id (BigAutoField) |
| receipts | Third-party commission receipts | id (BigAutoField) |
| management_receipts | Property management fee receipts | id (BigAutoField) |
| deposits | Third-party deposit transactions | id (AutoField) |
| auth_permission | Django permission system | id |
| auth_user_groups | User-group relationships | id |
| auth_user_user_permissions | User-specific permissions | id |
| django_migrations | Migration tracking | id |
| django_session | Session data | session_key |

---

### Table: `accounts`

**Purpose:** Stores multi-tenant account/organization information

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| id | BigAutoField | PRIMARY KEY | Unique account identifier |
| account_name | VARCHAR(191) | UNIQUE, NOT NULL | Account/company name |
| account_domain | VARCHAR(191) | UNIQUE, NOT NULL | Subdomain for tenant |
| contact_name | VARCHAR(191) | NULL | Primary contact name |
| contact_email | VARCHAR(191) | NULL | Contact email address |
| contact_phone | VARCHAR(191) | NULL | Contact phone number |
| additional_info | TEXT | NULL | Extra account details |
| logo | TEXT | NULL | Logo file path/URL |
| plan | VARCHAR(191) | NULL | Subscription plan |
| max_users | VARCHAR(191) | NULL | Maximum users allowed |
| min_users | VARCHAR(191) | NULL | Minimum users required |
| is_active | CHAR(1) | DEFAULT 'N' | Y/N/A/R status |
| is_deleted | CHAR(1) | DEFAULT 'N' | Soft delete flag |
| created_at | DATETIME | NULL | Creation timestamp |
| updated_at | DATETIME | NULL | Last update timestamp |
| created_by | VARCHAR(191) | NULL | Creator user ID |
| updated_by | VARCHAR(191) | NULL | Last updater ID |
| is_approved | CHAR(1) | DEFAULT 'N' | Approval status |

---

### Table: `users`

**Purpose:** Custom user model for authentication and profile

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| id | AutoField | PRIMARY KEY | Unique user identifier |
| name | VARCHAR(191) | NULL | User full name |
| mobile_number | VARCHAR(191) | NOT NULL | Contact number |
| email | VARCHAR(191) | UNIQUE, NOT NULL | Login email |
| password | VARCHAR(191) | NOT NULL | Hashed password |
| gender | VARCHAR(6) | NULL | Male/Female |
| dob | DATE | NULL | Date of birth |
| additional_info | TEXT | NULL | Additional details |
| timezone | VARCHAR(191) | NULL | User timezone |
| is_active | BOOLEAN | DEFAULT 1 | Active status |
| is_deleted | CHAR(1) | NOT NULL | Soft delete Y/N |
| remember_token | VARCHAR(100) | NULL | Session token |
| last_login | DATETIME | NULL | Last login time |
| created_at | DATETIME | NULL | Account creation |
| updated_at | DATETIME | NULL | Last profile update |
| created_by | VARCHAR(191) | NULL | Creator ID |
| updated_by | VARCHAR(191) | NULL | Updater ID |
| image | TEXT | NULL | Profile image path |
| is_staff | BOOLEAN | DEFAULT 0 | Staff access flag |
| is_superuser | BOOLEAN | DEFAULT 0 | Admin flag |
| account_id | BIGINT | FOREIGN KEY | FK → accounts(id) |

**Foreign Keys:**
- `account_id` → `accounts.id` (CASCADE)

---

### Table: `core_groupprofile`

**Purpose:** Links Django groups to specific accounts for multi-tenancy

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| id | AutoField | PRIMARY KEY | Profile ID |
| group_id | INT | FOREIGN KEY, UNIQUE | FK → auth_group(id) |
| account_id | BIGINT | FOREIGN KEY | FK → accounts(id) |
| is_active | BOOLEAN | DEFAULT 1 | Active status |
| description | TEXT | NULL | Group description |

**Foreign Keys:**
- `group_id` → `auth_group.id` (CASCADE)
- `account_id` → `accounts.id` (CASCADE, DEFAULT 2)

---

### Table: `rental_deals`

**Purpose:** Manages rental transaction deals with approval workflow

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| id | AutoField | PRIMARY KEY | Deal ID |
| submitted_date | DATE | NULL | Submission date |
| submitted_by_user_id | INT | FOREIGN KEY | FK → users(id) |
| reference_number | VARCHAR(191) | UNIQUE | Deal reference |
| date | DATE | NOT NULL | Deal date |
| unit_details | TEXT | NOT NULL | Unit/apartment info |
| building_name | TEXT | NOT NULL | Building name |
| project_name | TEXT | NOT NULL | Project/development |
| is_new_deal | CHAR(1) | DEFAULT 'N' | R=Renewal, N=New |
| owner_title | TEXT | NULL | Owner title (Mr/Mrs) |
| owner_first_name | TEXT | NOT NULL | Owner first name |
| owner_last_name | TEXT | NULL | Owner last name |
| owner_source | TEXT | NOT NULL | Owner source |
| owner_mobile | TEXT | NOT NULL | Owner phone |
| owner_email | TEXT | NULL | Owner email |
| tenant_title | TEXT | DEFAULT 'N/A' | Tenant title |
| tenant_first_name | TEXT | NOT NULL | Tenant first name |
| tenant_last_name | TEXT | NULL | Tenant last name |
| tenant_source | TEXT | NOT NULL | Tenant source |
| tenant_mobile | TEXT | NOT NULL | Tenant phone |
| tenant_email | TEXT | NULL | Tenant email |
| owner_agency | TEXT | NOT NULL | Owner's agency |
| agent_first_name | TEXT | NOT NULL | Agent first name |
| agent_last_name | TEXT | NULL | Agent last name |
| agent_phone | TEXT | NOT NULL | Agent phone |
| agent_email | TEXT | NULL | Agent email |
| brn | TEXT | NULL | Agency BRN number |
| tenant_agency | TEXT | NOT NULL | Tenant's agency |
| tenant_agent_first_name | TEXT | NOT NULL | Tenant agent name |
| tenant_agent_last_name | TEXT | NULL | Tenant agent surname |
| tenant_agent_phone | TEXT | NOT NULL | Tenant agent phone |
| tenant_agent_email | TEXT | NULL | Tenant agent email |
| tenant_brn | TEXT | NULL | Tenant agency BRN |
| tenancy_contract | TEXT | NOT NULL | Contract file path |
| owner_passport_copy | TEXT | NOT NULL | Owner passport file |
| tenant_passport_visa_copy | TEXT | NOT NULL | Tenant docs file |
| tenant_emirates_id | TEXT | NULL | Emirates ID file |
| rental_deposit_cheque_copy | TEXT | NOT NULL | Deposit cheque file |
| title_deed | TEXT | NOT NULL | Title deed file |
| owner_poa_pp_copy | TEXT | NULL | POA passport copy |
| key_hand_over_form | TEXT | NULL | Key handover file |
| total_commission | TEXT | NOT NULL | Total commission |
| less_outsude_commission | TEXT | NOT NULL | Outside commission |
| net_commission | TEXT | NOT NULL | Net commission |
| classic | TEXT | NOT NULL | Classic share |
| agent1 | TEXT | NOT NULL | Agent 1 share |
| agent2 | TEXT | NULL | Agent 2 share |
| agent3 | TEXT | NULL | Agent 3 share |
| is_approved_rejected | CHAR(1) | DEFAULT 'P' | P/F/A/R status |
| approved_rejected_by | TEXT | NULL | Approver user ID |
| is_entered_in_finance_system | CHAR(1) | DEFAULT '0' | Finance entry 0/1 |
| comments | TEXT | NULL | Admin comments |
| rental_price | TEXT | NULL | Rental amount |
| ejari | TEXT | NULL | Ejari file |
| agent_name1 | TEXT | NULL | Agent 1 name |
| agent_name2 | TEXT | NULL | Agent 2 name |
| agent_name3 | TEXT | NULL | Agent 3 name |
| owner_eid_copy | TEXT | NULL | Owner EID file |
| agent_comment | TEXT | NULL | Agent comments |
| mediating_agency | TEXT | NULL | Mediator agency |
| mediating_agent_name | TEXT | NULL | Mediator name |
| mediating_agent_phone | TEXT | NULL | Mediator phone |
| mediating_agent_email | TEXT | NULL | Mediator email |
| mediating_agency_brn | TEXT | NULL | Mediator BRN |
| poa_copy | TEXT | NULL | POA copy file |
| deal_start_date | DATE | NOT NULL | Deal start date |
| deal_end_date | DATE | NOT NULL | Deal end date |
| receipt_no | TEXT | NOT NULL | Receipt number |
| receipt_no2 | TEXT | NULL | Receipt 2 number |
| receipt_no3 | TEXT | NULL | Receipt 3 number |
| form_status | VARCHAR(10) | NULL | Complete/Incomplete |
| rental_kyc_number | TEXT | NOT NULL | KYC number |
| is_rental_aml | CHAR(3) | NULL | AML check Yes/No |
| kyc_number | TEXT | NULL | KYC number |
| comments_finance | TEXT | NULL | Finance comments |
| created_at | DATETIME | NULL | Creation timestamp |
| updated_at | DATETIME | NULL | Update timestamp |
| created_by | VARCHAR(191) | NULL | Creator ID |
| updated_by | VARCHAR(191) | NULL | Updater ID |
| account_id | BIGINT | FOREIGN KEY | FK → accounts(id) |
| property_id | BIGINT | FOREIGN KEY | FK → properties(id) |
| is_deleted | CHAR(1) | DEFAULT 'N' | Soft delete Y/N |
| plot_no | TEXT | NULL | Plot number |
| mode_of_payment | TEXT | NULL | Payment mode |
| deal_agent | VARCHAR(191) | NULL | Deal agent |
| receipt_id | INT | DEFAULT 0 | Receipt ID |
| receipt_id2 | INT | DEFAULT 0 | Receipt 2 ID |
| receipt_id3 | INT | DEFAULT 0 | Receipt 3 ID |
| property_usage | VARCHAR(191) | NULL | Property usage type |
| property_size | VARCHAR(191) | NULL | Property size |
| premises_no | VARCHAR(191) | NULL | Premises number |
| security_deposit | VARCHAR(191) | NULL | Security deposit |
| submitted_by_agent | INT | NOT NULL | Agent ID |
| property_type | VARCHAR(191) | NULL | Property type |
| tenancy_application_form | TEXT | NULL | Application file |
| screening | TEXT | NOT NULL | Screening status |
| screening_comments | TEXT | NULL | Screening notes |
| seller_nationality | VARCHAR(191) | NOT NULL | Seller nationality |
| buyer_nationality | VARCHAR(191) | NOT NULL | Buyer nationality |
| manager_approved_rejected | CHAR(1) | DEFAULT 'P' | Manager approval |
| re_submitted_date | DATE | NULL | Resubmission date |

**Foreign Keys:**
- `submitted_by_user_id` → `users.id` (DO_NOTHING)
- `account_id` → `accounts.id` (DO_NOTHING)
- `property_id` → `properties.id` (SET_NULL)

**Indexes:**
- `idx_form_status` on (form_status)
- `idx_is_deleted` on (is_deleted)
- `idx_is_approved_rejected` on (is_approved_rejected)
- `idx_manager_approved_rejected` on (manager_approved_rejected)
- `idx_finance_entered` on (is_entered_in_finance_system)
- Composite indexes on various combinations

---

### Table: `sales_deals`

**Purpose:** Sales transaction management with approval workflow

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| id | AutoField | PRIMARY KEY | Deal ID |
| submitted_date | DATE | NULL | Submission date |
| re_submitted_date | DATE | NULL | Resubmission date |
| submitted_by_user_id | INT | FOREIGN KEY | FK → users(id) |
| date | DATE | NOT NULL | Deal date |
| reference_number | TEXT | NOT NULL | Reference number |
| unit_details | TEXT | NOT NULL | Unit information |
| builduing_name | TEXT | NOT NULL | Building name |
| project_name | TEXT | NOT NULL | Project name |
| developer_details | TEXT | NULL | Developer info |
| seller_name | TEXT | NOT NULL | Seller name |
| seller_source | TEXT | NOT NULL | Seller source |
| selller_mobile | TEXT | NOT NULL | Seller mobile |
| seller_email | TEXT | NULL | Seller email |
| buyer_name | TEXT | NOT NULL | Buyer name |
| buyer_source | TEXT | NOT NULL | Buyer source |
| buyer_mobile | TEXT | NOT NULL | Buyer mobile |
| buyer_email | TEXT | NULL | Buyer email |
| seller_agency | TEXT | NULL | Seller agency |
| seller_agent_name | TEXT | NULL | Seller agent name |
| seller_agent_phone | TEXT | NULL | Seller agent phone |
| seller_agent_email | TEXT | NULL | Seller agent email |
| seller_agency_brn | TEXT | NULL | Seller BRN |
| buyer_agency | TEXT | NULL | Buyer agency |
| buyer_agent_name | TEXT | NULL | Buyer agent name |
| buyer_agent_phone | TEXT | NULL | Buyer agent phone |
| buyer_agent_email | TEXT | NULL | Buyer agent email |
| buyer_agency_brn | TEXT | NULL | Buyer BRN |
| mediating_agency | TEXT | NULL | Mediator agency |
| mediating_agent_name | TEXT | NULL | Mediator name |
| mediating_agent_phone | TEXT | NULL | Mediator phone |
| mediating_agent_email | TEXT | NULL | Mediator email |
| mediating_agency_brn | TEXT | NULL | Mediator BRN |
| signed_mou | TEXT | NULL | MOU file |
| new_title_deed | TEXT | NULL | New title deed file |
| old_title_deed | TEXT | NULL | Old title deed file |
| owners_passport_copy | TEXT | NULL | Owner passport file |
| buyers_passport_copy | TEXT | NULL | Buyer passport file |
| buyers_deposit_cheque_copy | TEXT | NULL | Buyer cheque file |
| sellers_deposit_cheque_copy | TEXT | NULL | Seller cheque file |
| seller_poa_passport_copy | TEXT | NULL | Seller POA file |
| buyer_poa_passport_copy | TEXT | NULL | Buyer POA file |
| total_commission | TEXT | NULL | Total commission |
| less_outsude_commission | TEXT | NULL | Outside commission |
| net_commission | TEXT | NULL | Net commission |
| classic | TEXT | NULL | Classic share |
| agent1 | TEXT | NULL | Agent 1 share |
| agent2 | TEXT | NULL | Agent 2 share |
| agent3 | TEXT | NULL | Agent 3 share |
| is_approved_rejected | CHAR(1) | DEFAULT 'P' | P/F/A/R status |
| approved_rejected_by | TEXT | NULL | Approver ID |
| is_entered_in_finance_system | CHAR(1) | DEFAULT '0' | Finance entry |
| comments | TEXT | NULL | Admin comments |
| deal_amount | TEXT | NULL | Deal amount |
| owner_eid_copy | TEXT | NULL | Owner EID file |
| agent_name1 | TEXT | NULL | Agent 1 name |
| agent_name2 | TEXT | NULL | Agent 2 name |
| agent_name3 | TEXT | NULL | Agent 3 name |
| buyer_eid | TEXT | NULL | Buyer EID file |
| agent_comment | TEXT | NULL | Agent comments |
| receipt_no | TEXT | NULL | Receipt number |
| receipt_no2 | TEXT | NULL | Receipt 2 |
| receipt_no3 | TEXT | NULL | Receipt 3 |
| seller_poa_copy | TEXT | NULL | Seller POA |
| buyer_poa_copy | TEXT | NULL | Buyer POA |
| buyer_poa_eid | TEXT | NULL | Buyer POA EID |
| seller_poa_eid | TEXT | NULL | Seller POA EID |
| form_status | VARCHAR(10) | NULL | Complete/Incomplete |
| sale_kyc_number | TEXT | NULL | KYC number |
| form_i_copy | TEXT | NULL | Form I file |
| referral_agreement_copy | TEXT | NULL | Referral agreement |
| management_approval_form_copy | TEXT | NULL | Approval form |
| is_sale_aml | CHAR(3) | NULL | AML Yes/No |
| kyc_number | TEXT | NULL | KYC number |
| comments_finance | TEXT | NULL | Finance comments |
| created_at | DATETIME | NULL | Creation time |
| updated_at | DATETIME | NULL | Update time |
| created_by | VARCHAR(191) | NOT NULL | Creator ID |
| updated_by | VARCHAR(191) | NULL | Updater ID |
| account_id | BIGINT | FOREIGN KEY | FK → accounts(id) |
| property_id | BIGINT | FOREIGN KEY | FK → properties(id) |
| is_deleted | CHAR(1) | DEFAULT 'N' | Soft delete |
| deal_agent | VARCHAR(191) | NULL | Deal agent |
| receipt_id | VARCHAR(191) | DEFAULT '0' | Receipt ID |
| receipt_id2 | VARCHAR(191) | DEFAULT '0' | Receipt 2 ID |
| receipt_id3 | VARCHAR(191) | DEFAULT '0' | Receipt 3 ID |
| submitted_by_agent | INT | NOT NULL | Agent ID |
| screening | TEXT | NOT NULL | Screening status |
| screening_comments | TEXT | NOT NULL | Screening notes |
| seller_nationality | VARCHAR(191) | NOT NULL | Seller nation |
| buyer_nationality | VARCHAR(191) | NOT NULL | Buyer nation |
| manager_cheque_copy | TEXT | NULL | Manager cheque |
| manager_approved_rejected | CHAR(1) | DEFAULT 'P' | Manager approval |

**Foreign Keys:**
- `submitted_by_user_id` → `users.id` (DO_NOTHING)
- `account_id` → `accounts.id` (DO_NOTHING)
- `property_id` → `properties.id` (DO_NOTHING)

---

### Table: `rental_properties`

**Purpose:** Property management deals and renewals

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| id | BigAutoField | PRIMARY KEY | Property ID |
| deal_date | VARCHAR(10) | NULL | Deal date (dd-mm-yyyy) |
| reference_number | TEXT | NOT NULL | Reference number |
| project_name | TEXT | NOT NULL | Project name |
| building_name | TEXT | NOT NULL | Building name |
| unit_details | TEXT | NOT NULL | Unit details |
| pms_price | TEXT | NOT NULL | PMS price |
| pm_start_date | VARCHAR(10) | NULL | PM start date |
| pm_end_date | VARCHAR(10) | NULL | PM end date |
| tenancy_start_date | VARCHAR(10) | NULL | Tenancy start |
| tenancy_end_date | VARCHAR(10) | NULL | Tenancy end |
| owner_first_name | TEXT | NOT NULL | Owner first name |
| owner_source | TEXT | NOT NULL | Owner source |
| owner_mobile | TEXT | NOT NULL | Owner mobile |
| owner_email | TEXT | NOT NULL | Owner email |
| agency_name | TEXT | NOT NULL | Agency name |
| agent_name | TEXT | NOT NULL | Agent name |
| brn | TEXT | NULL | BRN number |
| agent_phone | TEXT | NOT NULL | Agent phone |
| agent_email | TEXT | NULL | Agent email |
| no_of_cheque | TEXT | NOT NULL | Number of cheques |
| cheque_date | TEXT | NOT NULL | Cheque dates |
| pms_contract | TEXT | NOT NULL | PMS contract file |
| owner_passport_copy | TEXT | NOT NULL | Owner passport |
| owner_eid_copy | TEXT | NULL | Owner EID |
| pms_cheque_copy | TEXT | NOT NULL | PMS cheque |
| title_deed | TEXT | NOT NULL | Title deed |
| poa_pp | TEXT | NULL | POA passport |
| poa_copy | TEXT | NULL | POA copy |
| key_hand_over_form | TEXT | NULL | Key handover |
| kyc_form | TEXT | NULL | KYC form |
| kyc_number | TEXT | NULL | KYC number |
| total_commission | TEXT | NOT NULL | Total commission |
| less_outside_commission | TEXT | NOT NULL | Outside commission |
| net_commission | TEXT | NOT NULL | Net commission |
| classic | TEXT | NOT NULL | Classic share |
| agent1 | TEXT | NOT NULL | Agent 1 share |
| agent2 | TEXT | NULL | Agent 2 share |
| agent3 | TEXT | NULL | Agent 3 share |
| comments | TEXT | NULL | Comments |
| agent_name1 | TEXT | NULL | Agent 1 name |
| agent_name2 | TEXT | NULL | Agent 2 name |
| agent_name3 | TEXT | NULL | Agent 3 name |
| receipt_no | TEXT | NOT NULL | Receipt number |
| receipt_no2 | TEXT | NULL | Receipt 2 |
| receipt_no3 | TEXT | NULL | Receipt 3 |
| form_status | VARCHAR(50) | NULL | Complete/Incomplete |
| created_at | DATETIME | NULL | Creation time |
| updated_at | DATETIME | NULL | Update time |
| created_by | VARCHAR(191) | NULL | Creator ID |
| updated_by | VARCHAR(191) | NULL | Updater ID |
| account_id | BIGINT | FOREIGN KEY | FK → accounts(id) |
| status | VARCHAR(20) | DEFAULT 'Active' | Property status |
| deal_sno | INT | NULL | Deal serial number |
| is_approved_rejected | CHAR(1) | DEFAULT 'P' | Approval status |
| approved_rejected_by | TEXT | NULL | Approver ID |
| is_entered_in_finance_system | CHAR(1) | NOT NULL | Finance entry |
| comments_finance | TEXT | NULL | Finance comments |
| submitted_by_user_id | INT | NOT NULL | Submitter ID |
| is_deleted | CHAR(1) | DEFAULT 'N' | Soft delete |
| agent_comment | TEXT | NULL | Agent comments |
| is_property_aml | CHAR(3) | NOT NULL | AML status |
| screening | TEXT | NOT NULL | Screening status |
| screening_comments | TEXT | NULL | Screening notes |
| seller_nationality | VARCHAR(191) | NOT NULL | Seller nationality |
| buyer_nationality | VARCHAR(191) | NULL | Buyer nationality |
| submitted_date | DATE | NOT NULL | Submission date |
| re_submitted_date | DATE | NULL | Resubmission date |
| manager_approved_rejected | CHAR(1) | DEFAULT 'P' | Manager approval |

**Foreign Keys:**
- `account_id` → `accounts.id` (DO_NOTHING)

---

### Table: `properties`

**Purpose:** Master property data (Bayut integration)

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| id | BigAutoField | PRIMARY KEY | Property ID |
| bayut_property_ref_no | VARCHAR(191) | UNIQUE | Bayut reference |
| property_status | VARCHAR(7) | NOT NULL | Property status |
| permit_number | BIGINT | NOT NULL | Permit number |
| property_purpose | VARCHAR(4) | NOT NULL | Sale/Rent |
| property_parent_type | VARCHAR(11) | NOT NULL | Parent type |
| property_type | VARCHAR(16) | NOT NULL | Type (Apartment/Villa) |
| furnished | VARCHAR(3) | NULL | Yes/No |
| city | VARCHAR(191) | NOT NULL | City |
| locality | VARCHAR(191) | NOT NULL | Locality |
| sub_locality | VARCHAR(191) | NULL | Sub-locality |
| tower_name | VARCHAR(191) | NULL | Tower name |
| bayut_location_id | INT | NOT NULL | Bayut location ID |
| property_title | VARCHAR(191) | NULL | Property title |
| property_description | TEXT | NULL | Description |
| property_size | INT | NOT NULL | Size value |
| property_size_unit | VARCHAR(191) | NOT NULL | sqft/sqm |
| bedrooms | INT | NOT NULL | Number of bedrooms |
| bathroom | INT | NOT NULL | Number of bathrooms |
| price | INT | NOT NULL | Price |
| rent_frequency | VARCHAR(191) | NULL | Yearly/Monthly |
| listing_agent | VARCHAR(191) | NULL | Listing agent |
| listing_agent_phone | VARCHAR(191) | NULL | Agent phone |
| listing_agent_email | VARCHAR(191) | NULL | Agent email |
| off_plan | VARCHAR(191) | NULL | Off-plan status |
| featured_on_company_website | VARCHAR(5) | NULL | Featured flag |
| exclusive_rights | VARCHAR(3) | NULL | Exclusive yes/no |
| geopoints_latitude | DECIMAL(8,6) | NULL | Latitude |
| geopoints_longitude | DECIMAL(8,6) | NULL | Longitude |
| completion_status | VARCHAR(191) | NULL | Completion status |
| last_updated | DATETIME | NULL | Last update |
| created_at | DATETIME | NULL | Creation time |
| updated_at | DATETIME | NULL | Update time |

---

### Table: `receipts`

**Purpose:** Third-party commission receipts

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| id | BigAutoField | PRIMARY KEY | Receipt ID |
| date | DATE | NOT NULL | Receipt date |
| receipt_number | BIGINT | NOT NULL | Receipt number |
| dhs | VARCHAR(191) | NOT NULL | Amount (Dirhams) |
| fils | VARCHAR(191) | NOT NULL | Amount (Fils) |
| cheque_no | VARCHAR(191) | NULL | Cheque number |
| bank | VARCHAR(191) | NULL | Bank name |
| sec_date | DATE | NOT NULL | Security date |
| being | VARCHAR(191) | NOT NULL | Being description |
| created_at | DATETIME | NULL | Creation time |
| updated_at | DATETIME | NULL | Update time |
| status | VARCHAR(191) | NOT NULL | Receipt status |
| deal_type | VARCHAR(191) | NOT NULL | Deal type |
| received_from | VARCHAR(191) | NULL | Received from |
| payment_type | VARCHAR(191) | NULL | Payment type |
| deal_refer_no | VARCHAR(191) | NULL | Deal reference |
| sum_of_dhs | VARCHAR(191) | NOT NULL | Total amount |
| agent_name | VARCHAR(191) | NOT NULL | Agent name |
| project_name | VARCHAR(191) | NOT NULL | Project name |
| building_name | VARCHAR(191) | NOT NULL | Building name |
| unit_number | VARCHAR(191) | NOT NULL | Unit number |
| account_id | INT | NOT NULL | Account ID |
| agent_id | INT | NOT NULL | Agent ID |
| agent_email | VARCHAR(255) | NOT NULL | Agent email |
| mail_status | VARCHAR(255) | NULL | Email sent status |

---

### Table: `management_receipts`

**Purpose:** Property management fee receipts

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| id | BigAutoField | PRIMARY KEY | Receipt ID |
| date | DATE | NOT NULL | Receipt date |
| receipt_number | VARCHAR(100) | NULL | Receipt number |
| dhs | VARCHAR(191) | NOT NULL | Amount (Dirhams) |
| fils | VARCHAR(191) | NOT NULL | Amount (Fils) |
| cheque_no | VARCHAR(15) | NULL | Cheque number |
| bank | VARCHAR(255) | NULL | Bank name |
| sec_date | DATE | NOT NULL | Security date |
| being | VARCHAR(191) | NOT NULL | Being description |
| status | VARCHAR(191) | NOT NULL | Receipt status |
| deal_type | VARCHAR(50) | NOT NULL | Management/Ejari Fee |
| received_from | VARCHAR(191) | NULL | Received from |
| payment_type | VARCHAR(50) | NOT NULL | Cash/Cheque/Transfer |
| deal_refer_no | VARCHAR(191) | NULL | Deal reference |
| sum_of_dhs | VARCHAR(191) | NOT NULL | Total amount |
| agent_name | VARCHAR(191) | NOT NULL | Agent name |
| project_name | VARCHAR(191) | NOT NULL | Project name |
| building_name | VARCHAR(191) | NOT NULL | Building name |
| unit_number | VARCHAR(191) | NOT NULL | Unit number |
| created_at | DATETIME | NULL | Creation time |
| updated_at | DATETIME | NULL | Update time |
| account_id | INT | NULL | Account ID |

---

### Table: `deposits`

**Purpose:** Third-party deposit transactions

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| id | AutoField | PRIMARY KEY | Deposit ID |
| date | DATE | NOT NULL | Deposit date |
| deposit_number | BIGINT | NOT NULL | Deposit number |
| dhs | VARCHAR(191) | NOT NULL | Amount (Dirhams) |
| fils | VARCHAR(191) | NOT NULL | Amount (Fils) |
| cheque_no | VARCHAR(191) | NULL | Cheque number |
| bank | VARCHAR(191) | NULL | Bank name |
| sec_date | DATE | NOT NULL | Security date |
| being | VARCHAR(191) | NOT NULL | Being description |
| status | VARCHAR(191) | NULL | Deposit status |
| deal_type | VARCHAR(191) | NOT NULL | Deal type |
| received_from | VARCHAR(191) | NULL | Received from |
| payment_type | VARCHAR(191) | NULL | Payment type |
| deal_refer_no | VARCHAR(191) | NULL | Deal reference |
| sum_of_dhs | VARCHAR(191) | NOT NULL | Total amount |
| agent_name | VARCHAR(191) | NULL | Agent name |
| project_name | VARCHAR(191) | NOT NULL | Project name |
| building_name | VARCHAR(191) | NOT NULL | Building name |
| unit_number | VARCHAR(191) | NOT NULL | Unit number |
| created_at | DATETIME | NULL | Creation time |
| updated_at | DATETIME | NULL | Update time |
| account_id | INT | NOT NULL | Account ID |
| on_behalf_of | VARCHAR(191) | NOT NULL | On behalf of |

---

## 5. API / Application Flow

### Authentication Endpoints
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/login/` | POST | User login authentication |
| `/logout/` | POST | User logout |
| `/register/` | POST | User registration |

### Rental Deal Endpoints
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/rental-deals/filter/` | POST | Filter and search rental deals (DataTables) |
| `/rental-deals/create/` | POST | Create new rental deal |
| `/rental-deals/update/<id>/` | PUT | Update existing rental deal |
| `/rental-deals/view/<id>/` | GET | View rental deal details |
| `/rental-deals/<id>/delete/` | DELETE | Delete rental deal |
| `/rental-deals/list/` | GET | List all rental deals |
| `/rental-deals/draft/` | GET | List draft deals |
| `/rental-deals/pending/` | GET | List pending approval deals |
| `/rental-deals/approved/` | GET | List approved deals |
| `/rental-deals/rejected/` | GET | List rejected deals |
| `/rental-deals/waiting/` | GET | List deals waiting for finance |
| `/rental-deals/pending-finance/` | GET | List pending finance deals |
| `/rental-deals/entered-finance/` | GET | List finance-entered deals |
| `/update-single-field/` | POST | Update single finance field |
| `/api/agents/dropdown/` | GET | Get agent dropdown data |
| `/api/receipts/dropdown/` | GET | Get receipt dropdown data |
| `/tenancey/contract/download/<id>/` | GET | Download tenancy contract PDF |

### Sales Deal Endpoints
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/sales-deals/filter/` | POST | Filter and search sales deals (DataTables) |
| `/sales-deals/` | GET/POST | List or create sales deals |
| `/sales-deals/view/<id>/` | GET | View sales deal details |
| `/api/sales-deals/update/<id>/` | PUT | Update sales deal |
| `/sales-deals/<id>/edit/` | GET | Sales deal edit page |
| `/sales-deals/<id>/delete/` | DELETE | Delete sales deal |
| `/sales-deals/create/` | GET | Sales deal creation page |
| `/api/sales-deals/create/` | POST | Create sales deal API |
| `/sales-deals/list/` | GET | All sales deals list |
| `/sales-deals/draft/` | GET | Draft sales deals |
| `/sales-deals/pending/` | GET | Pending sales deals |
| `/sales-deals/approved/` | GET | Approved sales deals |
| `/sales-deals/rejected/` | GET | Rejected sales deals |
| `/sales-deals/update-single-field/` | POST | Update finance field |

### Property Management Endpoints
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/rental-properties/filter/` | POST | Filter properties |
| `/rental-properties/<id>/view/` | GET | View property details |
| `/rental-properties/<id>/edit/` | GET/PUT | Edit property |
| `/api/rental-properties/<id>/` | PUT | Update property API |
| `/rental-properties/<id>/delete/` | DELETE | Delete property |
| `/rental-properties/create/` | POST | Create property |
| `/rental-properties/list/` | GET | All properties |
| `/rental-properties/draft/` | GET | Draft properties |
| `/rental-properties/approved/` | GET | Approved properties |
| `/rental-properties/<id>/renew/` | GET | Renew property page |
| `/api/rental-properties/<id>/update-finance/` | POST/PUT | Update finance status |

### Management Receipt Endpoints
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/management-receipts/` | GET | Management receipts page |
| `/management-receipts/create/` | POST | Create management receipt |
| `/management-receipts/<id>/edit-receipt/` | GET/POST | Edit receipt |
| `/management-receipts/<id>/view-receipt/` | GET | View receipt |
| `/management-receipts/<id>/downloadReceiptPDF/` | GET | Download receipt PDF |
| `/management-receipts/managerdatatablefilter/` | POST | Filter receipts |

### Third-Party Receipt Endpoints
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/third_party_receipts/list/` | GET | List third-party receipts |
| `/third_party_receipts/api/deposits/filter/` | POST | Filter deposits |
| `/third_party_receipts/api/deposits/create/` | POST | Create deposit |
| `/third_party_receipts/api/deposits/edit/<id>/` | PUT | Edit deposit |
| `/third_party_receipts/create/` | GET | Create page |
| `/third_party_receipts/third-party/view/<id>/` | GET | View third-party receipt |
| `/third_party_receipts/recipts/download/<id>/` | GET | Download receipt PDF |

### Core & Receipt Endpoints
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Home/dashboard redirect |
| `/dashbroad/` | GET | Main dashboard |
| `/list/` | GET | Receipts list |
| `/api/filter/` | POST | Filter receipts |
| `/create/` | GET/POST | Create receipt |
| `/view/<id>/` | GET | View receipt |
| `/api/edit/<id>/` | PUT | Edit receipt |
| `/<id>/download/` | GET | Download receipt PDF |
| `/api/agents/` | GET | Agent list API |
| `/api/dashboard-stats/` | GET | Dashboard statistics |
| `/api/commission-stats/` | GET | Commission statistics |

### Role Management Endpoints
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/role/list/` | GET | Role management list page |
| `/role/create/` | GET, POST | Create new role page |
| `/role/edit/<id>/` | GET, PUT | Edit role page |
| `/role/view/<id>/` | GET | View role details page |
| `/role/filter/` | POST | DataTables filter for roles |
| `/role/api/list/` | GET | Get all roles (API) |
| `/role/api/create/` | POST | Create role (API) |
| `/role/api/<id>/` | GET | Retrieve role details (API) |
| `/role/api/<id>/update/` | PUT | Update role (API) |
| `/role/api/<id>/partial-update/` | PATCH | Partial update role (API) |
| `/role/api/<id>/delete/` | DELETE | Delete role (API) |

### Reports Management Endpoints
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/agent-commission-report/` | GET | Agent commission report page |
| `/agent-commission-report/datatable/` | POST | DataTables filter for commission report |
| `/agent-performance-report/` | GET | Agent performance report page |
| `/agent-performance-report/datatable/` | POST | DataTables filter for performance report |
| `/api/agents/dropdown/` | GET | Get agents dropdown for reports |

---

## Authentication

### Type of Authentication
**Session-based authentication** with Django's built-in auth system, extended with custom user model and role-based permissions.

### Authentication Flow

1. **User Login**
   - User submits email and password to `/login/`
   - System validates credentials against `Users` model
   - Password verification using bcrypt hashing
   - On success, Django creates session and stores session ID in cookie
   - User is redirected to dashboard (`/`)

2. **Custom User Model**
   - Uses email as primary authentication field (USERNAME_FIELD = 'email')
   - Custom user model: `core.Users` (AUTH_USER_MODEL = 'core.Users')
   - Extends Django's AbstractBaseUser and PermissionsMixin
   - User attributes: name, email, mobile_number, gender, dob, timezone, image

3. **Role-Based Access Control (RBAC)**
   - **Roles**: Admin, Manager, Agent, Finance
   - Permissions managed through Django Groups and Permissions
   - Account-specific groups via `GroupProfile` linking groups to accounts
   - Permissions auto-created on account creation with predefined role permissions

4. **Multi-Tenancy**
   - Each user belongs to an account (tenant)
   - `user_account_id` field links users to accounts
   - Groups scoped to specific accounts via `GroupProfile.account`
   - Data isolation enforced at query level

5. **Session Management**
   - Login redirect: `/` (LOGIN_REDIRECT_URL)
   - Logout redirect: `/login/` (LOGOUT_REDIRECT_URL)
   - Login URL: `/login/` (LOGIN_URL)
   - Session data stored in database (`django_session` table)

6. **Permission Checking**
   - Custom middleware for permission enforcement
   - Permissions verified in views using decorators and mixins
   - Permission examples: `manage_rental_deals`, `view_pending_sales_deals`, `edit_approved_properties`

7. **Alternative Authentication Backend** (Commented out)
   - Laravel authentication backend support (`LaravelBackend`)
   - BCrypt password verification for Laravel-migrated users
   - Found in `core/authentication_backend.py` (currently disabled)

---

## 7. Reports Management Module

### Overview
The Reports Management module provides comprehensive reporting and analytics capabilities for tracking agent performance and commission details across rental and sales deals.

### Report Types

#### 1. Agent Commission Report
**Purpose:** Track individual deal commissions for each agent

**Features:**
- Lists all rental and sales deals with commission breakdowns
- Filters by reference number, unit details, building, project, agent name, deal type, and date range
- Shows gross commission and net commission per deal
- DataTables integration with server-side processing
- Combined data from both `rental_deals` and `sales_deals` tables

**Columns Displayed:**
- Primary Agent Name
- Secondary Agent Name
- Deal Type (Rental/Sales)
- Reference Number
- Unit Details
- Project Name
- Building Name
- Price (Rental Price or Deal Amount)
- Deal Date
- Gross Commission
- Net Commission

**API Endpoint:** `/agent-commission-report/datatable/` (POST)

**Filters:**
- Reference Number
- Unit Details
- Building Name
- Project Name
- Agent Name
- Deal Type (Rental/Sales)
- Date Range (From/To)

---

#### 2. Agent Performance Report
**Purpose:** Aggregate performance metrics by agent

**Features:**
- Groups deals by agent and deal type
- Calculates total number of deals per agent
- Sums total gross commission per agent
- Sums total net commission per agent
- Filter by number of deals range
- Filter by commission amount ranges
- Multi-tenant aware (account_id filtering)

**Columns Displayed:**
- Agent Name
- Deal Type (Rental/Sales)
- Number of Deals
- Total Gross Commission
- Total Net Commission

**API Endpoint:** `/agent-performance-report/datatable/` (POST)

**Filters:**
- Agent Name
- Deal Type (Rental/Sales)
- Minimum/Maximum Number of Deals
- Minimum/Maximum Gross Commission
- Minimum/Maximum Net Commission
- Date Range (From/To)

---

### Technical Implementation

#### Data Sources
Reports aggregate data from:
- **rental_deals table** - Rental transactions
- **sales_deals table** - Sales transactions
- **users table** - Agent information

#### Data Processing Flow
```
1. Fetch rental deals (filtered by account_id)
2. Fetch sales deals (filtered by account_id)
3. Serialize both datasets using RentalDealsSerializer and SalesDealsSerializer
4. Combine into single dataset
5. Apply filters (reference number, agent, dates, etc.)
6. Apply DataTables search
7. Sort by requested column
8. Paginate results
9. Return JSON response
```

#### Commission Calculation
```python
For each deal:
  - Gross Commission = total_commission field
  - Net Commission = net_commission field
  - Classic Share = classic field
  - Agent Shares = agent1 + agent2 + agent3 fields
```

#### Performance Aggregation
```python
Group deals by (agent_name, deal_type):
  - Count number of deals
  - Sum gross commissions (with safe_float parsing)
  - Sum net commissions (with safe_float parsing)
  - Apply min/max filters
  - Return aggregated results
```

### Permissions
Custom permissions for reports module:
- `reports_management` - Access to reports module
- `agent_commission_report` - View agent commission report
- `agent_performance_report` - View agent performance report

### Templates
- `home/agent_commission_report.html` - Commission report UI
- `home/agent_performance_report.html` - Performance report UI

### Key Features
- **Multi-tenancy Support:** All queries filtered by `account_id`
- **DataTables Integration:** Server-side processing for large datasets
- **Combined Data:** Merges rental and sales deals into unified reports
- **Safe Float Parsing:** Handles messy commission data with regex extraction
- **Flexible Filtering:** Multiple filter criteria for both reports
- **Export Ready:** JSON response format compatible with Excel/CSV export

### Use Cases
1. **Commission Tracking:** Track all commissions paid to agents per deal
2. **Performance Analysis:** Compare agent performance across time periods
3. **Financial Reporting:** Calculate total commissions for accounting
4. **Agent Evaluation:** Identify top-performing agents by deal count and commission
5. **Audit Trail:** Detailed breakdown of all commission payments

---

## 8. Notes & Assumptions

### Missing Configurations
- `.env` file not included in repository - must be created manually
- AWS S3 bucket configuration required for file storage
- Email credentials (currently hardcoded in settings.py) should be moved to environment variables
- MySQL database must be created and configured before first run
- SECRET_KEY in settings.py is exposed (development key) - should use environment variable for production

### Unclear Areas
- Database schema migrations may need review - some models have `managed = False`
- Multiple commented model classes in various files suggest ongoing refactoring
- Some URL patterns are duplicated or overridden in main urls.py
- Exact requirements for bcrypt vs Django password hashing (typo: "bycrypt" in requirements.txt should be "bcrypt")
- Cron job execution environment not specified

### Assumptions Made
- Project is for a real estate agency managing multiple deal types
- Multi-tenant architecture supports multiple organizations on single deployment
- AWS S3 is primary storage for all uploaded files and documents
- MySQL is the production database (SQLite file present for development only)
- Email functionality configured for Microsoft Office 365 SMTP
- Scheduled tasks check for missing files in S3 daily at 9 PM (21:00 UTC)
- Custom logging implemented per module (Rental_Deal, Sales_Deals_Management, property_management_deals)
- Application designed for Dubai/Singapore region (AWS region: ap-southeast-1)
- Frontend uses DataTables for list views with server-side processing
- PDF generation using WeasyPrint for receipts and contracts
 

### Production Readiness Concerns
- DEBUG = True in settings.py (should be False for production)
- SECRET_KEY is hardcoded and insecure
- Email passwords hardcoded in settings
- No indication of HTTPS/SSL configuration
- No containerization (Docker) configuration found
- No CI/CD pipeline configuration visible

---

## Additional Information

### Logging
Separate log files for each module:
- `django.log` - Django framework errors
- `Rental_Deal/Rental_Deal.log` - Rental deal operations
- `Rental_Deal/Rental_Deal_File_Check.log` - Rental file validation
- `Sales_Deals_Management/Sales_Deals_Management.log` - Sales operations
- `Sales_Deals_Management/Sales_Deal_File_Check.log` - Sales file validation
- `property_management_deals/property_management_deals.log` - Property operations
- `property_management_deals/property_check_deals.log` - Property file validation

### Scheduled Tasks (Cron Jobs)
```python
# Runs daily at 9 PM UTC
- check_rental_in_S3 --days 2
- check_sale_in_S3 --days 2
```

### File Storage
- **Development**: Local filesystem (commented out)
- **Production**: AWS S3 bucket
- **URL Pattern**: `https://{bucket}.s3.amazonaws.com/live/classic_properties/`
- **Supported uploads**: Deal documents, property images, receipts, contracts

### Admin Interface
Django admin panel available at `/admin/` for superuser management of:
- User accounts
- Groups and permissions
- All deal types
- Properties and receipts

---

---

**Documentation Generated**: January 29, 2026  
**Django Version**: 5.2+  
**Python Version**: 3.8+  
**Database**: MySQL
