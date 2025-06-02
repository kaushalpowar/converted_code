# Investment Appointment Management System

## Introduction
This project is a modern Python/Streamlit rewrite of a legacy Informix 4GL application for managing investment appointments. The application handles the creation, modification, cancellation, and querying of investment appointments, including sell/buy transactions and remittance details.

## Directory Structure

```
/app
├── config/               # Configuration files
│   ├── .env              # Environment variables
│   └── config.py         # Application configuration
├── models/               # SQLAlchemy ORM models
│   ├── appointment.py    # Chah, Chad, Chap models
│   ├── policy.py         # Policy-related models
│   ├── investment.py     # Investment fund models
│   ├── client.py         # Client information models
│   ├── bank.py           # Bank information models
│   └── message.py        # Message system models (psrh, psrd)
├── schemas/              # Pydantic schemas for validation
│   ├── appointment.py    # Appointment schemas
│   ├── investment.py     # Investment schemas
│   └── payment.py        # Payment schemas
├── services/             # Business logic
│   ├── appointment_service.py  # Appointment CRUD operations
│   ├── investment_service.py   # Investment validation and processing
│   ├── policy_service.py       # Policy-related operations
│   └── payment_service.py      # Payment processing
├── db/                   # Database connection and migrations
│   ├── session.py        # SQLAlchemy session management
│   └── migrations/       # Alembic migration scripts
├── ui/                   # Streamlit pages and components
│   ├── Home.py           # Main entry point
│   ├── Add.py            # Add appointment page
│   ├── Cancel.py         # Cancel appointment page
│   ├── Modify.py         # Modify appointment page
│   ├── Query.py          # Query appointments page
│   └── Reports.py        # Message history & print preview
├── components/           # Reusable UI components
│   ├── investment_grid.py     # Investment grid component
│   └── remittance_form.py     # Remittance form component
├── utils/                # Utility functions
│   ├── date_utils.py     # Date manipulation utilities
│   ├── validation.py     # Common validation functions
│   ├── term_meaning.py   # Term meaning lookup (TermMeaning emulation)
│   ├── currency.py       # Currency utilities
│   ├── auth.py           # Authentication utilities
│   └── message_utils.py  # Message generation utilities
└── tests/                # Unit and integration tests
    ├── test_services/    # Service tests
    ├── test_models/      # Model tests
    └── test_ui/          # UI tests
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- PostgreSQL (or your preferred database)
- pip

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-org/investment-appointment-system.git
   cd investment-appointment-system
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure the database:
   - Create a `.env` file in the `config` directory with the following content:
     ```
     DATABASE_URL=postgresql://username:password@localhost/dbname
     SECRET_KEY=your_secret_key
     DEBUG=True
     ```

5. Run database migrations:
   ```bash
   alembic upgrade head
   ```

6. Load initial data (if needed):
   ```bash
   python scripts/load_initial_data.py
   ```

## Usage Instructions

### Running the Application

1. Start the Streamlit application:
   ```bash
   streamlit run ui/Home.py
   ```

2. Open your browser and navigate to `http://localhost:8501`

### Main Features

- **Add Appointment**: Create new investment appointments with sell/buy details or remittance information
- **Cancel Appointment**: Cancel existing appointments
- **Modify Appointment**: Update details of existing appointments
- **Query Appointment**: Search and view appointment history
- **Reports**: View and print message history

### Navigation

The application uses a sidebar for navigation between different features. Each page has its own form with validation and submission controls.

## Conversion Notes

### Key Differences from 4GL Version

1. **Architecture**: The 4GL monolithic application has been refactored into a layered architecture with clear separation of concerns:
   - Models (data structure)
   - Schemas (validation)
   - Services (business logic)
   - UI (presentation)

2. **Database Access**: 
   - Replaced direct SQL with SQLAlchemy ORM
   - Transactions are managed through SQLAlchemy sessions

3. **UI Changes**:
   - Terminal-based forms replaced with web-based Streamlit UI
   - Array-based data entry replaced with interactive data grids
   - Function key navigation replaced with buttons and links

4. **Validation**:
   - Form-level validation replaced with Pydantic schema validation
   - Business rule validation moved to service layer

### Limitations

- The Streamlit UI doesn't support some advanced terminal features like function keys
- Some complex cursor operations have been simplified
- Print functionality now generates PDFs or previews rather than direct printing

## Testing Procedures

### Unit Testing

Run the unit tests to verify individual components:

```bash
pytest tests/
```

### Integration Testing

Test the integration between components:

```bash
pytest tests/ --integration
```

### Comparison Testing with Original 4GL

To verify the conversion is correct, compare the behavior with the original 4GL application:

1. **Data Validation**: 
   - Enter the same test data in both systems
   - Verify validation errors are consistent

2. **Business Rules**:
   - Test edge cases (e.g., 100% allocation requirement, minimum amounts)
   - Compare results between systems

3. **Output Comparison**:
   - Generate messages in both systems
   - Compare the content of the message tables (psrh/psrd)

4. **Database State**:
   - After identical operations, compare the state of key tables (chah, chad, chap)

### Test Cases

Key test scenarios include:

1. Adding an appointment with multiple sell and buy transactions
2. Adding an appointment with remittance details
3. Modifying an existing appointment
4. Canceling an appointment
5. Querying appointments with various filters
6. Testing validation rules (e.g., 100% allocation, minimum amounts)
7. Testing date and frequency rules

## Manual Changes Required

Before running the application, the following manual changes are needed:

1. **Database Configuration**:
   - Update `config/.env` with your database credentials
   - Verify table structures match the expected schema

2. **External Service Integration**:
   - Implement or mock external service calls (risk checks, currency lookups)
   - Update `utils/auth.py` with your authentication logic

3. **Model Adjustments**:
   - Review and adjust SQLAlchemy models in `models/` to match your exact database schema
   - Verify foreign key relationships

4. **Business Rule Verification**:
   - Review validation rules in `services/` to ensure they match legacy behavior
   - Test edge cases specific to your business domain

## Troubleshooting

### Common Issues

1. **Database Connection Errors**:
   - Verify database credentials in `.env`
   - Check that the database server is running
   - Ensure the required tables exist

2. **Missing Dependencies**:
   - Run `pip install -r requirements.txt` to ensure all dependencies are installed
   - Check for version conflicts with `pip check`

3. **UI Rendering Issues**:
   - Clear browser cache
   - Restart the Streamlit server
   - Check browser console for JavaScript errors

4. **Data Validation Errors**:
   - Review the validation rules in the schemas
   - Check for data type mismatches
   - Verify business rule implementations

5. **Performance Issues**:
   - Enable query logging to identify slow database operations
   - Consider adding indexes to frequently queried fields
   - Review Streamlit caching strategy

### Getting Help

If you encounter issues not covered in this documentation:

1. Check the logs in the terminal running Streamlit
2. Review the SQLAlchemy documentation for ORM issues
3. Consult the Streamlit documentation for UI issues
4. File an issue in the project repository with detailed steps to reproduce

## Contributing

Please follow these guidelines when contributing to the project:

1. Create a feature branch from `main`
2. Follow the existing code style and architecture
3. Add tests for new functionality
4. Update documentation as needed
5. Submit a pull request with a clear description of changes

## License

This project is licensed under the MIT License - see the LICENSE file for details.