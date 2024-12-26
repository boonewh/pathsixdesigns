# PathSix CRM - Version 0.2.3

Welcome to **PathSix CRM**, a lightweight and intuitive CRM solution designed for small businesses. This is the initial release, providing the following core features:

## Features

- **Customer Tracking**: Manage customer information easily.
- **Basic Projects Tracking**: Keep track of projects.
- **Leads Management**: Organize and manage potential customers effectively.
- **Authentication**: Secure user login and registration.
- **Basic Account Management**: Update account details seamlessly.

## Future Updates

The following features are planned for upcoming releases:

- **Expanded Projects and Leads Tracking**: Track deadlines and get follow-up reminders.
- **Calendar**: automatically push follow-ups and appoinments. Send reminders.
- **Chat platform**: Real-time communication with the ability to integrate leads into your sales pipeline.

## About

PathSix CRM is in active development and aims to provide an easy-to-use, scalable solution for growing businesses. Stay tuned for regular updates!

### Need to Knows

- **The left menu links on the /customers page do not work right now.**

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

---

# tl;dr

Develop an advanced CRM system for small businesses primarily with sales teams, including features like search, RBAC, project management, lead handling, and real-time communication.

## Goals

### Business Goals

- Increase client retention by 20% in the first year of release.
- Drive sales efficiency by equipping salespeople with real-time data and communication tools.
- Capture the small business market by offering tailored, impactful CRM tools.

### User Goals

- Empower sales teams with streamlined workflow and access to client data.
- Enhance office communication with field teams for quicker response times.

### Non-Goals

- This iteration will not focus on integrating third-party marketing tools.

## User Stories

- As a salesperson, I want to access lead information with a search bar, so I can quickly contact potential clients.
- As a manager, I need RBAC to ensure the right team members have access to specific client data.
- As a project manager, I want a projects section linked to customers, so I can track project progress effectively.
- As an office administrator, I want to push leads to field salespeople in real-time, so they can immediately act on fresh opportunities.

## User Experience

- **Search Functionality**: Users will readily find customer details using a dynamic search bar with filters and auto-complete options.
- **RBAC**: An intuitive admin dashboard to assign roles and access levels, ensuring data security.
- **Projects Section**: Newly designed dashboard for linking projects with customers, including a 'recently viewed' panel for quick access.
- **Leads Section**: Can filter, assign, and push lead information to salespeople's mobile devices or desktops.
- **Communication Platform**: Integrated real-time chat, supporting both group and private messages, along with a lead-pushing feature.

## Narrative

Small businesses often face the challenge of managing client relations effectively, a burden especially heavy on their sales teams. By harnessing the power of an integrated CRM system, sales teams break the shackles of organizational chaos. Imagine a day where salespeople in the field have instant data access, real-time office sync, and clear project visibility at their fingertips. This CRM tool not only boosts efficiency but also propels businesses ahead in a competitive market, holding a personal, powerful edge that clients love.

## Success Metrics

- 90% user satisfaction reported in user feedback.
- 25% reduction in time spent on administrative tasks.
- Increased conversion rates of leads by 15% within the first 6 months.

## Technical Considerations

- Search functionality may involve setting up Elasticsearch for optimized searches.
- RBAC will require securely storing and managing user roles and permissions.
- Projects and recently viewed functionality will need dynamic databases for mapping and quick retrieval.
- The communication platform may leverage WebSockets for real-time updates.

## Milestones & Sequencing

1. Complete search bar development and integrate into the CRM. (Completed)
2. Implement and test RBAC system. (Completed)
3. Develop the project section. (Completed)
4. Implement leads section. (Completed)
5. Connect customers, projects and leads, ensuring that leads can become cumstomers and projects can be tied to both through table ids.
6. Include 'recently viewed' feature in project, customers and leads.
7. Develop the communication platform.
8. Add a real-time feature to push leads out to sales people.
9. Add a calendar to the app that will be used with feature #7.
10. Develop a "follow up" form that allows date and time for a follow up contact that is automatically pushed to a calendar.
11. Consider Adding Soft Deletes: Implement a deleted or is*active field for soft deletes instead of actual deletion:
    is_active = db.Column(db.Boolean, default=True)
    primaryjoin="and*(Client.client_id==Contact.client_id, Contact.active==True)"
    Adds a filter: only include contacts where Contact.active == True.

12. Conduct beta testing with initial users and iterate based on feedback.

---

**NOTE: Below here is developer notes.**

## I. Business Info

- **a.** Name
- **b.** Address
- **c.** Email address
- **d.** Phone
- **e.** Contact person
  - **1.** Phone
  - **2.** Preferred communication method
