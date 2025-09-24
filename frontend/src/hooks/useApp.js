// src/hooks/useApp.js
export const useApp = () => {

 const loginUser = async (email, password) => {
  try {
    const response = await fetch("http://127.0.0.1:8000/api/users/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    const data = await response.json();
    if (response.ok) {
      // Save the access token from backend
      localStorage.setItem("token", data.access_token);

      // Optionally, save user info if needed
      localStorage.setItem("user", JSON.stringify(data.user));

      return { success: true };
    } else {
      return { success: false, error: data.detail || "Login failed" };
    }
  } catch (err) {
    console.error(err);
    return { success: false, error: "Server error" };
  }
};

  const registerUser = async (userData) => {
    try {
      const response = await fetch("http://127.0.0.1:8000/api/users/register", { // changed 127.0.0.1 → localhost
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(userData),
      });

      const data = await response.json();
      if (response.ok) {
        return { success: true };
      } else {
        return { success: false, error: data.detail || "Registration failed" };
      }
    } catch (err) {
      console.error(err);
      return { success: false, error: "Server error" };
    }
  };

  return { loginUser, registerUser };
};
