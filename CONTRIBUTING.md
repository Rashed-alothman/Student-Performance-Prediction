# Contributing to Student Performance Prediction System

First off, thank you for considering contributing to the Student Performance Prediction System! It's people like you that make this project such a valuable resource for the educational community.

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). Please read it to understand the expectations we have for everyone who contributes to this project.

## How Can I Contribute?

### Reporting Bugs

This section guides you through submitting a bug report. Following these guidelines helps maintainers and the community understand your report, reproduce the behavior, and find related reports.

**Before Submitting A Bug Report:**

- Check the [issues](https://github.com/Rashed-alothman/student_performance_project/issues) for a list of current known issues
- Perform a search to see if the problem has already been reported

**How Do I Submit A Good Bug Report?**
Bugs are tracked as GitHub issues. Create an issue and provide the following information:

- **Use a clear and descriptive title** for the issue to identify the problem
- **Describe the exact steps to reproduce the problem** with as much detail as possible
- **Provide specific examples to demonstrate the steps**
- **Describe the behavior you observed after following the steps**
- **Explain which behavior you expected to see instead and why**
- **Include screenshots or animated GIFs** that show the problem
- **If the problem is related to performance or memory**, include a CPU profile capture
- **If the problem is related to prediction accuracy**, include the input data and expected outputs
- **Include details about your configuration and environment**

### Suggesting Enhancements

This section guides you through submitting an enhancement suggestion, including completely new features and minor improvements to existing functionality.

**Before Submitting An Enhancement Suggestion:**

- Check if there's already a suggestion or feature that provides what you have in mind
- Determine which repository the enhancement should be suggested in
- Perform a search to see if the enhancement has already been suggested

**How Do I Submit A Good Enhancement Suggestion?**
Enhancement suggestions are tracked as GitHub issues. Create an issue and provide the following information:

- **Use a clear and descriptive title** for the issue to identify the suggestion
- **Provide a step-by-step description of the suggested enhancement** in as much detail as possible
- **Provide specific examples to demonstrate the steps** or mockups to illustrate the suggestion
- **Describe the current behavior** and **explain which behavior you expected to see instead** and why
- **Explain why this enhancement would be useful** to most users
- **List any other applications, libraries, or frameworks where this enhancement exists**

### Pull Requests

- Fill in the required template
- Do not include issue numbers in the PR title
- Include screenshots and animated GIFs in your pull request whenever possible
- Follow the [Python style guide](https://www.python.org/dev/peps/pep-0008/)
- Include thoughtfully-written tests whenever possible
- Document new code
- End all files with a newline

## Development Process

### Setting Up Development Environment

1. Fork the repository on GitHub
2. Clone your fork locally:

```
git clone https://github.com/[your-username]/project_student_performance.git
cd project_student_performance
```

3. Set up a virtual environment:

```
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

4. Install dependencies:

```
pip install -r requirements.txt
```

5. Create a branch for your feature or bugfix:

```
git checkout -b feature/your-feature-name
```

### Style Guidelines

#### Python Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use docstrings for all functions, classes, and modules
- Keep lines under 80 characters when possible
- Use meaningful variable names

#### JavaScript Style

- Use ES6 syntax where possible
- Follow [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- Use meaningful variable and function names
- Comment complex logic

#### HTML/CSS Style

- Use semantic HTML5 elements
- Follow [BEM methodology](http://getbem.com/) for CSS classes
- Maintain responsive design principles

### Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

## Testing

- Include tests for all new features or bug fixes
- Make sure all tests pass before submitting a pull request
- Describe the tests you've added in your pull request

## Documentation

- Update the README.md with details of changes to the interface
- Update the docs directory with any new information
- Comment your code where necessary

## Additional Notes

### Issue and Pull Request Labels

This section lists the labels we use to help us track and manage issues and pull requests.

- **bug** - Issues with the current codebase
- **documentation** - Improvements or additions to documentation
- **enhancement** - New features or improvements
- **good-first-issue** - Good for newcomers
- **help-wanted** - Extra attention is needed
- **question** - Further information is requested

## Attribution

These contributing guidelines are adapted from the [Atom](https://github.com/atom/atom/blob/master/CONTRIBUTING.md) and [Ruby on Rails](https://github.com/rails/rails/blob/main/CONTRIBUTING.md) contributing guidelines.
