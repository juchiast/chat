function getApiUrl() {
  if (window.location.origin.includes("localhost")) {
    return "http://localhost:8080/api";
  } else {
    return `${window.location.origin}/api`;
  }
}

function getWsUrl() {
  if (window.location.origin.includes("localhost")) {
    return "ws://localhost:8081/";
  } else {
    return `${window.location.origin}/ws`;
  }
}

export { getApiUrl, getWsUrl };