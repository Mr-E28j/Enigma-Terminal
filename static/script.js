document.getElementById("command-input").addEventListener("keypress", function(e) {
  if (e.key === "Enter") {
    let command = e.target.value;
    e.target.value = "";
    fetch('/command', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ command: command })
    })
    .then(response => response.json())
    .then(data => {
      let outputArea = document.getElementById("terminal-output");
      outputArea.textContent += "\n" + data.output;
      // Desplaza el scroll hasta el final
      let terminalDiv = document.getElementById("terminal");
      terminalDiv.scrollTop = terminalDiv.scrollHeight;
    });
  }
});
