# BOTANIC LABS TESTING

# 1.0 AUTOMATED TESTING
Automated testing was undertaken using a range of open-source developer tools including Google Lighthouse Analysis, HTML, CSS and JavaScript validation. These tests assessed the applications quality, performance, accessibility and adherence to web standards. Any identified issues were addressed to enhance the websites usability and overall user experience.

## HTML Validation
To test the markup validity [HTML Validator](https://validator.w3.org/) was used to assess markup validity and compliance with accessibility standards. THe following table shows the results for each page:





**Summary Table**
| Page             | Date       | Comments | Pass/Fail |
|------------------|------------|----------|-----------|
| Home             |    16/10/24        |          |    Pass       |
| Products         |    16/10/24       |          |     Pass      |
| Product Detail   |    16/10/24       |          |    Pass       |
| Add Product      |     18/10/24       |   Duplicate id - [Go to Duplicate ID Issue](#duplicate-id-in-custom_clearable_file_input)       |    Pass       |
| Edit Product     |     19/10/24       |   Add alt tag to img element.       |    Pass       |
| Bag              |   17/10/24         |          |    Pass       |
| Checkout         |    17/10/24        |          |    Pass       |
| Checkout Success |     17/10/24       |          |    Pass       |
| Profile          |     17/10/24       |          |    Pass       |
| Articles         |     17/10/24       |          |    Pass       |
| Article Detail   |   19/10/24         |  ![font-optical-sizing](botanic_labs/media/docs/wireframes/optical_font_sizing.jpg) The above error was recorded multiple times throughout the content block rendered by summernote. It seems the HTML validator does not recognise the CSS property 'font-optical-sizing'. Having checked the website across multiple browsers and screen sizes it is working correctly therefore this particularly error has been ignored. In the future I will experimenth with other WYSIWYG text editors.        |     Pass      |
| Add Article      |  19/10/24        | During HTML validation, several warnings and errors were encountered due to the implementation of the Summernote widget. These errors mainly include: Use of obsolete attributes like frameborder on iframe. Attributes such as maxlength, cols, rows, height, and width being incorrectly applied to <div> elements and invalid properties such as font-optical-sizing.Despite these validation warnings, they do not affect the functionality or performance of the website. Summernote’s rendering works as expected, and these validation issues are related to how Summernote generates its HTML structure, which is beyond the control of the project code. Given that Summernote is a widely used and maintained WYSIWYG editor, these warnings are safe to ignore unless a strict HTML validation is required for the project.  |           |
| Edit Article     |    19/10/24        |   As "Add Article"       |           |
| FAQ              |     19/10/24       |   As "Add Article"       |           |
| Add FAQ          |    19/10/24        |   As "Add Article"       |           |
| Edit FAQ         |     19/10/24       |   As "Add Article"       |           |
| Login            |   17/10/24         |          |    Pass       |
| Register         |   17/10/24         |          |    Pass       |
| Logout           |   17/10/24         |          |    Pass       |
| Password Reset   |   17/10/24         |          |    Pass       |
| 404 Error        |   17/10/24         |          |    Pass       |

## CSS Validation

The CSS code of the website was validated using the [W3C CSS Validator](https://jigsaw.w3.org/css-validator/#validate_by_input). The validation results are as follows:


| CSS File      | Errors | Warnings                                                                                                                                       | Comments                                                                                                                        | Testing Date   |
|---------------|--------|------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------|----------------|
| articles.css  | None   | -webkit-box is a vendor extension<br>-webkit-line-clamp is a vendor extension<br>-webkit-box-orient is a vendor extension                      | These warnings relate to non-standard CSS properties for Webkit browsers. They can be safely ignored since they ensure compatibility with browsers like Chrome and Safari. Fallbacks have been provided for browsers that do not support Webkit. | 06 October 2024 |
| stripe.css    | None   | -webkit-transition is a vendor extension                                                                                                       | This warning is related to the use of the non-standard CSS transition property for Webkit-based browsers. It can be ignored as it's necessary for smooth animation in browsers like Chrome and Safari. | 06 October 2024 |
| faq.css       | None   | None                                                                                                                                           | No errors or warnings present.                                                                                                  | 06 October 2024 |
| products.css  | None   | None                                                                                                                                           | No errors or warnings present.                                                                                                  | 06 October 2024 |
| profile.css   | None   | None                                                                                                                                           | No errors or warnings present.                                                                                                  | 06 October 2024 |
| base.css      | None   | -webkit-user-select is a vendor extension<br>-moz-user-select is a vendor extension<br>-ms-user-select is a vendor extension                   | These warnings refer to vendor-specific CSS extensions used to control text selection behaviour across different browsers. These properties can be safely ignored as they ensure consistent behaviour in Webkit, Firefox, and IE/Edge browsers. | 06 October 2024 |

## JSHint
The JavaScript code was validated using [JSHint](https://jshint.com/). The results of the validation are as follows:

| Page               | Results                      | Comment                                                                                                                                                                              | Pass/Fail |
|--------------------|------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| checkout          | No errors or warnings         | There are 5 functions in this file.<br>The function with the largest signature takes 1 argument, while the median is 1.<br>Largest function has 13 statements, median is 5.<br>The most complex function has a cyclomatic complexity value of 3, while the median is 2. | Pass      |
| Profile    | No errors or warnings         | There is only one function in this file.<br>It takes no arguments.<br>This function contains 4 statements.<br>Cyclomatic complexity number for this function is 2.                                                             | Pass      |
| add_Article        | No errors or warnings         | There is only one function in this file.<br>It takes no arguments.<br>This function contains 2 statements.<br>Cyclomatic complexity number for this function is 1.                                                             | Pass      |
| edit_article       | No errors or warnings         | There is only one function in this file.<br>It takes no arguments.<br>This function contains 2 statements.<br>Cyclomatic complexity number for this function is 1.                                                             | Pass      |
| bag                | No errors or warnings         | There are 3 functions in this file.<br>The function with the largest signature takes 1 argument, while the median is 1.<br>Largest function has 5 statements, median is 2.<br>The most complex function has a cyclomatic complexity value of 1, while the median is 1. | Pass      |
| add_product        | No errors or warnings         | There is only one function in this file.<br>It takes no arguments.<br>This function contains 2 statements.<br>Cyclomatic complexity number for this function is 1.                                                             | Pass      |
| edit_product       | No errors or warnings         | There is only one function in this file.<br>It takes no arguments.<br>This function contains 2 statements.<br>Cyclomatic complexity number for this function is 1.                                                             | Pass      |
| products           | No errors or warnings         | There are 2 functions in this file.<br>The function with the largest signature takes 1 argument, while the median is 0.5.<br>Largest function has 12 statements, median is 6.5.<br>The most complex function has a cyclomatic complexity value of 2, while the median is 1.5. | Pass      |

**N.B.** A number of the JavaScript files were identified as having undefined variables, typically related to jQuery’s $ and stripe. This occurs because they are from external libraries that JSHint does not recognise. These are not actual errors in the code, but warnings from JSHint, as it does not have knowledge of the external libraries.  

## Python Linter Test
Python files that were created or edited for this project were validated using [CI Python Linter](https://pep8ci.herokuapp.com/). Any identied issues were rectified. Gitpod also has a built-in Python Linter which can be accessed by using the command `pyonth3 -m flake8`.

All code edited and created for this project has passed the Python Linter validation tests. 

## Lighthouse Analysis
For this project, Google’s Lighthouse tool was primarily used as a diagnostic aid to identify areas for improvement, rather than as a score-driven objective. Lighthouse is designed to highlight key areas like performance, accessibility, and best practices, but it’s important to understand that its score is not a definitive measure of a website’s overall quality. While it offers valuable suggestions, focusing solely on achieving a perfect score can lead to misguided priorities that may not align with the specific goals of the project.

Key issues identified by Lighthouse were addressed, such as optimising image sizes and improving accessibility where feasible. However, the emphasis was on balancing practical performance enhancements with the real-world needs of the site’s users and functionality. The objective was not to chase perfect scores, but to ensure that the website is efficient, user-friendly, and meets essential accessibility standards.

Render-Blocking Resources:
In the performance review, Lighthouse flagged several third-party resources, such as Bootstrap, jQuery, and Google Fonts, as render-blocking elements that could potentially slow down the initial page load. These resources are essential for the core functionality and visual presentation of the website, and since they come from third-party CDNs, I do not have control over their optimisation. While these render-blocking issues were noted, removing or deferring them could compromise the site’s user experience and functionality. Given their importance, no action was taken to eliminate these resources as they are critical for the proper rendering and interactivity of the site.

| Page              | Performance |          | Accessibility |          | Best Practice |          | SEO  |          |
|-------------------|-------------|----------|---------------|----------|---------------|----------|------|----------|
|                   | Mobile (%)  | Desktop (%) | Mobile (%)    | Desktop (%) | Mobile (%)    | Desktop (%) | Mobile (%) | Desktop (%) |
| **Home**          | 72          | 96       | 100             | 100       | 100           | 96      | 100  | 100      |
| **Products**     | 78          | 95       | 96            | 96       | 100           | 100      |91  | 91      |
| **Articles**        | 78          | 94       | 100            | 100       | 100           | 100      | 100  | 100      |
| **Article**        | 80          | 93       | 95            | 95       | 100           | 100      | 100  | 100      |
| **Article Management**      | 79          | 88       | 95            | 95       | 100           | 100      | 100  | 100      |
| **Edit Article**       | 78          | 81       | 88            | 90       | 100           | 100      | 100  | 100      |
| **Faq**        | 77          | 94       | 100            | 100       | 100           | 100       | 100  | 100      |
| **New Faq**   | 74          | 81    | 95             | 95        | 96            | 100      | 100  | 100      |
| **Edit Faq**       | 81          | 84       | 96            | 96       | 100           | 100      | 100  | 100      |
| **Profile**| 74          | 75       | 94           | 94      | 100           | 100      | 100  | 100      |
| **Profile**| 74          | 75       | 94           | 94      | 100           | 100      | 100  | 100      |
| **Add Product**| 76          | 89       | 95          | 95      | 100           | 100      | 100  | 100      |
| **Edit Product**| 78          | 87       | 92          | 92      | 96           | 96      | 100  | 100      |
| **Bag**| 81          | 88       | 100          | 100      | 100           | 100      | 91  | 91     |
| **checkout**| 74          | 98       | 89          | 89      | 81           | 100      | 100  | 100     |
| **Confirmation**| 70          | 94       | 93          | 93      | 100           | 100      | 100  | 100     |
| **Logout**| 85          | 96       | 95          | 95      | 100           | 100      | 90  | 90     |
| **Register**| 83          | 96       | 91          | 91      | 100           | 100      | 90  | 90     |
| **Log in**| 84          | 96       | 91          | 91      | 100           | 100      | 90  | 90     |
| **404**| 85          | 96       | 95          | 95      | 96           | 96      | 90  | 100     |



# 2.0 MANUAL TESTING
## Browser Compatibility 
-   Expected: Consistent appearance and functionality across major browsers.
-   Testing: Test site on Chrome, Mozilla, Safari, and Edge browsers.
-   Outcome: The site renders as expected with good responsiveness and compatibility across different browsers.

## Responsiveness Test
- Expected: Site should render appropriately on various devices with different screen sizes. 
- Testing: Test responsiveness on iPhone 12, iPad 12, and desktop (1024px). 
- Outcome: The site displays responsively across different devices, maintaining functionality and appearance as intended.

## Feature Testing:


# BUGS
### Duplicate ID in custom_clearable_file_input

Issue:
When adding a product via the custom_clearable_file_input widget, an error was being raised due to the use of duplicate id attributes in the HTML. The first id was explicitly set in my form template and used by JavaScript to display the selected filename. The second id was automatically generated by the {% include "django/forms/widgets/attrs.html" %} tag, causing a conflict by introducing a second identical id on the page.

This violated HTML standards, as multiple elements cannot share the same id, and raised the following error during HTML validation:

![Duplicate Attribute id Warning](botanic_labs/media/docs/wireframes/duplicate_id_error.png)

Solution:
To resolve this issue:

	1. Remove the id attribute from the custom widget. 

![Remove id attribute from custom_clearable_file_input.html](botanic_labs/media/docs/wireframes/custom_clearable_file_input.jpg)

    2. 
    A. Add a class="new-image" to the input field for file selection in the forms.py. This is achieved by using the attrs attribute to pass a custom HTML attributes to CustomClearableFileInput.in the attrs dictionary the class attribute is set to include "new-image border-black rounded-0". the new-image class can be targetted with JavaScript for functionality.
    B. A condition has been set to skip adding additional classes to the image. This is done by checking if the current field being iterated over is the image field. If it is, the field.widget.attrs['class'] is not modified because the class attribute has alerady been assigned when defining CustomClearableFileInput. Without this condition check the class for CustomClearableFileInput is overwritten and it will not function correctly. 

![Add class="new-image" to input field](botanic_labs/media/docs/wireframes/forms.py.jpg)



	3.	The JavaScript was modified to reference this class ($('.new-image')) instead of the id to update the displayed filename dynamically.
	
![Modify the Javascript to target the new-image class](botanic_labs/media/docs/wireframes/Javascript.jpg)

Outcome:
After making these changes, the form works as expected. Users can now upload images without errors, and the filename updates dynamically as intended. The code passes HTML validation since no duplicate IDs are present.

**User Profile Not Attached to Orders in Webhook Handling**

Issue: When capturing a payment via Stripe webhooks (e.g., by commenting out the form submission process to simulate a user closing the page before submission), the user_profile was not being attached to the order, even though the payment was successfully processed. The issue was caused by placing user_profile=profile in the wrong location within the webhook handler code.

Solution: The user_profile assignment was mistakenly placed within the section of the code that verifies if an order already exists, rather than in the section where a new order is created. Moving user_profile=profile to the correct location in the code, where the new order is created, ensured that user profiles are correctly attached to new orders processed through the webhook.

Outcome: After correcting the code placement, the user_profile is now correctly attached to orders, whether processed via the form submission or handled directly through Stripe webhooks. This allows user order history and profile data to function as expected in both cases.

## AttributeError When Using .split() on a NoneType Object in Product Recommendations
Issue: An error occurred when adding new products due to an attempt to call the .split() method on a NoneType object while processing the recommendations field in the Product model.

Cause: The issue arose because the recommendations field was initially a CharField that could be left empty. When the field was empty, it was stored as None, and trying to call .split() on a NoneType value resulted in an error. The database was originally set up to allow admin users to enter recommendations as a string using product primary key (PK) numbers, with products separated by commas.

Solution: The Product model was refactored to improve usability by allowing admin users to select specific product recommendations instead of manually entering comma-separated strings. The recommendations field was replaced with three separate ForeignKey fields to allow relational selection of recommended products:

![Recommendations](botanic_labs/media/docs/wireframes/recommendations.png)

## Issue with Form Submission Using CKEditor
Issue: After implementing CKEditor, the form was not submitting correctly when all required fields were filled, leading to form validation issues.

Cause: The issue stemmed from CKEditor not properly updating the content of the hidden textarea field when submitting the form. As a result, the form's content field appeared empty, causing validation errors.

Solution: The issue was resolved by switching to Summernote, a different rich text editor that integrates better with Django forms, preventing the submission issues encountered with CKEditor.