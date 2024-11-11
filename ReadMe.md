# PathSix CRM

# Documentation

## Introduction

### Overview of the PathSix CRM

The PathSix CRM is a comprehensive customer relationship management tool developed by PathSix Web Designs. Designed to streamline client management for small and medium-sized businesses, the CRM offers an intuitive interface that helps users efficiently organize, track, and maintain customer information. It includes functionalities such as client management, contact tracking, and user account handling to ensure that businesses can maintain strong relationships with their customers and improve their workflow.

### Key Features and Intended Usage

- **Client Management**: Easily create, view, and manage client profiles, complete with contact details and relevant notes.
- **Contact Tracking**: Link multiple contact persons to each client and store their individual information, such as phone numbers and emails.
- **User Account Management**: Manage user profiles, including registration, login, and account updates, with built-in authentication.
- **Flexible Data Handling**: Add, update, and delete client records, ensuring data accuracy and maintaining an organized database.
- **User-Friendly Interface**: Simplified navigation and well-structured templates to improve user experience and productivity.
- **Security Prompts**: Confirmation processes for sensitive actions like deleting client data, to prevent accidental data loss.
- **Responsive Design**: Optimized for a range of devices to allow users to manage client data anytime, anywhere.

The PathSix CRM is intended for use by businesses looking for an efficient way to manage their customer relationships, providing essential tools for clear record-keeping and easy access to client data.

### System Requirements and Prerequisites

**Server Requirements**:

- Flask web framework installed
- Python version 3.7 or higher
- Database setup (e.g., SQLite or a configured relational database)
- Web server (e.g., Nginx, Apache)

**Client-Side Requirements**:

- Modern web browser (Chrome, Firefox, Edge, Safari)
- Internet connection for remote access and updates

**Development Environment**:

- Flask-WTF for form handling
- SQLAlchemy for database interactions
- Properly configured Flask project with template and static file structure

**Security**:

- SSL/TLS for secure data transfer
- User authentication implemented with secure password handling (e.g., bcrypt)

The PathSix CRM is designed to be easy to deploy, allowing businesses to quickly start using it with minimal technical complexity while offering powerful, customizable functionality.

---

# PathSix CRM User Instruction Guide

Welcome to the PathSix CRM! This guide will help you navigate and use the main features of the CRM to manage your clients effectively.

## 1. General Navigation

The PathSix CRM is designed with an intuitive layout that allows for seamless navigation. The top navigation bar is your main tool for moving between pages.

### Navigation Menu

- **Home**: Returns to the CRM homepage.
- **Pricing**: View pricing details for PathSix services.
- **Contact**: Get in touch with PathSix Web Designs support.
- **CRM**: Access the CRM dashboard.
- **Login/Register**: Log in to or create an account.
- **Account/Logout**: Manage your account or log out if already logged in.

## 2. Pages Overview

### Home Page (`crm.html`)

- **Purpose**: The entry point for the CRM, with links to start managing clients.
- **Main Action**: Click on the relevant sections to navigate to client management or other tools.

### Customer List Page (`customers.html`)

- **Purpose**: View and manage all clients.
- **Features**:
  - **Client Table**: Displays a list of all clients with information like ID, name, website, pricing tier, email, and phone.
  - **Add New Client**: Click the “+Add New Client” link to go to the add client page.
  - **Reports Sidebar**: Use the left sidebar to view specific client information, such as email or phone reports.

### Add New Client Page (`create_client.html`)

- **Purpose**: Enter information for a new client.
- **Instructions**:
  1. Fill out the required fields under "Client Information," "Contact Person," and "Address Information."
  2. Add a note if necessary under "Contact Note."
  3. Click the submit button to save the new client.
- **Form Validation**: If any field has an error, the system will display an error message in red.

### Client Details Page (`client.html`)

- **Purpose**: View detailed information about a specific client.
- **Features**:
  - **Edit Client**: Click the “Edit Client” button to modify client details.
  - **Delete Client**: Use the delete form to remove a client after confirming the action.
- **Contact Information**: View associated contacts for the client or a message stating no contacts are available.

### Account Page (`account.html`)

- **Purpose**: View and update user account details.
- **Instructions**:
  - View your current username and email.
  - Fill in new information in the form and submit to update account details.

### Registration Page (`register.html`)

- **Purpose**: Create a new account for the CRM.
- **Instructions**:
  1. Enter a username, email, password, and confirm your password.
  2. Submit the form to register a new account.
  - **Error Handling**: Any form validation errors will be shown in red under the respective fields.

### Login Page (`login.html`)

- **Purpose**: Log in to the CRM.
- **Instructions**:
  1. Enter your registered email and password.
  2. Check "Remember Me" if desired for persistent login.
  3. Submit the form to log in.
- **Note**: A "Forgot password?" link is available for password reset.

### Delete Client Confirmation Page (`delete_client.html`)

- **Purpose**: Confirm and process the deletion of a client.
- **Instructions**:
  - Confirm the client name and click "Yes, Delete" to proceed.
  - Click “Cancel” to return to the client list without making changes.

## 3. Common Features and Tips

- **Form Validation**: Input fields show error messages in red if validation fails.
- **Flash Messages**: Important feedback messages may appear at the top of the page.
- **Responsive Design**: The CRM is optimized for use on both desktop and mobile devices.

## 4. Support and Contact

For any issues or support, please contact:

- **Email**: support@pathsixdesigns.com
- **Phone**: 325-305-9446

