# inlustro_devops
**Recruitment Management System**

**Description:**

The Recruitment Management System is a web application developed using Flask, a Python web framework, designed to streamline the recruitment process, manage job applications, conduct assessments, and evaluate candidates efficiently. This system provides users with the ability to register, log in, take assessments, and view assessment results.

**Integration of HTML Templates:**

To integrate HTML templates into the Flask application, the following steps should be followed:

1. **Create HTML Files:** Develop HTML files for each route utilizing Flask's `render_template` function. The required HTML files include:

   - `registration_form.html`
   - `registration_result.html`
   - `login_form.html`
   - `welcome.html`
   - `test_options.html`
   - `aptitude_test.html`
   - `programming_test.html`
   - `results.html`

2. **Modify Routes:** Adapt the routes in the Flask application to render the specified HTML templates. Ensure that the HTML templates are stored in a directory named `templates` within the same directory as your Python script.

**Integration of Prometheus and Grafana:**

To monitor the performance and health of the Recruitment Management System, Prometheus can be utilized for collecting metrics, while Grafana can be used for visualization. The integration steps are as follows:

1. **Install Prometheus:**
   - Download and install Prometheus from the official website: [Prometheus Downloads](https://prometheus.io/download/)
   - Configure Prometheus to scrape metrics from the Flask application. Update the Prometheus configuration file (`prometheus.yml`) accordingly.

2. **Install Grafana:**
   - Download and install Grafana from the official website: [Grafana Download](https://grafana.com/get)
   - Configure Grafana to connect to Prometheus as a data source.
   - Develop dashboards in Grafana to visualize the metrics collected by Prometheus.

**Usage:**

1. **Registration Form:**
   - Access the registration form by visiting the root URL (`/`).
   - Complete the necessary details and submit the form.

2. **Login:**
   - Access the login form by visiting `/login`.
   - Enter the username and password to log in.

3. **Assessments:**
   - Select the type of assessment (Aptitude or Programming) from the test options page (`/test`).
   - Take the assessment by following the instructions on the respective assessment pages (`/aptitude_test` or `/programming_test`).

4. **View Results:**
   - View the assessment results by navigating to `/results`.
   - Results will be displayed for the logged-in user.

5. **Monitoring with Prometheus and Grafana:**
   - Access the Prometheus dashboard to monitor metrics collected from the Flask application.
   - Visualize metrics and construct custom dashboards in Grafana for comprehensive monitoring.

**Dependencies:**

- Flask
- SQLite3 (for database operations)
- Prometheus
- Grafana
- Random (for generating random data)

**Installation:**

1. Install Flask using pip:
   ```
   pip install Flask
   ```

2. Install Prometheus and Grafana following their respective installation guides.

3. Clone the project repository:
   ```
   git clone <repository_url>
   ```

4. Run the Flask application:
   ```
   python app.py
   ```

**Contributing:**

Contributions are welcome! If you would like to contribute to this project, please fork the repository and submit a pull request.

**License:**

This project is licensed under the [MIT License](LICENSE).