- **f.** Contact notes
- **g.** Whose sale was it?
- **h.** Sales notes
  - **1.** What pricing tier are they in?
  - **2.** What extras were sold?
  - **3.** Did they have any ideas for their site?
  - **4.** How many pages and what are they?
  - **5.** Scheduling reminders?
- **i.** Contract date

## II. Reports

- **a.** Billing cycle (monthly or yearly?)
- **b.** Total revenue generated per client
- **c.** Payment status tracking

## III. Continuing Work On Websites

- **a.** Change request history
  - **1.** Dates
  - **2.** Pages
  - **3.** Sections
- **b.** Pending requests
  - **1.** Notes

## IV. Advertising Mailing List

- **a.** Direct Mailing Addresses List
  - **1.** Have they been sent a postcard?
  - **2.** Date
- **b.** Follow up contact time/date
- **c.** Marketing campaign notes
  - **1.** Success rate
  - **2.** Feedback

## V. PathSix Websites

- **a.** Domain
- **b.** Hosting site
- **c.** SSL status
- **d.** Notes
- **e.** Automated reminders

## VI. Hosting Accounts

- **a.** Website
- **b.** Cost

## VII. Planning board for projects

## VIII. Scheduling software

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

# PathSix CRM: Road to Version 1.0.0

## Current Status: v0.5.0

Core functionality implemented with final refinements needed for production release.

## Required Milestones for 1.0.0

### Code Structure and Naming

- [x] Complete customer -> client naming convention updates across all files
- [ ] Standardize template structure across all sections (projects, leads, clients)
- [ ] Ensure consistent modal implementation across all sections
- [x] Complete form standardization using dynamic form generation

### Data Validation and Error Handling

- [ ] Comprehensive form validation for all input fields
- [ ] Proper error handling for all database operations
- [ ] Consistent error message display
- [ ] Input sanitization verification
- [ ] File upload validation and error handling

### User Interface

- [ ] Consistent styling across all pages
- [ ] Mobile responsiveness verification
- [ ] Loading states for all actions
- [ ] Success/error feedback for all user actions
- [ ] Standardized button placement and styling
- [ ] Consistent modal behavior

### Search Functionality

- [ ] Update search to handle new client naming
- [ ] Optimize search performance
- [ ] Add search filters
- [ ] Improve search result display
- [ ] Add search history

### User Management

- [ ] Complete role-based access control
- [ ] User settings management
- [ ] Password reset functionality
- [ ] User activity logging
- [ ] Session management

### Testing

- [ ] Unit tests for core functionality
- [ ] Integration tests for main workflows
- [ ] User acceptance testing
- [ ] Security testing
- [ ] Load testing

### Documentation

- [ ] User manual
- [ ] Technical documentation
- [ ] Installation guide
- [ ] Configuration guide
- [ ] Backup/restore procedures

### Security

- [ ] Security audit completion
- [ ] XSS protection verification
- [ ] CSRF protection verification
- [ ] SQL injection protection verification
- [ ] Input validation security

### Database

- [ ] Database optimization
- [ ] Index optimization
- [ ] Migration scripts
- [ ] Backup procedures
- [ ] Data integrity checks

### Deployment

- [ ] Production environment setup guide
- [ ] Environment configuration documentation
- [ ] Database migration procedures
- [ ] Backup/restore procedures
- [ ] Monitoring setup

## Post-1.0.0 Features (Future Versions)

### 1.1.0 Planning

- Enhanced Reporting
  - Custom report builder
  - Export functionality
  - Data visualization

### 1.2.0 Planning

- Advanced Features
  - Calendar integration
    - Push follow up dates and notes to calendar
  - Email integration
  - Document management
  - Task management

### 1.3.0

- Real-Time Communication
- WebSocket implementation for instant messaging
- Direct messaging between users
- Group chat capabilities
- Lead notification system
  - Automatic lead assignment alerts
  - Project status change notifications
  - New lead notifications
- Message history and search
- File sharing within messages
- Read receipts and online status
- Mobile push notification support

### 1.4.0 Planning (In consideration)

- API Development
  - Basic REST API implementation
  - API authentication
  - API documentation

## Version Numbering Strategy

- 0.9.x: Pre-release refinements
- 1.0.0: First production release
- 1.x.0: Major feature additions
- 1.0.x: Bug fixes and minor improvements

## Sign-off Requirements for 1.0.0

1. All "Required Milestones" items checked
2. Testing completed with no critical bugs
3. Documentation complete
4. Security audit passed
5. Production deployment tested