PathSix Web Designs aims to provide professional and efficient tools for your business needs. Happy client management!

<!-- prettier-ignore-start -->

NOTE: Below here is developer notes. 

I. Business Info
    a. name
    b. address
    c. email address
    d. phone
    e. contact person 
        1. phone 
        2. preferred communication method
    f. contact notes
    g. Whose sale was it?
    h. sales notes 
        1. What pricing tier are they in? 
        2. What extras were sold? 
        3. Did they have any ideas for their site? 
        4. How many pages and what are they? 
        5. Scheduling reminders?
    i. contract date
II. Reports
    a. billing cycle (monthly or yearly?)
    b. total revenue generated per client
    c. payment status tracking
III. Continuing Work On Websites
    a. change request history 
        1. dates 
        2. pages 
        3. sections
    b. pending requests 
        1. notes
IV. Advertising Mailing List
    a. Direct Mailing Addresses List 
        1. Have they been sent a postcard? 
        2. Date
    b. Follow up contact time/date
    c. Marketing campaign notes 
        1. success rate 
        2. feedback
V. PathSix Websites
    a. Domain
    b. Hosting site
    c. SSL status
    d. Notes
    e. automated reminders
VI. Hosting Accounts
    a. Website
    b. Cost
VII. Planning board for projects
VIII. Scheduling software

<!-- prettier-ignore-end -->

# Notes on Enhancing PathSix CRM with JavaScript

## Creating a Client-Side Search Feature

### Key Steps for Client-Side Search:

- Use cached data (like the `companies` array) to filter results. This makes the search fast and avoids unnecessary server requests.
- Display the filtered results directly on the page using JavaScript.

### Setting Up the Search:

#### HTML

Add a search input at the top of the page for users to type in:

---

## JavaScript Enhancements to Consider for the CRM

### 1. Client-Side Form Validation

- **Why**: Avoid unnecessary server requests and give users instant feedback.
- **How**: Use JavaScript to check if all required fields are filled and if formats are correct (like email or phone).
- **Note**: Instant feedback means fewer errors on form submissions, which users will appreciate.

### 2. AJAX for Asynchronous Updates

- **Idea**: Use AJAX to handle creating, updating, and deleting records without page reloads.
- **Create New Records**: Send form data to Flask via AJAX and update the client list dynamically.
- **Edit Records**: Implement modals or inline forms for editing, with AJAX handling the updates.
- **Delete Records**: Remove clients via AJAX to avoid full-page refreshes.

### 3. Dynamic Search and Filtering

- **Immediate Feedback**: Add search bars with JavaScript that filter results as users type.
- **Note to Self**: For larger datasets, consider debouncing or lazy-loading results.

### 4. Interactive UI Elements

- **Modals**: Use them for adding or editing data without moving to a different page.
- **Expandable Sections**: Let users toggle sections like "Business Info" or "Reports" for a cleaner UI.
- **Date Pickers**: Add a JavaScript date picker for scheduling reminders.

### 5. Real-Time Updates

- **Approach**: Use `setInterval()` or WebSockets for real-time data updates. Great for seeing the latest status without refreshing.

### 6. Drag and Drop

- **Feature**: Add drag-and-drop functionality for rearranging clients or tasks. Users might love this for managing their workflow visually.

### 7. Inline Editing

- **Concept**: Make fields directly editable (e.g., click a client’s phone number to edit it in place).
- **Plan**: Save changes with AJAX to keep things smooth and fast.

### 8. Notifications and Alerts

- **Reminders**: Use JavaScript to create custom alerts (e.g., billing cycle due soon).
- **Tip**: This is more user-friendly than relying on page refreshes for notifications.

### 9. Loading Spinners/Progress Indicators

- **Why**: Users need visual cues when data is loading or actions are processing.
- **Add**: Show spinners when AJAX requests are pending.

### 10. Autocomplete for Form Inputs

- **Use Case**: Autocomplete for "Business Name" or "Contact Person" fields can speed up data entry.
- **Implementation Note**: Keep the UI intuitive, so users can easily find existing records.

<!-- prettier-ignore-start -->

// Sample data for testing and development
const companies = [
    { company: "Acme Inc.", address: "123 Street", city: "Somewhere", state: "TX", zipcode: "12345", email: "contact@acme.com", phone: "123-456-7890" },
    // Add more sample data as needed for testing
];

// Function to render the customer table
function renderTable(data) {
    const table = document.getElementById("reportTable");
    table.innerHTML = `
        <tr class="sm-thead">
            <th>Company</th><th>Address</th><th>City</th><th>State</th><th>Zipcode</th><th>Email</th><th>Phone</th>
        </tr>
        ${data.map(company => `
            <tr>
                <td>${company.company}</td>
                <td>${company.address}</td>
                <td>${company.city}</td>
                <td>${company.state}</td>
                <td>${company.zipcode}</td>
                <td>${company.email}</td>
                <td>${company.phone}</td>
            </tr>`).join('')}
    `;
}

// Load the table initially with all data
renderTable(companies);

// Function to filter the table based on search input
function filterCustomers() {
    const query = document.getElementById("search").value.toLowerCase();
    const filteredData = companies.filter(company =>
        company.company.toLowerCase().includes(query) ||
        company.city.toLowerCase().includes(query) ||
        company.email.toLowerCase().includes(query) ||
        company.phone.includes(query)
    );
    renderTable(filteredData);
}

<!-- prettier-ignore-end -->
