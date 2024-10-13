# BOTANIC LABS TESTING

# 1.0 AUTOMATED TESTING
Automated testing was undertaken using a range of open-source developer tools including Google Lighthouse Analysis, HTML, CSS and JavaScript validation. These tests assessed the applications quality, performance, accessibility and adherence to web standards. Any identified issues were addressed to enhance the websites usability and overall user experience.

## HTML Validation
To test the markup validity [HTML Validator](https://validator.w3.org/) was used to assess markup validity and compliance with accessibility standards. THe following table shows the results for each page:

### HTML Validation Test Results

#### Summary Table

## CSS Validation

The CSS code of the website was validated using the [W3C CSS Validator](https://jigsaw.w3.org/css-validator/#validate_by_input). The validation results are as follows:

## JSHint

### script.js Testing Report

## Lighthouse Analysis

# 2.0 MANUAL TESTING

## Feature Testing:


# BUGS
**User Profile Not Attached to Orders in Webhook Handling**

Issue: When capturing a payment via Stripe webhooks (e.g., by commenting out the form submission process to simulate a user closing the page before submission), the user_profile was not being attached to the order, even though the payment was successfully processed. The issue was caused by placing user_profile=profile in the wrong location within the webhook handler code.

Solution: The user_profile assignment was mistakenly placed within the section of the code that verifies if an order already exists, rather than in the section where a new order is created. Moving user_profile=profile to the correct location in the code, where the new order is created, ensured that user profiles are correctly attached to new orders processed through the webhook.

Outcome: After correcting the code placement, the user_profile is now correctly attached to orders, whether processed via the form submission or handled directly through Stripe webhooks. This allows user order history and profile data to function as expected in both cases.

**AttributeError When Using .split() on a NoneType Object in Product Recommendations**
Issue: An error occurred when adding new products due to an attempt to call the .split() method on a NoneType object while processing the recommendations field in the Product model.

Cause: The issue arose because the recommendations field was initially a CharField that could be left empty. When the field was empty, it was stored as None, and trying to call .split() on a NoneType value resulted in an error. The database was originally set up to allow admin users to enter recommendations as a string using product primary key (PK) numbers, with products separated by commas.

Solution: The Product model was refactored to improve usability by allowing admin users to select specific product recommendations instead of manually entering comma-separated strings. The recommendations field was replaced with three separate ForeignKey fields to allow relational selection of recommended products:

![Recommendations](botanic_labs/media/docs/wireframes/recommendations.png)

**Issue with Form Submission Using CKEditor**
Issue: After implementing CKEditor, the form was not submitting correctly when all required fields were filled, leading to form validation issues.

Cause: The issue stemmed from CKEditor not properly updating the content of the hidden textarea field when submitting the form. As a result, the form's content field appeared empty, causing validation errors.

Solution: The issue was resolved by switching to Summernote, a different rich text editor that integrates better with Django forms, preventing the submission issues encountered with CKEditor.