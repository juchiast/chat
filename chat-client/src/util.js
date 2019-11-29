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
    if (window.location.protocol === "https:") {
      return `wss://${window.location.host}/ws`;
    } else {
      return `ws://${window.location.host}/ws`;
    }
  }
}

export { getApiUrl, getWsUrl };