PathSix CRM

<!-- prettier-ignore-start -->


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

Create a JavaScript-based client-side search that uses the cached data (companies) to filter results without making any server requests. This approach will be fast, especially for smaller to moderate-sized datasets, as it only involves searching through the already-loaded data.

Here’s how to do it:

Filter the Data Array: Use JavaScript to filter the companies array based on the search term.
Update the Display: Display the filtered results in the same way we set up the different report views.
Step-by-Step Example:
Assuming you have your companies data array already defined, you can add a search input and filter the table based on the search term.

HTML
Add a search input at the top of the page:

html
Copy code
<input type="text" id="search" placeholder="Search customers" onkeyup="filterCustomers()">

<table id="reportTable">
    <!-- Initial table will load here -->
</table>
JavaScript
Now, add a function to filter the data and update the table display based on the search input.

// Sample data for demonstration
const companies = [
{ company: "Acme Inc.", address: "123 Street", city: "Somewhere", state: "TX", zipcode: "12345", email: "contact@acme.com", phone: "123-456-7890" },
// Add more sample company data as needed
];

// Function to render the full customer overview table
function renderTable(data) {
const table = document.getElementById("reportTable");
table.innerHTML = `        
    <tr class="sm-thead">
            <th>Company</th><th>Address</th><th>City</th><th>State</th><th>Zipcode</th><th>Email</th><th>Phone</th>
        </tr>
        ${data.map(company =>`

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

// Call this function to initially load all data
renderTable(companies);

// Function to filter customers based on search input
function filterCustomers() {
const query = document.getElementById("search").value.toLowerCase();
const filteredData = companies.filter(company =>
company.company.toLowerCase().includes(query) ||
company.city.toLowerCase().includes(query) ||
company.email.toLowerCase().includes(query) ||
company.phone.includes(query)
);
renderTable(filteredData); // Update table with filtered data
}

Explanation
Initial Table Load: renderTable(companies) is called once to load all customer data when the page first loads.
Filter Function: filterCustomers is called each time the user types in the search input (using onkeyup). It filters the companies array by checking if any fields (e.g., company, city, email, or phone) contain the search term.
Dynamic Display Update: After filtering, renderTable(filteredData) updates the table to display only the search results.
This approach is efficient, and because it only manipulates data in memory, it provides a smooth and immediate search experience without requiring AJAX or additional server requests.

Ways to use JavaScript to enhance the user experience for the custom CRM:

1. Client-Side Form Validation
   Use JavaScript to validate form fields before they are submitted to the server. For example:
   Check if all required fields are filled out.
   Verify the format of email addresses or phone numbers.
   Provide instant error messages or feedback without a page reload, allowing users to correct mistakes immediately.
2. AJAX for Asynchronous Data Updates
   Create New Records: When adding a new client, JavaScript with AJAX can send the form data to Flask, and update the list of clients on the page without refreshing.
   Edit Records: Allow editing of client information in a modal or inline form and update the back-end using AJAX, which keeps the page smooth.
   Delete Records: Instead of a full-page reload after deleting, send a request via AJAX and remove the client from the view without reloading the entire page.
3. Dynamic Search and Filtering
   Add a search bar with JavaScript that filters clients, sales records, or updates as the user types. This gives immediate feedback and helps users find information quickly.
   You could use JavaScript to send a request to Flask to retrieve filtered data without reloading the page.
4. Interactive UI Elements
   Modals for Adding/Editing Data: Use JavaScript to show modals for adding or editing client info instead of navigating to a different page. This will keep users on the same page, making the experience feel smoother.
   Expandable Sections: Have expandable panels for different sections like "Business Info," "Reports," etc., allowing users to collapse/expand sections as needed.
   Date Pickers: For scheduling reminders, use a JavaScript-based date picker widget to make selecting dates more intuitive and less error-prone.
5. Real-Time Updates
   For sections like Continuing Work On Websites, you could use JavaScript to periodically poll the server or use WebSockets to get real-time updates on changes, ensuring users always see the most recent data.
6. Drag and Drop Features
   Implement a drag-and-drop feature for rearranging the order of clients or projects, which can be intuitive for users managing lists.
7. Inline Editing
   Allow inline editing of data fields. For example, users could click on a client’s address, edit it directly in place, and click away to save it via AJAX. This avoids having to navigate to an "edit" page, making data management quicker.
8. Notifications and Alerts
   Use JavaScript to create custom notifications for reminders or alerts. For instance, if a billing cycle is due, display an alert using JavaScript instead of relying on page refreshes.
9. Loading Spinners/Progress Indicators
   Whenever data is being fetched or an action is being processed, show a loading spinner to indicate progress. This helps improve user experience, especially when waiting for AJAX requests to complete.
10. Autocomplete for Form Inputs
    For input fields like "Business Name" or "Contact Person," use JavaScript to implement an autocomplete feature. This can help users quickly find existing records, which is especially useful if you have repeat clients or contacts.

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# 1. Clients Table

class Client(db.Model):
**tablename** = 'clients'

    client_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    website = db.Column(db.String(255))  # New column for the website name
    pricing_tier = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # Relationships to link related data
    addresses = db.relationship('Address', backref='client', lazy=True)
    contact_notes = db.relationship('ContactNote', backref='client', lazy=True)
    sales = db.relationship('Sale', backref='client', lazy=True)
    reminders = db.relationship('Reminder', backref='client', lazy=True)
    billing_cycles = db.relationship('BillingCycle', backref='client', lazy=True)
    website_updates = db.relationship('WebsiteUpdate', backref='client', lazy=True)
    mailing_lists = db.relationship('MailingList', backref='client', lazy=True)
    client_websites = db.relationship('ClientWebsite', backref='client', lazy=True)

    def __repr__(self):
        return f"Client('{self.name}', '{self.website}')"

# 2. Address Table

class Address(db.Model):
**tablename** = 'addresses'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.client_id'), nullable=False)  # Foreign key to Client
    name = db.Column(db.String(100))  # Name associated with this address, if applicable
    street = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    zip_code = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)


    def __repr__(self):
        return f"Address('{self.street}', '{self.city}', '{self.state}', '{self.zip_code}')"

