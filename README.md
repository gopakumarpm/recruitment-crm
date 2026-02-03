# 👥 Recruitment CRM - Streamlit Application

A comprehensive Recruitment Customer Relationship Management (CRM) system built with Streamlit, designed for recruitment teams to manage candidates, track interactions, and analyze recruitment metrics.

## 🌟 Features

### Core Functionality
- **User Authentication & Role-Based Access Control**
  - Admin, Recruiter, and Viewer roles
  - Secure password hashing with bcrypt
  - Session management with timeout

- **Candidate Management**
  - Full CRUD operations (Create, Read, Update, Delete)
  - Comprehensive candidate profiles with personal and professional information
  - Status tracking (Applied, Screening, Interview, Offer, Hired, Rejected)
  - Skills tracking, experience levels, and education history

- **Call History & Interaction Tracking**
  - Log calls, meetings, and emails
  - Track call duration, outcomes, and notes
  - Schedule follow-up actions with reminders
  - View complete candidate interaction timeline

- **Advanced Search & Filtering**
  - Multi-criteria search (status, skills, experience, location)
  - Real-time filtering and results
  - Export search results

- **Analytics Dashboard**
  - Key metrics and KPIs
  - Visual charts (pie charts, bar charts, funnels)
  - Recruitment pipeline visualization
  - Candidate distribution by status, source, and recruiter

- **Data Export**
  - Export candidates to CSV or Excel
  - Timestamped filenames for easy tracking
  - Bulk data download capabilities

- **User Management (Admin Only)**
  - Create and manage users
  - Assign roles and permissions
  - Activate/deactivate users

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd Recruitment
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Initialize the Database

The database will be automatically initialized on first run, but you can also manually initialize it:

```bash
python database/schema.py
```

This will create:
- SQLite database at `data/recruitment.db`
- All necessary tables (users, candidates, call_history, activity_log)
- Default admin user with credentials:
  - **Username:** `admin`
  - **Password:** `admin123`

⚠️ **Important:** Change the default admin password after first login!

### 4. Run the Application

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

## 📁 Project Structure

```
Recruitment/
├── app.py                          # Main entry point
├── config.py                       # Configuration settings
├── requirements.txt                # Python dependencies
├── .gitignore                      # Git ignore rules
├── README.md                       # This file
├── .streamlit/
│   └── config.toml                # Streamlit configuration
├── database/
│   ├── __init__.py
│   ├── db_manager.py              # Database operations
│   └── schema.py                  # Database schema & initialization
├── models/
│   ├── __init__.py
│   ├── user.py                    # User model
│   ├── candidate.py               # Candidate model
│   └── call_history.py            # Call history model
├── auth/
│   ├── __init__.py
│   ├── authenticator.py           # Authentication logic
│   └── session_manager.py         # Session state management
├── pages/
│   ├── 1_📊_Dashboard.py          # Analytics dashboard
│   ├── 2_👥_Candidates.py         # Candidate management
│   ├── 3_🔍_Search.py             # Advanced search
│   ├── 4_📞_Call_History.py       # Call tracking
│   ├── 5_📥_Import_Export.py      # Data export
│   └── 6_⚙️_Settings.py           # User settings & admin panel
├── components/
│   ├── __init__.py
│   └── charts.py                  # Chart components
├── utils/
│   ├── __init__.py
│   ├── validators.py              # Input validation
│   ├── exporters.py               # Export functionality
│   ├── formatters.py              # Data formatting
│   └── constants.py               # Application constants
└── data/
    └── recruitment.db             # SQLite database (created at runtime)
```

## 👤 User Roles & Permissions

### Admin
- Full access to all features
- User management (create, edit, delete users)
- Assign roles and permissions
- View activity logs
- All recruiter permissions

### Recruiter
- Manage candidates (create, edit, delete)
- Log and view call history
- Access search and analytics
- Export data
- Update own profile

### Viewer
- View candidates (read-only)
- View call history (read-only)
- Access dashboard and analytics
- Export data
- Update own profile

## 📊 Database Schema

### Users Table
- id, username, email, password_hash
- full_name, role, is_active
- created_at, updated_at

