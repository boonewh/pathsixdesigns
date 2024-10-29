PathSix CRM

I. Business Info
a. name
b. address
c. email address
d. phone
e. contact person 1. phone 2. preferred communication method
f. contact notes
g. Whose sale was it?
h. sales notes 1. What pricing tier are they in? 2. What extras were sold? 3. Did they have any ideas for their site? 4. How many pages and what are they? 5. Scheduling reminders?
i. contract date
II. Reports
a. billing cycle (monthly or yearly?)
b. total revenue generated per client
c. payment status tracking
III. Continuing Work On Websites
a. change request history 1. dates 2. pages 3. sections
b. pending requests 1. notes
IV. Advertising Mailing List
a. Direct Mailing Addresses List 1. Have they been sent a postcard? 2. Date
b. Follow up contact time/date
c. Marketing campaign notes 1. success rate 2. feedback
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