# 3. ContactNote Table

class ContactNote(db.Model):
**tablename** = 'contact_notes'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.client_id'), nullable=False)
    note = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"ContactNote('Client ID: {self.client_id}', 'Note: {self.note[:30]}...')"

# 4. Sales Table

class Sale(db.Model):
**tablename** = 'sales'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.client_id'), nullable=False)
    sale_amount = db.Column(db.Float)
    sale_date = db.Column(db.DateTime, default=datetime.utcnow)
    extras_sold = db.Column(db.Text)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        return f"Sale('Client ID: {self.client_id}', 'Amount: {self.sale_amount}', 'Date: {self.sale_date}')"

# 5. BillingCycle Table

class BillingCycle(db.Model):
**tablename** = 'billing_cycles'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.client_id'), nullable=False)
    billing_cycle = db.Column(db.String(10))  # 'monthly' or 'yearly'
    last_billed = db.Column(db.DateTime)
    next_billing = db.Column(db.DateTime)
    payment_status = db.Column(db.String(10))  # e.g., 'pending', 'paid', 'overdue'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"BillingCycle('Client ID: {self.client_id}', 'Cycle: {self.billing_cycle}', 'Status: {self.payment_status}')"

# 6. Website Updates Table

class WebsiteUpdate(db.Model):
**tablename** = 'website_updates'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.client_id'), nullable=False)
    update_date = db.Column(db.DateTime, default=datetime.utcnow)
    pages_updated = db.Column(db.JSON)  # List of pages updated
    sections_updated = db.Column(db.JSON)  # Sections on each page updated
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"WebsiteUpdate('Client ID: {self.client_id}', 'Date: {self.update_date}')"

# 7. Mailing List Table

class MailingList(db.Model):
**tablename** = 'mailing_list'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.client_id'), nullable=False)
    address = db.Column(db.String(255))
    postcard_sent = db.Column(db.Boolean, default=False)
    date_sent = db.Column(db.DateTime)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"MailingList('Client ID: {self.client_id}', 'Address: {self.address}', 'Postcard Sent: {self.postcard_sent}')"

# 8. Domains and Hosting Table

class ClientWebsite(db.Model):
**tablename** = 'client_websites'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.client_id'), nullable=False)
    domain = db.Column(db.String(100), nullable=False)
    hosting_site = db.Column(db.String(100))
    ssl_status = db.Column(db.String(20))  # e.g., 'active', 'expiring', 'expired'
    renewal_date = db.Column(db.DateTime)
    hosting_cost = db.Column(db.Float)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"ClientWebsite('Client ID: {self.client_id}', 'Domain: {self.domain}', 'SSL Status: {self.ssl_status}')"
