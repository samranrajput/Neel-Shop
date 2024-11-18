const {app, BrowserWindow} = require("electron");
function ElectronMainMethod(){
    const launchWindow = new BrowserWindow({
        title: "ec",
        width: 777,
        height: 444,
    });
    const appURL = "http://127.0.0.1:8000/home/";
    launchWindow.loadURL(appURL);
}
app.whenReady().then(ElectronMainMethod)