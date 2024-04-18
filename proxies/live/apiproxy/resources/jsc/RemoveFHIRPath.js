// Get current proxy URL
var proxyUrl = context.getVariable("proxy.url");

// Check if the proxy URL contains '/FHIR/R4/' string
if (proxyUrl.includes('/FHIR/R4/')) {
  // Disable copy path
  context.setVariable("target.copy.pathsuffix", false);

  // Replace string in incoming proxy URL path
  var proxyUrlReplaced = proxyUrl.replace('/FHIR/R4/', '/');
  print("Replaced: " + proxyUrlReplaced)

  // Replace outgoing url
  context.setVariable("target.url", proxyUrlReplaced);
}
