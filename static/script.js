/**
 * Handle registration form submission
 */
async function handleRegisterSubmit(event) {
  event.preventDefault();

  // 1. Capture inputs
  const fullName = document.getElementById("reg-fullname").value.trim();
  const email = document.getElementById("reg-email").value.trim();
  const password = document.getElementById("reg-password").value;
  const registerBtn = document.getElementById("register-btn");
  const errorMessage = document.getElementById("error-message");

  // 2. Clear previous errors
  errorMessage.textContent = "";
  errorMessage.classList.add("hidden");

  // 3. Validate inputs locally
  if (!fullName || !email || !password) {
    displayError("Please fill in all fields");
    return;
  }

  if (password.length < 8) {
    displayError("Password must be at least 8 characters long");
    return;
  }

  // 4. Disable button during submission
  registerBtn.disabled = true;
  registerBtn.textContent = "Registering...";

  // 5. Prepare payload matching backend UserCreate schema
  const payload = {
    email: email,
    password: password,
    full_name: fullName,
  };

  try {
    const response = await fetch("/auth/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (response.status === 201) {
      // Success: Hide form and show success message
      document.getElementById("register-section").classList.add("hidden");
      document.getElementById("success-section").classList.remove("hidden");
    } else if (response.status === 400) {
      const errorData = await response.json();
      // Handle validation errors
      if (errorData.detail && Array.isArray(errorData.detail)) {
        const errorTexts = errorData.detail
          .map((err) => err.msg || err)
          .join(", ");
        displayError(`Registration failed: ${errorTexts}`);
      } else if (errorData.detail) {
        displayError(`Registration failed: ${errorData.detail}`);
      } else {
        displayError("Registration failed: Invalid input");
      }
    } else if (response.status === 409) {
      displayError("This email is already registered. Please try another one.");
    } else {
      const errorData = await response.json();
      displayError(
        `Registration failed: ${errorData.detail || "Unknown error"}`
      );
    }
  } catch (error) {
    console.error("Connection Error:", error);
    displayError(
      "Could not connect to the server. Please check your connection."
    );
  } finally {
    // Re-enable button
    registerBtn.disabled = false;
    registerBtn.textContent = "Register";
  }
}

/**
 * Display error message
 */
function displayError(message) {
  const errorMessage = document.getElementById("error-message");
  errorMessage.textContent = message;
  errorMessage.classList.remove("hidden");
}

/**
 * Reset form for new registration
 */
function resetForm() {
  document.getElementById("register-form").reset();
  document.getElementById("register-section").classList.remove("hidden");
  document.getElementById("success-section").classList.add("hidden");
  document.getElementById("error-message").classList.add("hidden");
}
