function togglePassword() {
  const input = document.getElementById("id_password");
  const isPassword = input.type === "password";
  input.type = isPassword ? "text" : "password";
}