### Candidates Table
- Personal: first_name, last_name, email, phone, location, linkedin_url
- Professional: current_role, current_company, years_of_experience, skills, education
- Recruitment: status, position_applied, recruiter_id, source
- Additional: salary_expectation, notice_period, resume_url, notes
- Metadata: created_by, created_at, updated_at

### Call History Table
- candidate_id, recruiter_id, call_date
- call_type, duration, outcome
- notes, next_action, next_action_date

### Activity Log Table
- user_id, action_type, entity_type, entity_id
- description, created_at

## 🔧 Configuration

### Environment Variables (Optional)

You can customize settings in `config.py`:

- `DATABASE_PATH`: Path to SQLite database
- `SESSION_TIMEOUT_HOURS`: Session timeout duration (default: 24 hours)
- `DEFAULT_ADMIN_*`: Default admin credentials
- `RECORDS_PER_PAGE`: Pagination limit

## 🌐 Deployment to Streamlit Cloud

### 1. Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit: Recruitment CRM"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

### 2. Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository, branch (main), and main file (app.py)
5. Click "Deploy"

### 3. Configure Secrets (if needed)

In Streamlit Cloud dashboard, you can add secrets:

```toml
[admin]
username = "admin"
password = "your-secure-password"
email = "admin@yourcompany.com"
```

### Important Notes for Streamlit Cloud

⚠️ **Database Persistence**: Streamlit Cloud uses an ephemeral filesystem. The SQLite database will reset on redeploy. For production use, consider migrating to an external database like PostgreSQL.

**Options for Data Persistence:**
1. **Manual Backup**: Regularly export data using the Export feature
2. **External Database**: Use PostgreSQL with services like Supabase or Neon
3. **GitHub Sync**: Store database in repository (for small datasets only)

## 🧪 Testing

### Manual Testing Checklist

- [ ] Login with default admin credentials
- [ ] Create a new candidate
- [ ] Edit candidate details
- [ ] Search for candidates
- [ ] Log a call/interaction
- [ ] View dashboard analytics
- [ ] Export data to CSV/Excel
- [ ] Create a new user (admin)
- [ ] Change password
- [ ] Test different role permissions

### Run Local Tests

```bash
# Test database initialization
python database/schema.py

# Test imports
python -c "from models.candidate import candidate_model; print('OK')"
```

## 🔒 Security Features

- **Password Hashing**: bcrypt with salt
- **SQL Injection Prevention**: Parameterized queries
- **Input Validation**: Email, phone, URL validation
- **Session Management**: Timeout after 24 hours
- **Role-Based Access Control**: Server-side permission checking
- **Activity Logging**: Audit trail for sensitive operations

## 📈 Usage Tips

1. **Start with the Dashboard**: Get an overview of your recruitment pipeline
2. **Add Candidates**: Use the Candidates page to add new applicants
3. **Track Interactions**: Log every call in the Call History page
4. **Use Search**: Find candidates quickly with advanced filters
5. **Export Regularly**: Download data for backup and reporting
6. **Set Follow-ups**: Never miss a candidate with reminder dates

## 🐛 Troubleshooting

### Database Errors

```bash
# Reset database
rm data/recruitment.db
python database/schema.py
```

### Import Errors

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Port Already in Use

```bash
# Run on different port
streamlit run app.py --server.port 8502
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 📧 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact the development team

## 🎯 Future Enhancements

- Email integration for automated notifications
- Resume parsing with AI
- Calendar integration for interview scheduling
- Advanced reporting and custom dashboards
- Mobile-responsive design improvements
- PostgreSQL migration for production
- Real-time collaboration features
- API endpoints for integrations

## 🙏 Acknowledgments

Built with:
- [Streamlit](https://streamlit.io/) - Web framework
- [Plotly](https://plotly.com/) - Interactive charts
- [Pandas](https://pandas.pydata.org/) - Data manipulation
- [BCrypt](https://github.com/pyca/bcrypt/) - Password hashing

---

**Version:** 1.0.0
**Last Updated:** 2026-02-03
**Built with ❤️ using Streamlit**
