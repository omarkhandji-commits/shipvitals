Write-Host "ShipVitals installer"
if (Get-Command npm -ErrorAction SilentlyContinue) {
  npm install -g shipvitals
  Write-Host "Run: shipvitals audit ."
} elseif (Get-Command pipx -ErrorAction SilentlyContinue) {
  pipx install shipvitals-cli
  Write-Host "Run: shipvitals audit ."
} else {
  Write-Error "Install Node.js/npm or pipx, then run npm install -g shipvitals or pipx install shipvitals-cli."
}
