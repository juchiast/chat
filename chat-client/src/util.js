export const getApiUrl = () => {
  if (window.location.origin.includes("localhost")) {
    return "http://localhost:8080/api";
  } else {
    return `${window.location.origin}/api`;
  }
}